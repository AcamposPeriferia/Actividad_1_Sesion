from datetime import datetime
from typing import Any

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


class TransferRecordResponse(BaseModel):
    transfer_id: str
    from_account: str
    to_account: str
    amount: float
    created_at: datetime


class AccountResponse(BaseModel):
    account_id: str
    owner: str
    account_type: str
    balance: float


class AuditEventResponse(BaseModel):
    event_id: str
    event_type: str
    occurred_at: datetime
    details: dict[str, Any]
