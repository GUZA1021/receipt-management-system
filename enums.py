from enum import Enum

class ReceiptStatus(Enum):
    PENDING = "PENDING"
    HANDLED = "HANDLED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class UserRole(Enum):
    SALESMAN = "SALESMAN"
    ACCOUNTANT = "ACCOUNTANT"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"