1. Problema
¿Qué puede pasar hoy que no debería? hoy el sistema permite transferencias por un monto arbitrariamente alto, sin ningún tope de validación.
2. Alcance (dentro / fuera)
¿Qué se toca y qué NO se toca? Dentro: la validación en el endpoint de transferencias. Fuera: cambios al límite por canal, autenticación, o el flujo de aprobación manual.
3. Restricciones
¿Qué no se puede romper? no modificar el contrato del endpoint para transferencias válidas; no tocar el módulo de auditoría.
4. Criterios de aceptación
¿Cómo se sabe que quedó bien, de forma verificable? una transferencia por encima del monto máximo devuelve HTTP 400 con mensaje claro; una transferencia válida no cambia su comportamiento.
5. Riesgos
¿Qué podría salir mal, o qué es sensible? si el límite queda mal calibrado, se podrían bloquear transferencias legítimas de clientes corporativos.
6. Plan de pruebas
¿Qué casos se van a probar? monto justo en el límite, un peso por encima del límite, monto negativo, y una transferencia válida muy por debajo del límite.