# application/use_cases/challenge_use_cases.py


import copy
import io
import os
import zipfile
from collections import ChainMap
from datetime import datetime
from typing import Any, Dict, List, Optional, Type

from fastapi import BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from loguru import logger
from pydantic import BaseModel, TypeAdapter
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from BMC_API.src.api.dependencies.schemas import BulkOperationResponse
from BMC_API.src.application.dto.challenge_dto import (
    ChallengeHistoryModelDTO,
    ChallengeModelBaseOutputDTO,
    ChallengeModelUpdateDTO,
)
from BMC_API.src.application.dto.task_dto import (
    TaskModelBaseOutputDTO,
    TaskModelUpdateDTO,
)
from BMC_API.src.application.interfaces.email_scheduler import EmailSchedulerService
from BMC_API.src.application.use_cases.base_use_cases import BaseService
from BMC_API.src.application.use_cases.challenge_history_use_cases import (
    ChallengeHistoryService,
)
from BMC_API.src.application.use_cases.conference_use_cases import ConferenceService
from BMC_API.src.application.use_cases.task_history_use_cases import TaskHistoryService
from BMC_API.src.application.use_cases.task_use_cases import TaskService
from BMC_API.src.application.use_cases.user_use_cases import UserService
from BMC_API.src.core.config.settings import settings
from BMC_API.src.core.exceptions import RepositoryException
from BMC_API.src.domain.entities.challenge_model import ChallengeModel
from BMC_API.src.domain.interfaces.token_cache import TokenCache
from BMC_API.src.domain.repositories.challenge_repository import (
    ChallengeRepositoryProtocol,
)
from BMC_API.src.domain.services.status_manager import (
    Assignments,
    StatusActions,
    StatusBusiness,
)
from BMC_API.src.domain.value_objects.enums.challenge_enums import ChallengeStatus
from BMC_API.src.domain.value_objects.enums.user_enums import Roles
from BMC_API.src.infrastructure.external_services.challenge_to_pdf.challenge_to_pdf_converter import (
    convert_challenge_to_pdf,
)


