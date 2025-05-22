### CHALLENGE ENUMS ###
from enum import StrEnum


class ChallengeStatus(StrEnum):
    # 1. Initial submission statuses
    DRAFT = "Draft"
    DRAFT_UPDATED = "DraftUpdated"
    DRAFT_SUBMITTED = "DraftSubmitted"

    # 2. Revision statuses
    MINOR_REVISION_REQUIRED = "MinorRevisionRequired"
    MAJOR_REVISION_REQUIRED = "MajorRevisionRequired"
    REVISION_UPDATED = "RevisionUpdated"
    REVISION_SUBMITTED = "RevisionSubmitted"

    # 3. Final statuses for first and second submissions
    # These can only attend by admins
    # If further modification is necessary, only admins can change from these to another status

    # 3.1 Preliminary accepted statuses
    PRELIM_ACCEPT_AS_STANDARD_CHALLENGE = "PrelimAcceptAsStandardChallenge"
    PRELIM_ACCEPT_AS_LIGHTHOUSE_CHALLENGE = "PrelimAcceptAsLighthouseChallenge"
    REVISION_UPDATED_PRELIM_ACCEPT = "RevisionUpdatedPrelimAccept"
    REVISION_SUBMITTED_PRELIM_ACCEPT = "RevisionSubmittedPrelimAccept"

    # 3.2 After acceptance, statuses for further modifications
    ACCEPTED_MODIFIED_DRAFT = "AcceptedModifiedDraft"
    ACCEPTED_MODIFIED_UPDATED = "AcceptedModifiedUpdated"
    ACCEPTED_MODIFIED_SUBMITTED = "AcceptedModifiedSubmitted"

    # 3.3 Final statuses, no update of proposals allowed after this
    LOCKED = "Locked"
    ACCEPT = "Accept"
    REJECT = "Reject"
    ACCEPT_AS_LIGHTHOUSE_CHALLENGE = "AcceptAsLighthouseChallenge"
    ACCEPT_AS_STANDARD_CHALLENGE = "AcceptAsStandardChallenge"
    ACCEPTED_MODIFIED = "AcceptedModified"

    # 4. Special status if non-marked version of proposal document is necessary
    CLEAN_PROPOSAL = "CleanProposal"

    # 
    # RevisionOfSubmittedNewParameters = "RevisionOfSubmittedNewParameters"
    # Deleted = "Deleted"


### ENUMS Adapted from old system, these are not used in backend anymore. They are controlled from frontend code ###

# class LifecycleType(str, Enum):
#     OneTimeEvent = "OneTimeEvent"
#     OpenCall = "OpenCall"
#     RepeatedEventOneTime = "RepeatedEventOneTime"
#     RepeatedEventOpenCall = "RepeatedEventOpenCall"
#     Other = "Other"


# class Duration(str, Enum):
#     FullDay = "FullDay"
#     HalfDay = "HalfDay"
#     Other = "Other"

# class ReviewerStatus(str, Enum):
#     AcceptAsIs = "Accept - as is"
#     AcceptRevisionRequiredLater = "Accept - revision required later"
#     MinorRevisionRequired = "Minor revision required"
#     MajorRevisionRequired = "Major revision required"
#     Reject = "Reject"


# class SuperReviewerStatus(str, Enum):
#     StrongAccept = "StrongAccept"
#     WeakAccept = "WeakAccept"
#     StrongReject = "StrongReject"
#     WeakReject = "WeakReject"
#     RevisionRequired = "RevisionRequired"


# class SubmissionInstructions(str, Enum):
#     NoInstructions = "NoInstructions"
#     FormatOfInstructions = "FormatOfInstructions"
#     LicenceRequirements = "LicenceRequirements"
#     MissingCasesAllowence = "MissingCasesAllowence"
#     NumberOfResubmissionsAllowed = "NumberOfResubmissionsAllowed"
#     NumberOfDifferentSubmissionsPerParticipantsAllowed = (
#         "NumberOfDifferentSubmissionsPerParticipantsAllowed"
#     )
#     Timeline = "Timeline"


