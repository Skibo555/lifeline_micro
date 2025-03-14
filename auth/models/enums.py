from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    DONOR = "donor"
    REQUESTER = "requester"
    HOSPITAL_ADMIN = "hospital_admin"
    VOLUNTEER = "volunteer"


class HospitalType(str, Enum):
    PRIVATE = "private"
    PUBLIC = "public"


class HospitalStatus(str, Enum):
    SUSPENDED = "suspended"
    ACTIVE = "active"

