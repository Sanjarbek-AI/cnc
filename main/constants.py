from enum import Enum


class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class CompetitionStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class ContactStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class InformationStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class ShowroomStatus(str, Enum):
    active = "active"
    inactive = "inactive"
