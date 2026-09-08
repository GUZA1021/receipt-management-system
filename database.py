from models import Manager, Salesman, Receipt, Accountant, Admin

users = [
    Manager(1,"manager","manager", "manager@live.dk", "manager"),
    Accountant(3, "accountant", "accountant", "accountantlive.dk", "accountant"),
    Salesman(2, "salesman", "salesman", "salesman@live.dk", "salesman", manager_id=1),
    Admin(4, "admin","admin","admin@live.dk", "admin")
]
receipts = []