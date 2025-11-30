from models import User, Salesman, Manager, Accountant, UserRole, Admin
from database import users
from enums import UserRole


class UserFactory:

    def create(new_id, username, name, email, password, role, manager_id = None):
        # new_id = len(users) + 1
        
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

        # users.append(user)
        return user
    

    