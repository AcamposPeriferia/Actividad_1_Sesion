class AccountRepository:
    """Repositorio en memoria para mantener el ejemplo simple."""

    def __init__(self):
        self._accounts = {
            "ACC-001": 1000.0,
            "ACC-002": 500.0,
            "ACC-003": 200.0,
        }

    def exists(self, account_id: str) -> bool:
        return account_id in self._accounts

    def get_balance(self, account_id: str) -> float:
        return self._accounts[account_id]

    def transfer(self, from_account: str, to_account: str, amount: float) -> None:
        self._accounts[from_account] -= amount
        self._accounts[to_account] += amount