class ChallengeSubmissionOps:
    def __init__(
        self,
        challenge_history_service: ChallengeHistoryService,
        task_history_service: TaskHistoryService,
    ):
        self.challenge_history_service = challenge_history_service
        self.task_history_service = task_history_service

    async def detect_differences(self, new_status, status_assignments, challenge_obj, task_list):
        differences_in_challenge = []
        differences_in_tasks = []

        # 1. Get challenge histories
        challenge_histories_obj, *_ = await self.challenge_history_service.list(
            search_filters={"challenge_id": challenge_obj.id}, sort_by="timestamp", sort_desc=True
        )

        if challenge_histories_obj and isinstance(challenge_histories_obj, list):
            if Assignments.RETAKE_SNAPSHOT in status_assignments:
                challenge_histories_obj_filtered = [
                    challenge_history
                    for challenge_history in challenge_histories_obj
                    if challenge_history.new_status != new_status
                ]
                challenge_history_last = challenge_histories_obj_filtered[0]
            else:
                challenge_history_last = challenge_histories_obj[0]
        else:
            challenge_history_last = challenge_histories_obj

        # Get column names of challenge model
        column_names = ChallengeModelUpdateDTO.model_fields.keys()
        for column_name in column_names:
            old_value = challenge_history_last.snapshot.get(column_name)
            new_value = getattr(challenge_obj, column_name)
            if old_value != new_value:
                differences_in_challenge.append({"field": column_name, "content": new_value})

        # Get task histories
        for task_obj in task_list:
            differences_in_task = []
            task_histories_in_db, *_ = await self.task_history_service.list(
                search_filters={"task_id": task_obj.id}, sort_by="timestamp", sort_desc=True
            )
            if task_histories_in_db and isinstance(task_histories_in_db, list):
                if Assignments.RETAKE_SNAPSHOT in status_assignments:
                    task_history_in_db_filtered = [
                        task_history for task_history in task_histories_in_db if task_history.new_status != new_status
                    ]
                    task_history_last = task_history_in_db_filtered[0]
                else:
                    task_history_last = task_histories_in_db[0]
            else:
                task_history_last = task_histories_in_db

            if task_history_last:
                # Get column names of challenge model
                column_names = TaskModelUpdateDTO.model_fields.keys()
                for column_name in column_names:
                    old_value = task_history_last.snapshot.get(column_name)
                    new_value = getattr(task_obj, column_name)
                    if old_value != new_value:
                        differences_in_task.append({"field": column_name, "content": new_value})
            differences_in_tasks.append(differences_in_task)

        return differences_in_challenge, differences_in_tasks

    def mark_differences(
        self, differences_in_challenge, differences_in_tasks, challenge_to_pdf, task_list_to_pdf, mark_color
    ):
        challenge_to_pdf.subheading = (
            f"###FONT_TAG_{mark_color.upper()}_START###"
            + f" Remark: This challenge has been slightly modified. All changes are highlighted in {mark_color}. "
            + "###FONT_TAG_END###"
        )
        if differences_in_challenge:
            for difference in differences_in_challenge:
                field = difference.get("field")
                content = difference.get("content")
                if isinstance(content, str):
                    new_content = (
                        f"###FONT_TAG_{mark_color.upper()}_START###" + " " + content + " " + "###FONT_TAG_END###"
                    )
                elif isinstance(content, list):
                    new_content = [f"###FONT_TAG_{mark_color.upper()}_START###"] + content + ["###FONT_TAG_END###"]
                setattr(
                    challenge_to_pdf,
                    field,
                    new_content,
                )

        if differences_in_tasks:
            for idx, differences_in_task in enumerate(differences_in_tasks):
                for difference in differences_in_task:
                    field = difference.get("field")
                    content = difference.get("content")
                    if isinstance(content, str):
                        new_content = (
                            f"###FONT_TAG_{mark_color.upper()}_START###" + " " + content + " " + "###FONT_TAG_END###"
                        )
                    elif isinstance(content, list):
                        new_content = [f"###FONT_TAG_{mark_color.upper()}_START###"] + content + ["###FONT_TAG_END###"]
                    setattr(
                        task_list_to_pdf[idx],
                        field,
                        new_content,
                    )
        return challenge_to_pdf, task_list_to_pdf

    async def take_snapshot(
        self,
        new_status,
        current_status,
        status_assignments,
        differences_in_challenge,
        differences_in_tasks,
        challenge_obj,
        task_list,
    ):
        timestamp = datetime.now()
        snapshot_fields = [
            field
            for field in ChallengeModelBaseOutputDTO.model_fields.keys()
            if field not in ["challenge_tasks", "challenge_owner", "challenge_conference"]
        ]

        # Create snapshot dynamically
        snapshot = {field: getattr(challenge_obj, field) for field in snapshot_fields if hasattr(challenge_obj, field)}

        # Convert datetime fields to ISO format
        for key, value in snapshot.items():
            if isinstance(value, datetime):
                snapshot[key] = value.isoformat()

        if Assignments.RETAKE_SNAPSHOT in status_assignments:
            challenge_histories, *_ = await self.challenge_history_service.list(
                search_filters={"challenge_id": challenge_obj.id}, sort_by="timestamp", sort_desc=True
            )
            challenge_history_latest = (
                challenge_histories[0] if isinstance(challenge_histories, list) else challenge_histories
            )
            if challenge_history_latest:
                updates = {
                    "changes": differences_in_challenge,
                    "snapshot": snapshot,
                    "timestamp": timestamp,
                    "version": challenge_obj.version,
                }
                await self.challenge_history_service.update(id=challenge_history_latest.id, model_update=updates)
        else:
            challenge_history_dict = {
                "challenge_id": challenge_obj.id,
                "version": challenge_obj.version,
                "old_status": current_status,
                "new_status": new_status,
                "challenge": challenge_obj,
                "changes": differences_in_challenge,
                "snapshot": snapshot,
                "timestamp": timestamp,
            }

            await self.challenge_history_service.create(challenge_history_dict)

        # Snapshot for tasks
        snapshot_fields = [field for field in TaskModelBaseOutputDTO.model_fields.keys()]

        # Create snapshot dynamically
        for idx, task_obj in enumerate(task_list):
            snapshot = {field: getattr(task_obj, field) for field in snapshot_fields if hasattr(task_obj, field)}

            # Convert datetime fields to ISO format
            for key, value in snapshot.items():
                if isinstance(value, datetime):
                    snapshot[key] = value.isoformat()

            if Assignments.RETAKE_SNAPSHOT in status_assignments:
                task_histories, *_ = await self.task_history_service.list(
                    search_filters={"task_id": task_obj.id}, sort_by="timestamp", sort_desc=True
                )
                task_history_latest = task_histories[0] if isinstance(task_histories, list) else task_histories
                if task_history_latest:
                    updates = {
                        "changes": differences_in_tasks[idx]
                        if isinstance(differences_in_tasks, list) and differences_in_tasks
                        else [],
                        "snapshot": snapshot,
                        "timestamp": timestamp,
                        "version": task_obj.version,
                    }
                    await self.task_history_service.update(id=task_history_latest.id, model_update=updates)
            else:
                task_history_dict = {
                    "task_id": task_obj.id,
                    "challenge_id": task_obj.task_challenge_id,
                    "version": task_obj.version,
                    "old_status": current_status,
                    "new_status": new_status,
                    "changes": differences_in_tasks[idx]
                    if isinstance(differences_in_tasks, list) and differences_in_tasks
                    else [],
                    "snapshot": snapshot,
                    "timestamp": timestamp,
                }
                await self.task_history_service.create(task_history_dict)


