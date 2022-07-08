class Account:

    def __init__(self) -> None:
        super().__init__()
        self._balance = 0

    def deposit(self, amount):
        raise NotImplementedError


class WithdrawableAccount(Account):

    def withdraw(self, amount):
        raise NotImplementedError


class DynamicAccount(WithdrawableAccount):

    def deposit(self, amount):
        self._balance += amount

        return self._balance

    def withdraw(self, amount):
        self._balance -= amount

        return self._balance


class SavingAccount(WithdrawableAccount):

    def deposit(self, amount):
        self._balance += amount

        return self._balance

    def withdraw(self, amount):
        self._balance -= amount

        return self._balance


class NonWithdrawableAccount(Account):

    def deposit(self, amount):
        self._balance += amount

        return self._balance


BaseAccountClass = WithdrawableAccount