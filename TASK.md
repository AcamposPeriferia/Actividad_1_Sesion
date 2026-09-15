# Requerimiento de la actividad

El endpoint `POST /transfers` no debe permitir transferencias con un monto menor o igual a cero.

## Criterios de aceptación

1. Un monto `<= 0` debe devolver HTTP 400.
2. El mensaje de error debe ser claro.
3. El contrato actual del endpoint no debe cambiar para transferencias válidas.
4. La validación debe ubicarse en la capa que corresponda según la arquitectura existente.
5. Debe agregarse al menos una prueba automatizada para el nuevo comportamiento.
6. No deben modificarse archivos que no sean necesarios para resolver el requerimiento.

## Restricción para la dinámica

No implementes inmediatamente el cambio.

Primero explora el repositorio, identifica su estructura, pruebas, convenciones y riesgos. Después construye un `CLAUDE.md` que permita a una nueva sesión de Claude Code trabajar correctamente en este proyecto.
