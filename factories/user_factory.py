from models import Salesman, Manager, Accountant, Admin

class UserFactory:

    def create(new_id, username, name, email, password, role, manager_id = None):
        
        match role:
            case "SALESMAN":
                if manager_id is None:
                    raise ValueError(f"Salesman {username} needs to have a manager.")
                
                user = Salesman(new_id, username, name, email, password, manager_id)
            case "ACCOUNTANT":
                user = Accountant(new_id, username, name, email, password)
            case "MANAGER":
                user = Manager(new_id, username, name, email, password)
            case "ADMIN":
                user = Admin(new_id, username, name, email, password)

        return user
    

    