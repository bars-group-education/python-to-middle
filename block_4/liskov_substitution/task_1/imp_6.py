class Account:

    def __init__(self) -> None:
        super().__init__()
        self._balance = 0

    def deposit(self, amount):
        return self._balance

    def withdraw(self, amount):
        return self._balance


class WithdrawableAccount(Account):
    def withdraw(self, amount):
        self._balance -= amount

        return self._balance


class DepositableAccount(Account):
    def deposit(self, amount):
        self._balance += amount

        return self._balance


class DynamicAccount(WithdrawableAccount, DepositableAccount):
    pass


class SavingAccount(DynamicAccount):
    pass


class NonWithdrawableAccount(WithdrawableAccount):
    pass


BaseAccountClass = Account