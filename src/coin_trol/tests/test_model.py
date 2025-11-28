from model.db_interface.py import *

def test_create_user():
    uid = create_user("TestUser", "test@user.com")
    assert uid is not None

def test_create_wallet_and_transaction():
    uid = create_user("Tester", "tester@coin.com")
    wid = create_wallet(uid, "TestWallet", 100.0)
    assert wid is not None
    add_transaction(wid, -10, "Food", "Pizza")
    balance = calculate_wallet_balance(wid)
    assert isinstance(balance, float)

def test_delete_transaction():
    uid = create_user("DelUser", "delete@coin.com")
    wid = create_wallet(uid, "DelWallet", 100.0)
    tid = add_transaction(wid, -5, "DeleteTest", "Temp")
    assert delete_transaction(tid)
