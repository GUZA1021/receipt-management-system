from enums import ReceiptStatus
from datetime import datetime
from factories.receipt_factory import ReceiptFactory


class ReceiptApplication:

    def __init__(self, receipts, users):
        self.repo = receipts
        self.users = users

    # def get_user(self, user_id):
    #     """Find user by id"""
    #     for x in self.users:
    #         if x.id == user_id:
    #             return x


    def get_receipt(self, receipt_id):
        """Finds the receipt with the id"""
        for x in self.repo:
            if x.id == receipt_id:
                return x
    
    def get_user_receipt(self, user_id):
        """Findes all receipts from user"""
        result = []
        for x in self.repo:
            if x.submitter_id == user_id:
                result.append(x)
        return result
    

    def get_by_status(self, status):
        result = []
        for x in self.repo:
            if x.status == status:
                result.append(x)
        return result


    def create_receipt(self, user_id, amount, image_path):
        receipt = ReceiptFactory.create(user_id, amount, image_path)
        return receipt
    
    def get_all(self):
        return self.repo

    def handle(self, receipt_id, accountant_id):
        receipt = self.get_receipt(receipt_id)

        if receipt is None:
            raise ValueError("Receipt not found")
        
        if receipt.status != ReceiptStatus.PENDING:
            raise ValueError("Only PENDING receipts")
        
        receipt.status = ReceiptStatus.HANDLED
        receipt.handled_by_id = accountant_id
        self.add_event(receipt, f"Handled by {accountant_id}")
        return receipt

    def approve(self, receipt_id, manager_id):

        receipt = self.get_receipt(receipt_id)

        if receipt.status != ReceiptStatus.HANDLED: #Rejected receipt isn't handled again
            raise ValueError("Cannot approve receipt that is not handled yet")
        
        if receipt.submitter_id == manager_id:
            raise ValueError("FRAUD PREVENTION! Manager cannot approve own receipt")
        
        receipt.status = ReceiptStatus.APPROVED
        receipt.approved_by_id = manager_id
        self.add_event(receipt, f"Approved by {manager_id}")

        return receipt

    def reject(self, receipt_id, manager_id):   
        receipt = self.get_receipt(receipt_id)

        if receipt is None:
            raise ValueError("Receipt not found")

        if receipt.status != ReceiptStatus.HANDLED:
            raise ValueError("Cannot reject receipt that is not handled yet")

        if receipt.submitter_id == manager_id:
            raise ValueError("Managers cannot reject their own receipts")

        receipt.status = ReceiptStatus.REJECTED
        receipt.rejected_by_id = manager_id
        self.add_event(receipt, f"Rejected by {manager_id}")

        return receipt

    def add_event(self, receipt, message):
        receipt.handling_log.append(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}: {message}")
