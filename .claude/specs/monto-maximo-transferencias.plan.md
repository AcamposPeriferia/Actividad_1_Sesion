# Plan de ejecución: monto máximo por transferencia

- **Spec:** [monto-maximo-transferencias.md](monto-maximo-transferencias.md)
- **Estado:** propuesto, pendiente de aprobación (no hay nada implementado)
- **Fecha:** 2026-09-24

## Resumen

Hoy `POST /transfers` acepta montos arbitrariamente altos: una transferencia de 470.000.000 COP desde la cuenta corporativa ACC-003 se completa sin ningún tope. El cambio consiste en agregar un límite en la capa de servicio y cubrirlo con pruebas.

- **Alcance:** toca **2 archivos** y se hace en **3 waves** (Implementación, Pruebas y Verificación).
- **Front end y auditoría:** no hay que tocarlos. El front end ya muestra el `detail` de cualquier error 400, y la auditoría ya registra cualquier rechazo que produzca el servicio.

Hay una decisión que debe tomar el negocio antes de empezar: **el valor del monto máximo**. La spec no lo define, y es justo el riesgo que ella misma señala: ACC-003 y ACC-004 son clientes corporativos con saldos altos.

| Archivo | Cambio |
|---|---|
| [app/services/transfer_service.py](../../app/services/transfer_service.py) | Constante `MAX_TRANSFER_AMOUNT` y validación nueva en `_validate` |
| [tests/test_transfers.py](../../tests/test_transfers.py) | Pruebas de los casos de la spec (más una en `test_audit.py`, opcional) |

---

## Wave 0: Decisiones previas (bloquean el resto)

| # | Decisión | Propuesta | Responsable |
|---|---|---|---|
| D1 | Valor del monto máximo | Constante `MAX_TRANSFER_AMOUNT` con un valor provisional, que el negocio debe validar contra los saldos corporativos | Negocio |
| D2 | ¿Un monto igual al límite se acepta? | **Sí.** La spec solo rechaza montos "por encima" del límite | Negocio / Equipo |
| D3 | Texto del error | `"Monto invalido: excede el maximo permitido de {MAX}"`, en el mismo estilo que el error actual de monto `<= 0` | Equipo |
| D4 | Dónde queda el valor | Constante en el módulo del servicio. Leerlo de configuración, o tener un límite por canal o por tipo de cuenta, queda fuera de alcance | Equipo |

---

## Wave 1: Implementación

**Archivo que se toca:** [app/services/transfer_service.py](../../app/services/transfer_service.py)

- Agregar la constante `MAX_TRANSFER_AMOUNT` a nivel de módulo.
- Agregar en `TransferService._validate` la validación `amount > MAX_TRANSFER_AMOUNT` → `ValueError(...)`.
- Orden: **justo después** de la validación de `amount <= 0` y **antes** de revisar cuentas y saldo.

**Por qué en `_validate`**

- Ahí viven hoy todas las reglas de negocio de la transferencia.
- Todo lo que se lanza en `_validate` queda auditado automáticamente como `TRANSFER_REJECTED` por `create_transfer`, así que no hace falta tocar `app/audit/`.
- El endpoint ya convierte `ValueError` en HTTP 400 ([app/api/transfers.py](../../app/api/transfers.py)), así que el contrato no cambia.
- Si la validación quedara después de la de saldo, un monto excesivo respondería `"Insufficient funds"` en vez del error de límite.

**Archivos que no se tocan:**

| Archivo o carpeta | Por qué |
|---|---|
| `app/audit/` | Restricción de la spec |
| `app/api/`, `app/schemas.py` | El contrato no cambia |
| `app/repositories/`, `app/container.py`, `app/main.py` | No hacen falta |
| `frontend/` | Ya muestra el `detail` del error |

**Cómo se verifica**

- `git diff --stat` muestra un solo archivo modificado.
- `pytest -q` deja en verde las 16 pruebas actuales.

---

## Wave 2: Pruebas

**Archivo que se toca:** [tests/test_transfers.py](../../tests/test_transfers.py), usando el helper `transfer(client, ...)` y la fixture `client` que ya existen.

| Caso (según la spec) | Monto | Resultado esperado |
|---|---|---|
| Justo en el límite | `MAX` | HTTP 200 y los saldos cambian |
| Un peso por encima | `MAX + 1` | HTTP 400 con el mensaje de límite, los saldos **no** cambian y no aparece en `GET /transfers` |
| Monto negativo | `-50` | HTTP 400 con el mensaje de monto inválido (ya lo cubre `test_transfer_fails_when_amount_is_not_positive`) |
| Válida muy por debajo del límite | `100.000` | HTTP 200, igual que hoy (ya lo cubre `test_transfer_successfully`) |

**Opcional, en [tests/test_audit.py](../../tests/test_audit.py):** que `MAX + 1` genere un evento `TRANSFER_REJECTED` con el motivo del límite.

**Qué cuidar**

- **Saldo de prueba:** usar ACC-003 como origen, que tiene 480.000.000. Si `MAX + 1` supera ese saldo, darle a la cuenta un saldo mayor dentro de la propia prueba (`account_repository.get("ACC-003").balance = ...`). Si no, el caso "justo en el límite" fallaría por saldo insuficiente.
- **Sin números fijos:** importar `MAX_TRANSFER_AMOUNT` desde el servicio en lugar de escribir el valor a mano, para que las pruebas no se rompan si el negocio recalibra el límite.

**Cómo se verifica:** `pytest -v` deja en verde las 16 pruebas actuales y las nuevas.

---

## Wave 3: Verificación final

| Qué se revisa | Cómo |
|---|---|
| Arriba del máximo devuelve 400 con mensaje claro | `pytest -v`, más una prueba manual: `uvicorn app.main:app --reload`, abrir http://127.0.0.1:8000, transferir `MAX + 1` desde ACC-003 y confirmar que se ve el mensaje de error |
| Las transferencias válidas no cambian | `test_transfer_successfully` sigue en verde sin modificarse; en la UI, una transferencia pequeña sigue mostrando "Transferencia exitosa" |
| El rechazo queda auditado | En la tabla de Auditoría de la UI aparece un evento "Rechazada" con el motivo del límite |
| No se tocó nada fuera de alcance | `git diff --stat` solo muestra los archivos del plan; `app/audit/` y `frontend/` sin cambios |
| Riesgo de calibración del límite | El PR deja anotado el valor usado y que el negocio debe validarlo antes de salir a producción |

---

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Límite mal calibrado bloquea a clientes corporativos (ACC-003, ACC-004) | D1 la valida el negocio, y el valor queda en una sola constante fácil de ajustar |
| Error de límite tapado por el de saldo insuficiente | La validación va antes de revisar el saldo (Wave 1) |
| Tocar la auditoría por error | La validación va en `_validate`, que ya se audita sola; se verifica con `git diff --stat` |
| Imprecisión de `float` en el borde del límite | Probar exactamente `MAX` y `MAX + 1`, con valores enteros |
