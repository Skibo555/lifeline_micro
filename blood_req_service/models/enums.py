from enum import Enum


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


class BloodType(Enum):
    O_POSITIVE = "O+"
    AB_POSITIVE = "AB+"


class UserRole(str, Enum):
    ADMIN = "admin"
    DONOR = "donor"
    REQUESTER = "requester"
    HOSPITAL_ADMIN = "hospital_admin"
    VOLUNTEER = "volunteer"
