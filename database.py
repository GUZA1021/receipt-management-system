from models import Manager, Salesman, Receipt, Accountant, Admin

users = [
    Manager(1,"amin","amin", "amin@h.dk", "amin"),
    Accountant(3, "karim", "karim", "karim@h.dk", "karim"),
    Salesman(2, "martin", "martin", "martin@h.dk", "martin", manager_id=1),
    Admin(4, "admin","admin","admin@lvie.dk", "admin")
]
receipts = [Receipt(1, 199.50, "/static/example1.png", submitter_id=2)]