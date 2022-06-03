#all testfile names should start wiht "test*" also function names inside files should also 
# cmd -  pytest -v to autodetect all tests and get result
# pytest -v -s to print any print statements in function
# 
import pytest

from testfunction import divide, BankAccount

@pytest.fixture
def zeroBank():
    return BankAccount()


# def test_add():
#     print("testing add")
#     assert 1==1
# @pytest.mark.parametrize("num1, num2, expected", [
#     (3,2,1),
#     (30,3,10),
#     (40,2,20)
# ])
# def test_divide(num1, num2, expected):
#     assert divide(num1, num2) == expected



def test_bank_set_initial_amount():
    b1 = BankAccount(50)
    b2 = BankAccount(200)
    b2.withdraw(20)
    b2.deposit(30)
    b2.collect_intrest()
    assert int(b2.balance) == 231
    