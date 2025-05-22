from pydantic import ConfigDict

from .base_model import NoExtraBaseModel


class TaskModelBase(NoExtraBaseModel):
    """DTO for task base model."""

    task_name: str
    task_abstract: str | None = None
    task_acquisition_devices: str | None = None
    task_acquisition_protocol: str | None = None
    task_algorithm_target: str | None = None
    task_annoation_instructions: str | None = None
    task_annotation_aggregation: str | None = None
    task_annotators: str | None = None
    task_assesment_aim: str | None = None
    task_author_emails: str | list | None = None
    task_author_names: list[str] | None = None
    task_award_policy: str | None = None
    task_case_definition: str | None = None
    task_center: str | None = None
    task_challenge_cohort: str | None = None
    # task_challenge_schedule: str | None = None
    task_characteristic_data: str | None = None
    task_code_availability_organizers: str | None = None
    task_code_availability_participants: str | None = None
    task_conference_name: str | None = None
    task_conflict_of_interest: str | None = None
    task_contact_person: str | None = None
    task_contex_information_data: str | None = None
    task_contex_information_patient: str | None = None
    task_data_origin: str | None = None
    # task_data_usage_agreement_comments: str | None = None
    task_ethics_approval: str | None = None
    task_evaluation_metrics: str | None = None
    task_explanation_number_proportion_data: str | None = None
    task_field_of_application: str | None = None
    task_further_analyses: str | None = None
    task_imaging_modalities: str | None = None
    # task_interaction_level_list: str | None = None
    task_interaction_level_policy: str | None = None
    task_justification_of_data_characteristics: str | None = None
    task_justification_of_metrics: str | None = None
    task_justification_of_rank_computation_method: str | None = None
    task_justification_of_statistical_analyses: str | None = None
    task_keywords: list | str | None = None
    task_licence: str | None = None
    task_lifecycle: str | None = None
    task_metod_reference: str | None = None
    task_missing_data: str | None = None
    task_new_data: str | None = None
    task_number_of_cases: str | None = None
    # task_operators: str | None = None
    task_organizer_participation_policy: str | None = None
    task_organizing_team: str | None = None
    # task_participation_policy: str | None = None
    task_platform: str | None = None
    task_pre_evaluation: str | None = None
    task_pre_processing_methods: str | None = None
    task_pulication_policy: str | None = None
    task_rank_computation_method: str | None = None
    task_results_announcement: str | None = None
    task_result_submission_method: str | None = None
    task_schedule: str | None = None
    task_sources_of_error_images: str | None = None
    task_sources_of_error_other: str | None = None
    task_statistical_analyses: str | None = None
    # task_submission_instructions: str | None = None
    task_target_cohort: str | None = None
    task_task_category: str | None = None
    task_training_data_policy: str | None = None
    task_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


# class TaskInDB(TaskModelBase):
#     """
#     Internal model representing a task stored in the database.
#     This model  is used only for internal operations.
#     """

#     version: int | None = None
#     task_challenge_id: int | None = None
#     task_challenge: Any | None = None
#     task_locked: bool | None = None
#     task_owner_id: int | None = None
#     task_owner: Any | None = None
