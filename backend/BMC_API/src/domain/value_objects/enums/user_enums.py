### User ENUMS ###
### Adapted from old system ###

from enum import Enum


class Roles(str, Enum):
    ADMIN = "Admin"
    SUBADMIN = "SubAdmin"
    ORGANIZER = "Organizer"
    REVIEWER = "Reviewer"
    SUPERREVIEWER = "SuperReviewer"
    VIEWER = "Viewer"
