from enums import ReceiptStatus
from datetime import datetime
from factories.receipt_factory import ReceiptFactory


class ReceiptApplication:
    """
    Application layer for working with receipts.
    Handles receipt creation and transitions between states of receipts
    """

    def __init__(self, receipts, users):
        self.repo = receipts
        self.users = users


    def get_receipt(self, receipt_id):
        """Return a receipt with a given id"""
        for x in self.repo:
            if x.id == receipt_id:
                return x
    
    def get_user_receipt(self, user_id):
        """Return all receipts submitted by user."""
        result = []
        for x in self.repo:
            if x.submitter_id == user_id:
                result.append(x)
        return result
    

    def get_by_status(self, status):
        """Return all receipts with a given status"""
        result = []
        for x in self.repo:
            if x.status == status:
                result.append(x)
        return result
    
    def get_all(self):
        """Return all receipts."""
        return self.repo


    def create_receipt(self, user_id, amount, image_path):
        receipt = ReceiptFactory.create(user_id, amount, image_path)
        self.repo.append(receipt)

        return receipt
    


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
