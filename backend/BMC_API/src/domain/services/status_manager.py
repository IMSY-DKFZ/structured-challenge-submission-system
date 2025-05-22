from enum import Enum

from BMC_API.src.domain.value_objects.enums.challenge_enums import ChallengeStatus

"""
Status transitions done by system when it is triggered. 
If there is no transition found for current status, 
this means the object reached to its final status for system-wise auto transition. 
After that, only Admins can change the status manually. 
"""
status_transitions_for_update = {
    # Initial submission statuses
    ChallengeStatus.DRAFT: ChallengeStatus.DRAFT_UPDATED,
    # Revision statuses
    ChallengeStatus.MINOR_REVISION_REQUIRED: ChallengeStatus.REVISION_UPDATED,
    ChallengeStatus.MAJOR_REVISION_REQUIRED: ChallengeStatus.REVISION_UPDATED,
    # Preliminary accepted statuses
    ChallengeStatus.PRELIM_ACCEPT_AS_STANDARD_CHALLENGE: ChallengeStatus.REVISION_UPDATED_PRELIM_ACCEPT,
    ChallengeStatus.PRELIM_ACCEPT_AS_LIGHTHOUSE_CHALLENGE: ChallengeStatus.REVISION_UPDATED_PRELIM_ACCEPT,
    # After acceptance, statuses for further modifications
    ChallengeStatus.ACCEPTED_MODIFIED_DRAFT: ChallengeStatus.ACCEPTED_MODIFIED_UPDATED,
}

status_transitions_for_submit = {
    # Initial submission statuses
    ChallengeStatus.DRAFT: ChallengeStatus.DRAFT_SUBMITTED,
    ChallengeStatus.DRAFT_UPDATED: ChallengeStatus.DRAFT_SUBMITTED,
    # Revision statuses
    ChallengeStatus.MINOR_REVISION_REQUIRED: ChallengeStatus.REVISION_SUBMITTED,
    ChallengeStatus.MAJOR_REVISION_REQUIRED: ChallengeStatus.REVISION_SUBMITTED,
    ChallengeStatus.REVISION_UPDATED: ChallengeStatus.REVISION_SUBMITTED,
    # Preliminary accepted statuses
    ChallengeStatus.PRELIM_ACCEPT_AS_STANDARD_CHALLENGE: ChallengeStatus.REVISION_SUBMITTED_PRELIM_ACCEPT,
    ChallengeStatus.PRELIM_ACCEPT_AS_LIGHTHOUSE_CHALLENGE: ChallengeStatus.REVISION_SUBMITTED_PRELIM_ACCEPT,
    ChallengeStatus.REVISION_UPDATED_PRELIM_ACCEPT: ChallengeStatus.REVISION_SUBMITTED_PRELIM_ACCEPT,
    # After acceptance, statuses for further modifications
    ChallengeStatus.ACCEPTED_MODIFIED_DRAFT: ChallengeStatus.ACCEPTED_MODIFIED_SUBMITTED,
    ChallengeStatus.ACCEPTED_MODIFIED_UPDATED: ChallengeStatus.ACCEPTED_MODIFIED_SUBMITTED,
}


class Assignments(str, Enum):
    """All related task definitions"""

    TAKE_SNAPSHOT = "Take snapshot"
    RETAKE_SNAPSHOT = "Retake snapshot"  # Overwrite to the last snapshot
    EXPORT_PROPOSAL = "Export proposal"
    GET_DIFF = "Get differences from latest snapshot"
    MARK_DIFFS_RED = "Mark differences with red"
    MARK_DIFFS_BLUE = "Mark differences with blue"
    SUBMISSION_EMAIL_TO_USER = "Send email notification about proposal file to the user"
    SUBMISSION_EMAIL_TO_CHAIRS = "Send email notification about proposal file to the chairs"
    SUBMISSION_EMAIL_TO_ADMINS = "Send email notification about proposal file to the admins"


class StatusActions:
    @staticmethod
    def next_status_for_update(current_status: ChallengeStatus):
        new_status = status_transitions_for_update.get(current_status)
        if new_status:
            return new_status
        else:
            return current_status

    @staticmethod
    def next_status_for_submit(current_status: ChallengeStatus):
        new_status = status_transitions_for_submit.get(current_status)
        if new_status:
            return new_status
        else:
            return current_status

    def eligible_to_change(self):
        if self.current_status in [
            ChallengeStatus.LOCKED,
            ChallengeStatus.REJECT,
            # ChallengeStatus.ACCEPT,
            # ChallengeStatus.REJECT,
            # ChallengeStatus.ACCEPT_AS_LIGHTHOUSE_CHALLENGE,
            # ChallengeStatus.ACCEPT_AS_STANDARD_CHALLENGE,
            # ChallengeStatus.ACCEPTED_MODIFIED,
        ]:
            return False
        return True


class StatusBusiness:
    """Put all automation logic here like what happens after an action"""

    @staticmethod
    def status_assignments(status: ChallengeStatus):
        tasks = []
        if status == ChallengeStatus.DRAFT_SUBMITTED:
            tasks.append(Assignments.TAKE_SNAPSHOT)
            tasks.append(Assignments.EXPORT_PROPOSAL)
            tasks.append(Assignments.SUBMISSION_EMAIL_TO_USER)
            tasks.append(Assignments.SUBMISSION_EMAIL_TO_CHAIRS)
            tasks.append(Assignments.SUBMISSION_EMAIL_TO_ADMINS)

        if status in [
            ChallengeStatus.REVISION_SUBMITTED,
            ChallengeStatus.REVISION_SUBMITTED_PRELIM_ACCEPT,
        ]:
            tasks.append(Assignments.TAKE_SNAPSHOT)
            tasks.append(Assignments.GET_DIFF)
            tasks.append(Assignments.MARK_DIFFS_BLUE)
            tasks.append(Assignments.EXPORT_PROPOSAL)
            tasks.append(Assignments.SUBMISSION_EMAIL_TO_USER)
            tasks.append(Assignments.SUBMISSION_EMAIL_TO_CHAIRS)
            tasks.append(Assignments.SUBMISSION_EMAIL_TO_ADMINS)


        if status in [
            ChallengeStatus.ACCEPTED_MODIFIED_SUBMITTED,
            ChallengeStatus.ACCEPT,
            ChallengeStatus.ACCEPT_AS_LIGHTHOUSE_CHALLENGE,
            ChallengeStatus.ACCEPT_AS_STANDARD_CHALLENGE,
            ChallengeStatus.ACCEPTED_MODIFIED,
        ]:
            tasks.append(Assignments.TAKE_SNAPSHOT)
            tasks.append(Assignments.GET_DIFF)
            tasks.append(Assignments.MARK_DIFFS_RED)
            tasks.append(Assignments.EXPORT_PROPOSAL)
            tasks.append(Assignments.SUBMISSION_EMAIL_TO_USER)
            tasks.append(Assignments.SUBMISSION_EMAIL_TO_CHAIRS)
            tasks.append(Assignments.SUBMISSION_EMAIL_TO_ADMINS)

        if status in [
            ChallengeStatus.CLEAN_PROPOSAL
        ]:
            tasks.append(Assignments.TAKE_SNAPSHOT)
            tasks.append(Assignments.EXPORT_PROPOSAL)
            tasks.append(Assignments.SUBMISSION_EMAIL_TO_USER)

        return tasks
