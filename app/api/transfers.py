from fastapi import APIRouter, HTTPException

from app.repositories.account_repository import AccountRepository
from app.schemas import AccountResponse, TransferRequest, TransferResponse
from app.services.transfer_service import TransferError, TransferService

router = APIRouter()
repository = AccountRepository()
service = TransferService(repository)


@router.get("/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: str):
    if not repository.exists(account_id):
        raise HTTPException(status_code=404, detail="Account not found")

    return AccountResponse(
        account_id=account_id,
        balance=repository.get_balance(account_id),
    )


@router.post("/transfers", response_model=TransferResponse)
def create_transfer(request: TransferRequest):
    try:
        service.create_transfer(
            from_account=request.from_account,
            to_account=request.to_account,
            amount=request.amount,
        )
    except TransferError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return TransferResponse(
        message="Transfer completed",
        from_account=request.from_account,
        to_account=request.to_account,
        amount=request.amount,
    )