# class EvaluationSoftware(str, Enum):
#     NotAvailable = "NotAvailable"
#     AvailableAfterRegistration = "AvailableAfterRegistration"
#     PartiallyAvailable = "PartiallyAvailable"
#     PubliclyAvailable = "PubliclyAvailable"
#     Other = "Other"


# class PreEvaluationMethod(str, Enum):
#     NoPreEvaluation = "NoPreEvaluation"
#     PrivateResults = "PrivateResults"
#     PublicLeaderboard = "PublicLeaderboard"
#     ResultsOnTrainingData = "ResultsOnTrainingData"
#     ResultsOnValidationDataset = "ResultsOnValidationDataset"
#     Other = "Other"


# class EthicalApproval(str, Enum):
#     No_Ethics_Needed = "No_Ethics_Needed"
#     Approving_Entity = "Approving_Entity"
#     URL_To_Approval_Document = "URL_To_Approval_Document"
#     Other = "Other"


# class ChallengeVenue(str, Enum):
#     AAPM = "AAPM"
#     BII = "BII"
#     CLEF = "CLEF"
#     DREAM = "DREAM"
#     HHMI = "HHMI"
#     ICPR = "ICPR"
#     ImageCLEF = "ImageCLEF"
#     ISBI = "ISBI"
#     ISMRM = "ISMRM"
#     Kaggle = "Kaggle"
#     MICCAI = "MICCAI"
#     SHAPE_SYMPOSIUM = "SHAPE_SYMPOSIUM"
#     SMLMS = "SMLMS"
#     SPIE = "SPIE"


# class Publication(str, Enum):
#     NoPublication = "NoPublication"
#     Arxiv = "Arxiv"
#     Bioinformatics = "Bioinformatics"
#     Bioxiv = "Bioxiv"
#     CEUR = "CEUR"
#     ComputerizedMedicalImagingAndGraphics = "ComputerizedMedicalImagingAndGraphics"
#     ConferenceProceedings = "ConferenceProceedings"
#     FrontiersInNeuroanatomy = "FrontiersInNeuroanatomy"
#     IEEETransactionsOnMedicalImaging = "IEEETransactionsOnMedicalImaging"
#     IEEEConferenceOnComputerVisionAndPatternRecognition = (
#         "IEEEConferenceOnComputerVisionAndPatternRecognition"
#     )
#     IEEEJournalOfBiomedicalAndHealthInformatics = (
#         "IEEEJournalOfBiomedicalAndHealthInformatics"
#     )
#     InternationalJournalOfComputerAssistedRadiologyAndSurgery = (
#         "InternationalJournalOfComputerAssistedRadiologyAndSurgery"
#     )
#     InternationalJournalOfRadiationOncologyBiologyPhysics = (
#         "InternationalJournalOfRadiationOncologyBiologyPhysics"
#     )
#     JournalOfMedicalImaging = "JournalOfMedicalImaging"
#     JournalOfNeuroimaging = "JournalOfNeuroimaging"
#     JournalOfOphthalmology = "JournalOfOphthalmology"
#     MedicalImageAnalysis = "MedicalImageAnalysis"
#     MedicalPhysics = "MedicalPhysics"
#     MidasJournal = "MidasJournal"
#     Nature = "Nature"
#     NatureBiomedicalEngineering = "NatureBiomedicalEngineering"
#     NatureBiotechnology = "NatureBiotechnology"
#     NatureCommunications = "NatureCommunications"
#     NatureMethods = "NatureMethods"
#     NeuroImage = "NeuroImage"
#     NMRInBiomedicine = "NMRInBiomedicine"
#     PatternRecognitionLetters = "PatternRecognitionLetters"
#     PhysicsInMedicineAndBiology = "PhysicsInMedicineAndBiology"
#     Science = "Science"
#     ScientificReports = "ScientificReports"
#     Other = "Other"


# class DataUsageAgreement(str, Enum):
#     NoRedistribution = "NoRedistribution"
#     RedistributionForAllPurposes = "RedistributionForAllPurposes"
#     URLToDataUsageAgreement = "URLToDataUsageAgreement"
#     Other = "Other"
