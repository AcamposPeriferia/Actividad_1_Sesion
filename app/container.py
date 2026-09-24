"""Instancias compartidas de la aplicación (estado en memoria)."""

from app.audit.audit_log import AuditLog
from app.repositories.account_repository import AccountRepository
from app.repositories.transfer_repository import TransferRepository
from app.services.transfer_service import TransferService

account_repository = AccountRepository()
transfer_repository = TransferRepository()
audit_log = AuditLog()
transfer_service = TransferService(account_repository, transfer_repository, audit_log)


def reset_state() -> None:
    """Vuelve a los datos semilla. Lo usan las pruebas."""
    account_repository.reset()
    transfer_repository.clear()
    audit_log.clear()
