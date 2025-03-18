from enum import Enum


class BloodType(Enum):
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    AB = "AB"
    AD = "AD"


class Urgency(Enum):
    VERY_URGENT = "Very urgent"
    URGENT = "urgent"
    RESERVE = "reserve"


class UserRole(str, Enum):
    ADMIN = "admin"
    DONOR = "donor"
    REQUESTER = "requester"
    HOSPITAL_ADMIN = "hospital_admin"
    VOLUNTEER = "volunteer"


class HospitalType(str, Enum):
    PRIVATE = "private"
    PUBLIC = "public"


class HopitalStatus(str, Enum):
    SUSPENDED = "suspended"
    ACTIVE = "active"


class BloodType(Enum):
    O_POSITIVE = "O+"
    AB_POSITIVE = "AB+"


class RequestType(Enum):
    URGENT = 'urgent'
    NORMAL = "normal"


class RequestStatus(Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    EXPIRED = 'expired'

