# Mini Bank

Banca en línea de práctica para trabajar con Claude Code a partir de specs.
Tiene una **API REST en FastAPI** y un **front end nativo** (HTML, CSS y JavaScript con ES modules; sin frameworks ni build). La API sirve el front end, así que ambos corren en el mismo origen.

## Qué hace

- Consulta cuentas personales y corporativas, con saldos en COP.
- Hace transferencias entre cuentas, con validaciones de negocio.
- Guarda el historial de transferencias completadas.
- Audita cada intento de transferencia, aceptado o rechazado.

Todo el estado vive en memoria y se reinicia al reiniciar el servidor. No hay base de datos ni autenticación.

## Arquitectura

```
frontend/            Front end nativo (lo sirve la API en /app)
  index.html
  css/styles.css
  js/api.js          Cliente HTTP (fetch) y manejo de errores de la API
  js/app.js          Render y eventos de la UI
app/
  main.py            App FastAPI: routers, /health y montaje del front
  container.py       Instancias compartidas y reset_state() para las pruebas
  schemas.py         Contratos de entrada y salida (Pydantic)
  api/               Capa HTTP: accounts, transfers, audit
  services/          Reglas de negocio (TransferService)
  repositories/      Datos en memoria: cuentas y transferencias
  audit/             Módulo de auditoría (sensible, ver abajo)
tests/               Pruebas con pytest y TestClient
.claude/specs/       Specs y planes de ejecución
```

**Flujo de una transferencia:** `frontend` → `POST /transfers` → `api/transfers.py` → `TransferService._validate` → repositorios → `audit_log.record(...)`.

**Errores:**
- El servicio lanza `ValueError` o `TransferError`.
- La API los convierte en HTTP 400 con `detail`.
- El front end muestra ese `detail` tal cual al usuario.

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Estado de la API |
| GET | `/accounts` | Lista de cuentas |
| GET | `/accounts/{id}` | Detalle de una cuenta (404 si no existe) |
| POST | `/transfers` | Crea una transferencia (400 si no pasa las validaciones) |
| GET | `/transfers` | Historial, de la más reciente a la más antigua |
| GET | `/audit-events` | Eventos de auditoría, del más reciente al más antiguo |

El contrato de `POST /transfers` para transferencias válidas es `{message, from_account, to_account, amount}`. No debe cambiar.

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux/macOS
pip install -r requirements.txt
```

## Ejecutar

```bash
uvicorn app.main:app --reload
```

- Front end: http://127.0.0.1:8000/ (redirige a `/app/`)
- Documentación de la API: http://127.0.0.1:8000/docs

## Pruebas

```bash
pytest -q
```

`tests/conftest.py` restablece los datos semilla antes de cada prueba y expone la fixture `client`.

## Datos semilla

| Cuenta | Titular | Tipo | Saldo (COP) |
|---|---|---|---|
| ACC-001 | Laura Gómez | PERSONAL | 3.500.000 |
| ACC-002 | Carlos Rincón | PERSONAL | 850.000 |
| ACC-003 | Distribuidora Andina S.A.S. | CORPORATIVA | 480.000.000 |
| ACC-004 | Tienda La Esquina | CORPORATIVA | 12.000.000 |

## Zonas sensibles

- **`app/audit/`:** trazabilidad regulatoria. Los demás módulos solo llaman a `record`. Cualquier cambio en este módulo requiere aprobación de Cumplimiento.
- **Contrato de `POST /transfers`:** lo consume el front end, así que hay que mantenerlo compatible.

## Siguiente paso

Implementar la spec [monto-maximo-transferencias](.claude/specs/monto-maximo-transferencias.md) siguiendo su [plan](.claude/specs/monto-maximo-transferencias.plan.md). Hoy la API acepta transferencias de cualquier monto; por ejemplo, 470.000.000 COP desde ACC-003.
