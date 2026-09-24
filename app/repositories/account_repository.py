from dataclasses import dataclass, replace


@dataclass
class Account:
    account_id: str
    owner: str
    account_type: str  # "PERSONAL" | "CORPORATIVA"
    balance: float


# Datos semilla (COP). Incluye clientes corporativos con saldos altos.
SEED_ACCOUNTS = (
    Account("ACC-001", "Laura Gómez", "PERSONAL", 3_500_000.0),
    Account("ACC-002", "Carlos Rincón", "PERSONAL", 850_000.0),
    Account("ACC-003", "Distribuidora Andina S.A.S.", "CORPORATIVA", 480_000_000.0),
    Account("ACC-004", "Tienda La Esquina", "CORPORATIVA", 12_000_000.0),
)


class AccountRepository:
    """Repositorio en memoria para mantener el ejemplo simple."""

    def __init__(self):
        self.reset()

    def reset(self) -> None:
        self._accounts = {account.account_id: replace(account) for account in SEED_ACCOUNTS}

    def list_accounts(self) -> list[Account]:
        return list(self._accounts.values())

    def get(self, account_id: str) -> Account | None:
        return self._accounts.get(account_id)

    def exists(self, account_id: str) -> bool:
        return account_id in self._accounts

    def get_balance(self, account_id: str) -> float:
        return self._accounts[account_id].balance

    def transfer(self, from_account: str, to_account: str, amount: float) -> None:
        self._accounts[from_account].balance -= amount
        self._accounts[to_account].balance += amount
