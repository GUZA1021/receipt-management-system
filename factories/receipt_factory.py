from models import User, Salesman, Accountant, UserRole, Receipt
from enums import ReceiptStatus
from database import receipts

class ReceiptFactory:
    def create(user_id, amount, image_path):
        if amount <= 0:
            raise ValueError("The amount should be more than 0")
        
        new_id = len(receipts) + 1
        receipt = Receipt(new_id, amount, image_path, user_id)
        receipts.append(receipt)
        
        return receipt
