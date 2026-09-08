from application.receipt_application import ReceiptApplication
from enums import ReceiptStatus

def test_create_receipt():
    receipts = []
    users = []
    app = ReceiptApplication(receipts, users)

    receipt = app.create_receipt(user_id=1, amount=100, image_path="img/path")

    assert receipt.submitter_id == 1
    assert receipt.amount == 100
    assert receipt.image_path == "img/path"
    assert receipt in receipts

def test_handle():
    receipts = []
    users = []
    app = ReceiptApplication(receipts, users)

    receipt = app.create_receipt(user_id=1, amount=100, image_path="img/path")

    app.handle(receipt_id=receipt.id, accountant_id=2)

    assert receipt.status == ReceiptStatus.HANDLED
    assert receipt.handled_by_id == 2

def test_reject():
    receipts = []
    users = []
    app = ReceiptApplication(receipts, users)

    receipt = app.create_receipt(user_id=1, amount=100, image_path="img/path")
    receipt.status = ReceiptStatus.HANDLED

    app.reject(receipt_id=receipt.id, manager_id=2)

    assert receipt.status == ReceiptStatus.REJECTED
    assert receipt.rejected_by_id == 2

def test_approve():
    receipts = []
    users = []
    app = ReceiptApplication(receipts, users)

    receipt = app.create_receipt(user_id=1, amount=100, image_path="img/path")
    receipt.status = ReceiptStatus.HANDLED

    app.approve(receipt_id=receipt.id, manager_id=2)

    assert receipt.status == ReceiptStatus.APPROVED
    assert receipt.approved_by_id == 2


def test_get_all_receipts():
    receipts = []
    users = []
    app = ReceiptApplication(receipts, users)

    receipt_1 = app.create_receipt(user_id=1, amount=100, image_path="img/path1")
    receipt_2 = app.create_receipt(user_id=2, amount=200, image_path="img/path2")

    all_receipts = app.get_all()

    assert len(all_receipts) == 2
    assert receipt_1 in all_receipts
    assert receipt_2 in all_receipts

