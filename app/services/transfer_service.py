from app.audit.audit_log import TRANSFER_COMPLETED, TRANSFER_REJECTED, AuditLog
from app.repositories.account_repository import AccountRepository
from app.repositories.transfer_repository import Transfer, TransferRepository


class TransferError(Exception):
    pass


class TransferService:
    def __init__(
        self,
        repository: AccountRepository,
        transfers: TransferRepository,
        audit_log: AuditLog,
    ):
        self.repository = repository
        self.transfers = transfers
        self.audit_log = audit_log

    def create_transfer(self, from_account: str, to_account: str, amount: float) -> Transfer:
        try:
            self._validate(from_account, to_account, amount)
        except (TransferError, ValueError) as exc:
            self.audit_log.record(
                TRANSFER_REJECTED,
                from_account=from_account,
                to_account=to_account,
                amount=amount,
                reason=str(exc),
            )
            raise

        self.repository.transfer(from_account, to_account, amount)
        transfer = self.transfers.add(from_account, to_account, amount)
        self.audit_log.record(
            TRANSFER_COMPLETED,
            transfer_id=transfer.transfer_id,
            from_account=from_account,
            to_account=to_account,
            amount=amount,
        )
        return transfer

    def _validate(self, from_account: str, to_account: str, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Monto invalido: debe ser mayor a 0")

        if from_account == to_account:
            raise TransferError("Origin and destination accounts must be different")

        if not self.repository.exists(from_account):
            raise TransferError("Origin account does not exist")

        if not self.repository.exists(to_account):
            raise TransferError("Destination account does not exist")

        if self.repository.get_balance(from_account) < amount:
            raise TransferError("Insufficient funds")
