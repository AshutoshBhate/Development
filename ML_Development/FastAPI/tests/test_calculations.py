import pytest
from app.calculations import add, multiply, subtract, divide, BankAccount, InsufficientFunds

#Fixture is a function that runs before a specific test case
@pytest.fixture
def zero_bank_account():
    print("Creating empty bank account")
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

########################################################################################################

# def test_add():
#     addition = add(7, 5)
#     print("Testing the addition functionality")
    
#     assert addition == 12

#Now test_add which is parametrized :

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print("Testing the add functionality")
    assert add(num1, num2) == expected
    
def test_multiply():
    multiplication = multiply(8, 9)
    print("Testing the multiplication functionality")
    
    assert multiplication == 72
    
def test_subtract():
    subtraction = subtract(7, 5)
    print("Testing the subtraction functionality")
    
    assert subtraction == 2
    
def test_divide():
    division = divide(5, 5)
    print("Testing the division functionality")
    
    assert division == 1
    
#######################################################################################################
    
def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50
    
def test_bank_default_amount(zero_bank_account):
    print("Testing my bank account")
    assert zero_bank_account.balance == 0
    
def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30
    
def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80
    
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
    assert zero_bank_account.balance == expected
    
def test_insufficient_funds(zero_bank_account):
    with pytest.raises(InsufficientFunds):
        zero_bank_account.withdraw(60)
    