from enum import Enum


class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class CompetitionStatus(str, Enum):
    active = "active"
    stopped = "stopped"
    deleted = "deleted"


class ContactStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class ShowroomStatus(str, Enum):
    active = "active"
    inactive = "inactive"


class ShowroomType(str, Enum):
    showroom = "showroom"
    dealer = "dealer"


class UserPostStatus(str, Enum):
    accepted = "accepted"
    unaccepted = "unaccepted"
    disactive = "disactive"
    deleted = "deleted"
