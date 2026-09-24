"""Módulo de auditoría.

Registra cada intento de transferencia, aceptado o rechazado, para trazabilidad
regulatoria. Es un módulo sensible: cambios aquí requieren aprobación de
Cumplimiento. Los demás módulos solo deben llamar a `record`.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

TRANSFER_COMPLETED = "TRANSFER_COMPLETED"
TRANSFER_REJECTED = "TRANSFER_REJECTED"


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    event_type: str
    occurred_at: datetime
    details: dict[str, Any] = field(default_factory=dict)


class AuditLog:
    """Registro en memoria, solo de escritura hacia adelante."""

    def __init__(self):
        self.clear()

    def clear(self) -> None:
        self._events: list[AuditEvent] = []

    def record(self, event_type: str, **details: Any) -> AuditEvent:
        event = AuditEvent(
            event_id=f"EVT-{len(self._events) + 1:05d}",
            event_type=event_type,
            occurred_at=datetime.now(timezone.utc),
            details=dict(details),
        )
        self._events.append(event)
        return event

    def list_events(self) -> list[AuditEvent]:
        return list(reversed(self._events))
