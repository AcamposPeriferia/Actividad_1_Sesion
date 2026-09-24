from fastapi import APIRouter

from app.container import audit_log
from app.schemas import AuditEventResponse

router = APIRouter(tags=["audit"])


@router.get("/audit-events", response_model=list[AuditEventResponse])
def list_audit_events():
    return [AuditEventResponse(**vars(event)) for event in audit_log.list_events()]
