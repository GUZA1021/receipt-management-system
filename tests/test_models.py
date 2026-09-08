from models import Salesman, Manager, Accountant, Receipt
from enums import *

def test_user_can_bumit_salesman():
    user = Salesman(1, "salesman", "salesman", "salesman@live.dj", "salesman", manager_id = 1)  

    assert user.can_submit() is True

def test_salesman_view():
    user = Salesman(1, "salesman", "salesman", "salesman@live.dj", "salesman", manager_id = 1)  
    other_receipt = Receipt(1, 100, "img/path", submitter_id=2)
    own_receipt = Receipt(2, 2, "img/path", submitter_id=1)

    assert user.can_view(own_receipt) is True
    assert user.can_view(other_receipt) is False

def test_manager_not_approve_own_receipt():
    manager = Manager(1, "manager", "manager", "manager@live.dk", "manager")
    receipt = Receipt(1, 100, "img/path", submitter_id=1)
    receipt.status = ReceiptStatus.HANDLED

    assert manager.can_approve(receipt) is False

def test_manager_approve():
    manager = Manager(1, "manager", "manager", "manager@live.dk", "manager")
    receipt = Receipt(1, 100, "img/path", submitter_id=2)

    receipt.status = ReceiptStatus.HANDLED

    assert manager.can_approve(receipt) is True

def test_accountant_handle():
    accountant = Accountant(1, "accountant", "accountant", "accountant@live.dk", "accountant")
    receipt = Receipt(1, 100, "img/path", submitter_id=2)

    receipt.status = ReceiptStatus.PENDING
    assert accountant.can_handle(receipt) is True

    receipt.status = ReceiptStatus.APPROVED
    assert accountant.can_handle(receipt) is False


def test_add_event():
    receipt = Receipt(1, 100, "img/path", submitter_id=2)

    receipt.add_event("Handled")

    assert len(receipt.handling_log) == 1
    assert "Handled" in receipt.handling_log[0]