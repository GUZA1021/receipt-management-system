from application.user_application import UserApplication
from models import Manager

def test_create_user():
    users = []
    app = UserApplication(users)

    new_user = app.create_user(username="test_user", name="Test User", 
                               email="test_user@live.dk", password="testuser", role="MANAGER")

    assert new_user in users
    assert new_user.username == "test_user"

def test_validate_user():
    manager = Manager(1, "test_user", "Test User", "test_user@live.dk", "testuser")
    
    users = [manager]
    app = UserApplication(users)

    assert app.validate_user("test_user", "testuser") is manager

def test_validate_wrong_user():
    manager = Manager(1, "test_user", "Test User", "test_user@live.dk", "testuser")
    
    users = [manager]
    app = UserApplication(users)

    assert app.validate_user("test_user", "usertest")  is None
    assert app.validate_user("usertest", "testuser") is None
