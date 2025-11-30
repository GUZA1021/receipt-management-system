from datetime import datetime
from enums import ReceiptStatus, UserRole



class User:
    def __init__ (self, id, username, name, email, password, role):
        self.id = id
        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.role = role

   
    def __repr__(self):
        return f'<User id={self.id} username={self.username} role={self.role}>'
    
    def is_salesman(self):
        return self.role == UserRole.SALESMAN
    
    def is_accountant(self):
        return self.role == UserRole.ACCOUNTANT
    
    def is_manager(self):
        return self.role == UserRole.MANAGER
    
    def is_admin(self):
        return self.role == UserRole.ADMIN
    
    def can_manage_users(self):
        return self.is_admin()
    
    def can_view_logs(self):
        return self.is_admin()

    def can_view_all_receipts(self):
        return self.is_admin()

    def can_submit(self):
        return self.is_salesman() or self.is_manager()
    
    def can_handle(self, receipt):
        return self.is_accountant() and receipt.status == ReceiptStatus.PENDING
    
    def can_approve(self, receipt):
        if not self.is_manager():
            return False
        if receipt.submitter_id == self.id:
            return False
        return receipt.status == ReceiptStatus.HANDLED
    
    def can_reject(self, receipt):
        if not self.is_manager():
            return False
        if receipt.submitter_id == self.id:
            return False
        return receipt.status == ReceiptStatus.HANDLED
    
    def can_view(self, receipt):
        if self.is_salesman():
            return receipt.submitter_id == self.id
        
        if self.is_accountant() or self.is_manager():
            return True
        
        return False
    

class Manager(User):
    def __init__(self, id, username, name, email, password):
        super().__init__(id, username, name, email, password, UserRole.MANAGER)

class Accountant(User):
    def __init__(self, id, username, name, email, password):
        super().__init__(id, username, name, email, password, UserRole.ACCOUNTANT)


class Salesman(User):
    def __init__(self, id, username, name, email, password, manager_id):
        super().__init__(id, username, name, email, password, UserRole.SALESMAN)
        self.manager_id = manager_id

class Admin(User):
    def __init__(self, id, username, name, email, password):
        super().__init__(id, username, name, email, password, UserRole.ADMIN)


class Receipt:
    def __init__ (self, id, amount, image_path, submitter_id):
        self.id = id
        self.amount = amount
        self.image_path = image_path
        self.submitter_id = submitter_id

        self.date = datetime.now()


        self.status = ReceiptStatus.PENDING 

        self.handled_by_id = None
        self.approved_by_id = None
        self.rejected_by_id = None

        self.handling_log = []


    def add_event(self, message):
        self.handling_log.append(f"{datetime.now()}: {message}")
