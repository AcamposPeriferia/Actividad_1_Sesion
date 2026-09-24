from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class Transfer:
    transfer_id: str
    from_account: str
    to_account: str
    amount: float
    created_at: datetime


class TransferRepository:
    """Historial en memoria de transferencias completadas."""

    def __init__(self):
        self.clear()

    def clear(self) -> None:
        self._transfers: list[Transfer] = []

    def add(self, from_account: str, to_account: str, amount: float) -> Transfer:
        transfer = Transfer(
            transfer_id=f"TRF-{len(self._transfers) + 1:05d}",
            from_account=from_account,
            to_account=to_account,
            amount=amount,
            created_at=datetime.now(timezone.utc),
        )
        self._transfers.append(transfer)
        return transfer

    def list_transfers(self) -> list[Transfer]:
        return list(reversed(self._transfers))
