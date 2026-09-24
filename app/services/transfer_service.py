from app.repositories.account_repository import AccountRepository


class TransferError(Exception):
    pass


class TransferService:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def create_transfer(self, from_account: str, to_account: str, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Monto invalido: debe ser mayor a 0")

        if not self.repository.exists(from_account):
            raise TransferError("Origin account does not exist")

        if not self.repository.exists(to_account):
            raise TransferError("Destination account does not exist")

        if self.repository.get_balance(from_account) < amount:
            raise TransferError("Insufficient funds")

        self.repository.transfer(from_account, to_account, amount)
