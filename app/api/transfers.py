from fastapi import APIRouter, HTTPException

from app.container import transfer_repository, transfer_service
from app.schemas import TransferRecordResponse, TransferRequest, TransferResponse
from app.services.transfer_service import TransferError

router = APIRouter(tags=["transfers"])


@router.post("/transfers", response_model=TransferResponse)
def create_transfer(request: TransferRequest):
    try:
        transfer_service.create_transfer(
            from_account=request.from_account,
            to_account=request.to_account,
            amount=request.amount,
        )
    except (TransferError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return TransferResponse(
        message="Transfer completed",
        from_account=request.from_account,
        to_account=request.to_account,
        amount=request.amount,
    )


@router.get("/transfers", response_model=list[TransferRecordResponse])
def list_transfers():
    return [TransferRecordResponse(**vars(t)) for t in transfer_repository.list_transfers()]
