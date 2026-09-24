cat > .claude/commands/pr-description.md << 'EOF'

--
description: Genera la descripcion del PR
--

Revisa el diff (git diff main..HEAD) y redacta:

## Resumen
## Motivo del Cambio
## Riesgos (datos, contratos)
## Como probar

Usa solo lo que aparece en el diff
EOF
