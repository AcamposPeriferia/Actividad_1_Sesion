from fastapi import APIRouter, HTTPException

from app.container import account_repository
from app.schemas import AccountResponse

router = APIRouter(tags=["accounts"])


@router.get("/accounts", response_model=list[AccountResponse])
def list_accounts():
    return [AccountResponse(**vars(account)) for account in account_repository.list_accounts()]


@router.get("/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: str):
    account = account_repository.get(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    return AccountResponse(**vars(account))
