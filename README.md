# Mini Bank API

Proyecto pequeño para practicar trabajo asistido con Claude Code.

## Qué hace

Expone una API mínima para consultar cuentas y realizar transferencias entre cuentas almacenadas en memoria.

## Instalación

```bash
python -m venv .venv
```

Windows:

```bash
.venv\\Scripts\\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecutar

```bash
uvicorn app.main:app --reload
```

Documentación interactiva:

- http://127.0.0.1:8000/docs

## Pruebas

```bash
pytest -q
```

## Nota

El proyecto está intencionalmente simplificado para una actividad de capacitación. No utiliza base de datos ni autenticación real.
