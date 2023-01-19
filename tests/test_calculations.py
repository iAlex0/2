import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount(0)

@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    assert add(num1, num2)  == expected

# @pytest.mark.parametrize("num1, num2, expected")
# def test_subtract(num1, num2, expected):
#     assert a - b == expected

# @pytest.mark.parametrize("num1, num2, expected")
# def test_multiply(num1, num2, expected):
#     assert a * b == expected

# @pytest.mark.parametrize("num1, num2, expected")
# def test_divide(num1, num2, expected):
#     assert a / b == expected

def test_bank_account(bank_account):
    assert bank_account.balance == 50
    
def test_bank_default(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account):
    bank_account.withdraw(5)
    assert bank_account.balance == 45

def test_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000)
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    # zero_bank_account.collect_interest()
    assert zero_bank_account.balance == expected

def test_insufficient_funds(zero_bank_account):
    with pytest.raises(InsufficientFunds):
        zero_bank_account.withdraw(1)