from pydantic import BaseModel


class TransferRequest(BaseModel):
    from_account: str
    to_account: str
    amount: float


class TransferResponse(BaseModel):
    message: str
    from_account: str
    to_account: str
    amount: float


class AccountResponse(BaseModel):
    account_id: str
    balance: float