class ChallengeService(BaseService[ChallengeModel, ChallengeModelBaseOutputDTO]):
    def __init__(
        self,
        repository: ChallengeRepositoryProtocol,
        dto_class: Optional[Type[BaseModel]] = None,
        token_cache: Optional[TokenCache] = None,
        conference_service: ConferenceService = None,
        task_service: TaskService = None,
        challenge_history_service: ChallengeHistoryService = None,
        task_history_service: TaskHistoryService = None,
        user_service: UserService = None,
    ) -> None:
        super().__init__(repository, dto_class)
        self.token_cache = token_cache
        self.conference_service = conference_service
        self.task_service = task_service
        self.challenge_history_service = challenge_history_service
        self.task_history_service = task_history_service
        self.user_service = user_service
        self.submission_ops = ChallengeSubmissionOps(
            challenge_history_service,
            task_history_service,
        )

    async def challenge_histories(self, id: int) -> List:
        obj = await super().get_raw(id)
        if obj.histories:
            return (
                TypeAdapter(List[ChallengeHistoryModelDTO]).validate_python(obj.histories),
                1,
                len(obj.histories),
            )
        else:
            raise RepositoryException(f"No history found for challenge {id}")

    async def update_challenge(self, id: int, model_update: Dict) -> ChallengeModelBaseOutputDTO:
        challenge_obj = await self.get_raw(id)
        current_status = challenge_obj.challenge_status
        new_status = StatusActions.next_status_for_update(current_status)
        model_update["challenge_modified_time"] = datetime.now()
        model_update["challenge_status"] = new_status
        return await super().update(id=id, model_update=model_update)

    async def update_challenge_bulk(
        self, updates: List[Dict[str, Any]]
    ) -> BulkOperationResponse[ChallengeModelBaseOutputDTO]:
        for entity_data in updates:
            challenge_obj = await self.get_raw(entity_data["id"])
            current_status = challenge_obj.challenge_status
            new_status = StatusActions.next_status_for_update(current_status)
            entity_data["challenge_modified_time"] = datetime.now()
            entity_data["challenge_status"] = new_status

        return await super().update_bulk(updates=updates)

    async def prune_challenge(self, id: int) -> BulkOperationResponse:
        """Delete a challenge, challenge histories, its related tasks and task histories."""
        challenge_obj = await self.get_raw(id)
        challenge_tasks = challenge_obj.challenge_tasks

        successful_results = []
        failed_results = []

        # 1. Delete challenge tasks histories
        task_history_ids = [history.id for task in challenge_tasks for history in task.histories]
        if task_history_ids:
            result = await self.task_history_service.delete_bulk(ids=task_history_ids)
            if result.successful:
                successful_results.append({"task histories": result.successful})
            if result.failed:
                failed_results.append({"task histories": result.failed})

        # 2. Delete challenge tasks
        task_ids = [task.id for task in challenge_tasks]
        if task_ids:
            result = await self.task_service.delete_bulk(ids=task_ids)
            if result.successful:
                successful_results.append({"tasks": result.successful})
            if result.failed:
                failed_results.append({"tasks": result.failed})

        # 3. Delete challenge histories
        challenge_history_ids = [history.id for history in challenge_obj.histories]
        if challenge_history_ids:
            result = await self.challenge_history_service.delete_bulk(ids=challenge_history_ids)
            if result.successful:
                successful_results.append({"challenge histories": result.successful})
            if result.failed:
                failed_results.append({"challenge histories": result.failed})

        # 3. Delete challenge
        try:
            await self.delete(id=id)
            successful_results.append({"challenge": [id]})
        except Exception as e:
            failed_results.append({"challenge id": [id], "error": str(e)})

        successful = dict(ChainMap(*successful_results))
        len_successful = sum([len(val) for val in successful.values()])
        failed = dict(ChainMap(*failed_results))
        len_failed = sum([len(val) for val in failed.values()])
        return BulkOperationResponse(
            detail=f"Bulk prune completed: {len_successful} successful, {len_failed} failed.",
            successful=successful,
            failed=failed,
        )
    async def prune_challenges_bulk(self, ids: List[int]) -> BulkOperationResponse[Any]:
        """
        Prune multiple entities by their IDs.

        Args:
            ids: List of entity IDs to prune

        Returns:
            List of successful deletion results
        """
        successful_results = []
        failed_results = []

        for entity_id in ids:
            try:
                await self.prune_challenge(id=entity_id)
                successful_results.append(entity_id)
            except NoResultFound:
                failed_results.append({
                    "id": entity_id,
                    "error": f"{self.model_name} with id {entity_id} not found.",
                })
                logger.warning(f"{self.model_name} with id {entity_id} not found for deletion.")
            except Exception as e:
                failed_results.append({"id": entity_id, "error": str(e)})
                logger.error(f"Error pruning {self.model_name} with id {entity_id}: {e}")
                continue

        return BulkOperationResponse[Any](
            detail=f"Bulk prune completed: {len(successful_results)} successful, {len(failed_results)} failed.",
            successful=successful_results,
            failed=failed_results,
        )


    async def status(self, id: int, new_status: ChallengeStatus) -> ChallengeModelBaseOutputDTO:
        """Transactional update the status of a challenge and its related tasks."""

        timestamp = datetime.now()

        # Use the same database session for both operations
        db_session: AsyncSession = self.repository.session
        task_session: AsyncSession = self.task_service.repository.session

        if db_session != task_session:
            raise ValueError(
                "ChallengeService and TaskService must share the same DB session for transactional safety."
            )

        try:
            challenge_obj = await self.get_raw(id)
            challenge_tasks = challenge_obj.challenge_tasks

            if challenge_tasks:
                updates = [
                    {"id": task.id, "task_modified_time": timestamp, "task_status": new_status}
                    for task in challenge_tasks
                ]
                await self.task_service.update_bulk(updates=updates)

            challenge_update_data = {"challenge_modified_time": timestamp, "challenge_status": new_status}
            updated_challenge = await self.update(id=id, model_update=challenge_update_data)

            await db_session.commit()
            return updated_challenge

        except Exception as e:
            await db_session.rollback()
            raise e

    async def bulk_status(self, ids: List[int], new_status: str) -> BulkOperationResponse[ChallengeModelBaseOutputDTO]:
        """Bulk update the status of multiple challenges and their related tasks."""

        successful_results = []
        failed_results = []

        db_session = self.repository.session
        task_session = self.task_service.repository.session

        if db_session != task_session:
            raise ValueError("ChallengeService and TaskService must share the same DB session.")

        for challenge_id in ids:
            timestamp = datetime.now()

            try:
                # Get the challenge and related tasks
                challenge_obj = await self.get_raw(challenge_id)
                challenge_tasks = challenge_obj.challenge_tasks

                if challenge_tasks:
                    task_updates = [
                        {"id": task.id, "task_modified_time": timestamp, "task_status": new_status}
                        for task in challenge_tasks
                    ]
                    await self.task_service.update_bulk(updates=task_updates)

                # Update the challenge
                challenge_update_data = {"challenge_modified_time": timestamp, "challenge_status": new_status}
                updated_challenge = await self.update(id=challenge_id, model_update=challenge_update_data)

                successful_results.append(updated_challenge)

            except Exception as e:
                await db_session.rollback()
                failed_results.append({"id": challenge_id, "error": str(e)})
                continue

        await db_session.commit()

        return BulkOperationResponse[Any](
            detail=f"Bulk status update completed: {len(successful_results)} successful, {len(failed_results)} failed.",
            successful=successful_results,
            failed=failed_results,
        )

    async def download_challenge(self, id: int) -> FileResponse:
        obj = await super().get_raw(id)
        if not obj.challenge_file:
            HTTPException(
                status_code=403,
                detail="The challenge has not been submitted yet. Please submit it first.",
            )
        try:
            proposal_file_name = obj.challenge_file
            file_full_path = os.path.join(settings.submissions_folder, proposal_file_name)

            os.stat(file_full_path)
            headers = {
                "X-Content-Filename": proposal_file_name,  # Emre: Do NOT forget to add this to server/nginx configuration!
            }
            return FileResponse(
                path=file_full_path,
                media_type="application/pdf",
                filename=proposal_file_name,
                headers=headers,
            )
        except RuntimeError as e:
            logger.error(str(e))
            raise HTTPException(
                status_code=503,
                detail="Something went wrong. Please contact the admins",
            )
        except FileNotFoundError as e:
            logger.error(str(e))
            raise HTTPException(
                status_code=404,
                detail="Challenge file not found. Please contact the admins",
            )
        except Exception as e:
            logger.error(str(e))
            raise HTTPException(
                status_code=503,
                detail="Something went wrong. Please contact the admins",
            )

    async def download_challenge_bulk(self, ids: List[int]) -> StreamingResponse:
        """
        Download multiple challenge files and package them into a ZIP archive.
        Directly return a StreamingResponse.
        """
        successful_ids = []
        failed_results = []
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for id in ids:
                try:
                    obj = await super().get_raw(id)
                    if not obj.challenge_file:
                        error_msg = f"Challenge {id} has no submitted file."
                        failed_results.append({"id": id, "error": error_msg})
                        logger.warning(error_msg)
                        continue

                    proposal_file_name = obj.challenge_file
                    file_path = os.path.join(settings.submissions_folder, proposal_file_name)

                    os.stat(file_path)

                    with open(file_path, "rb") as f:
                        file_data = f.read()
                        zip_file.writestr(proposal_file_name, file_data)

                    successful_ids.append(id)

                except FileNotFoundError:
                    error_msg = f"Challenge file not found for id {id}."
                    failed_results.append({"id": id, "error": error_msg})
                    logger.error(error_msg)
                    continue
                except Exception as e:
                    error_msg = f"Error processing challenge id {id}: {str(e)}"
                    failed_results.append({"id": id, "error": error_msg})
                    logger.error(error_msg)
                    continue

        if not successful_ids:
            raise HTTPException(status_code=404, detail="No challenge files found for the provided IDs.")

        zip_buffer.seek(0)

        response = StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={
                "Content-Disposition": "attachment; filename=challenges_bulk_download.zip",
                "X-Successful-IDs": ",".join(map(str, successful_ids)),
                "X-Failed-Count": str(len(failed_results)),
            },
        )
        return response

    async def take_snapshot(self, id: int):
        challenge_obj = await self.get_raw(id)
        task_list = challenge_obj.challenge_tasks
        current_status = challenge_obj.challenge_status

        differences_in_challenge, differences_in_tasks = await self.submission_ops.detect_differences(
            new_status=current_status, status_assignments=[], challenge_obj=challenge_obj, task_list=task_list
        )

        await self.submission_ops.take_snapshot(
            new_status=current_status,
            current_status=current_status,
            status_assignments=[],
            differences_in_challenge=differences_in_challenge,
            differences_in_tasks=differences_in_tasks,
            challenge_obj=challenge_obj,
            task_list=task_list,
        )

    async def submit_challenge(
        self, id: int, background_tasks: BackgroundTasks, send_notification_emails: bool = False
    ) -> None:
        submission_time = datetime.now()

        # PREPARATIONS
        ## 1. Get challenge object and tasks of challenge
        challenge_obj = await self.get_raw(id)
        task_list = challenge_obj.challenge_tasks

        ## 2. Create clean copies of challenge and task objects for PDF export. Remove irrelevant fields.
        challenge_to_pdf = copy.deepcopy(challenge_obj)
        setattr(challenge_to_pdf, "histories", [])
        setattr(challenge_to_pdf, "challenge_tasks", [])
        setattr(challenge_to_pdf, "challenge_conference", None)
        setattr(challenge_to_pdf, "challenge_owner", None)

        task_list_to_pdf = copy.deepcopy(list(task_list))
        for task_obj in task_list_to_pdf:
            setattr(task_obj, "histories", [])
            setattr(task_obj, "task_challenge", None)
            setattr(task_obj, "task_owner", None)

        ## 3. Detect new status
        current_status = challenge_obj.challenge_status
        new_status = StatusActions.next_status_for_submit(current_status)

        ## 4. Get task/business list for new status
        status_assignments = StatusBusiness.status_assignments(new_status)
        if new_status == current_status and new_status not in [
            ChallengeStatus.ACCEPT,
            ChallengeStatus.ACCEPT_AS_LIGHTHOUSE_CHALLENGE,
            ChallengeStatus.ACCEPT_AS_STANDARD_CHALLENGE,
            ChallengeStatus.ACCEPTED_MODIFIED,
        ]:
            status_assignments.append(Assignments.RETAKE_SNAPSHOT)

        # OPERATIONS
        ## 1. Find and mark the modified sections between two statuses
        if Assignments.GET_DIFF in status_assignments:
            differences_in_challenge, differences_in_tasks = await self.submission_ops.detect_differences(
                new_status, status_assignments, challenge_obj, task_list
            )
        else:
            differences_in_challenge = []
            differences_in_tasks = []

        ## 2. Mark updated sections in challenge_to_pdf and task_list_to_pdf
        if (differences_in_challenge or differences_in_tasks) and Assignments.MARK_DIFFS_BLUE in status_assignments:
            mark_color = "blue"
            challenge_to_pdf, task_list_to_pdf = self.submission_ops.mark_differences(
                differences_in_challenge, differences_in_tasks, challenge_to_pdf, task_list_to_pdf, mark_color
            )

        elif (differences_in_challenge or differences_in_tasks) and Assignments.MARK_DIFFS_RED in status_assignments:
            mark_color = "red"
            challenge_to_pdf, task_list_to_pdf = self.submission_ops.mark_differences(
                differences_in_challenge, differences_in_tasks, challenge_to_pdf, task_list_to_pdf, mark_color
            )

        ## 3. Snapshot for challenges

        if Assignments.TAKE_SNAPSHOT in status_assignments:
            await self.submission_ops.take_snapshot(
                new_status,
                current_status,
                status_assignments,
                differences_in_challenge,
                differences_in_tasks,
                challenge_obj,
                task_list,
            )

        ## 4. Export PDF file for the proposal
        if Assignments.EXPORT_PROPOSAL in status_assignments:
            try:
                proposal_file_name = convert_challenge_to_pdf(challenge_to_pdf, task_list_to_pdf)
                file_full_path = os.path.join(settings.submissions_folder, proposal_file_name)
                os.stat(file_full_path)
            except HTTPException as e:
                raise e
            except Exception as e:
                logger.error(str(e))
                raise e

            # Prepare submission PDF file
            try:
                file_full_path = os.path.join(settings.submissions_folder, proposal_file_name)
                os.stat(file_full_path)
            except RuntimeError as e:
                logger.error(str(e))
                raise HTTPException(
                    status_code=503,
                    detail="Something went wrong. Please contact the admins",
                )
            except FileNotFoundError as e:
                logger.error(str(e))
                raise HTTPException(
                    status_code=404,
                    detail="Challenge file not found. Please contact the admins",
                )
            except Exception as e:
                logger.error(str(e))
                raise e
            else:
                challenge_file_location = str(file_full_path)

        ## 5. Send notification e-mails if requested
        if send_notification_emails and settings.environment != "dev":
            email_scheduler = EmailSchedulerService(background_tasks)
            challenge_name = str(challenge_obj.challenge_name)

            # 1. Send notifications to admins
            if Assignments.SUBMISSION_EMAIL_TO_ADMINS in status_assignments:
                try:
                    admin_list, *_ = await self.user_service.list(search_filters={"roles__contains": Roles.ADMIN})

                    if admin_list and not isinstance(admin_list, list) and isinstance(admin_list, str):
                        admin_list = [admin_list]

                    # Clear fake e-mail address of DEFAULT_ADMIN_NAME
                    admin_emails = [admin.email for admin in admin_list if admin.email != settings.DEFAULT_ADMIN_NAME]

                    recipients = list(set(admin_emails))
                    logger.info(f"E-mail will be requested for {recipients}")
                    
                    if recipients:
                        email_scheduler.schedule_draft_submitted(
                            recipients, submission_time, challenge_name, challenge_file_location
                        )
                        
                except Exception as e:
                    logger.exception(f"E-mail requested for {recipients} failed.")
                    logger.exception(e)
            # 2. Send notifications to conference chairs
            if Assignments.SUBMISSION_EMAIL_TO_CHAIRS in status_assignments:
                try:
                    recipients = challenge_obj.challenge_conference.chairperson_emails
                    if recipients and not isinstance(recipients, list) and isinstance(recipients, str):
                        recipients = [recipients]

                    logger.info(f"E-mail will be requested for {recipients}")
                    if recipients:
                        email_scheduler.schedule_draft_submitted(
                            recipients, submission_time, challenge_name, challenge_file_location
                        )
                except Exception as e:
                    logger.exception(f"E-mail requested for {recipients} failed.")
                    logger.exception(e)

            # 3. Send notifications to user
            if Assignments.SUBMISSION_EMAIL_TO_USER in status_assignments:
                try:
                    user = challenge_obj.challenge_owner
                    recipients = user.email
                    if recipients and not isinstance(recipients, list) and isinstance(recipients, str):
                        recipients = [recipients]
                    first_name = user.first_name
                    last_name = user.last_name
                    
                    logger.info(f"E-mail will be requested for {recipients}")
                    if recipients:
                        email_scheduler.schedule_own_draft_submitted(
                            recipients, submission_time, first_name, last_name, challenge_name, challenge_file_location
                        )
                except Exception as e:
                    logger.exception(f"E-mail requested for {recipients} failed.")
                    logger.exception(e)
        ## 6. Update challenge and its tasks

        # Increase the version
        new_version = challenge_obj.version + 1 if challenge_obj.version else 1

        # Use the same database session for both operations
        db_session: AsyncSession = self.repository.session  # assuming your repository exposes .session
        task_session: AsyncSession = self.task_service.repository.session

        if db_session != task_session:
            raise ValueError(
                "ChallengeService and TaskService must share the same DB session for transactional safety."
            )

        try:
            if task_list:
                updates = [
                    {
                        "id": task_obj.id,
                        "task_submission_time": submission_time,
                        "task_status": new_status,
                        "version": new_version,
                    }
                    for task_obj in task_list
                ]
                await self.task_service.update_bulk(updates=updates)

            challenge_update_data = {
                "challenge_submission_time": submission_time,
                "challenge_status": new_status,
                "version": new_version,
                "challenge_file": proposal_file_name,
            }
            updated_challenge = await self.update(id=challenge_obj.id, model_update=challenge_update_data)

            await db_session.commit()
            return updated_challenge

        except Exception as e:
            await db_session.rollback()
            raise e
