from factories.user_factory import UserFactory

class UserApplication:

    def __init__(self, users):
        self.repo = users

    def get_all_users(self):
        return self.repo

    def validate_user(self, username, password):
        users = [x for x in self.repo if x is not None]

        for user in users:
            if user.username == username and user.password == password:
                return user

    def get_user(self, user_id):
        for x in self.repo:
            if x.id == user_id:
                return x
    
    def create_user(self, username, name, email, password, role, manager_id=None):
        new_id = len(self.repo) + 1
        user = UserFactory.create(new_id, username, name, email, password, role, manager_id)
        self.repo.append(user)
        return user
                