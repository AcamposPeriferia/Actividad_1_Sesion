#!/usr/bin/env bash
# guard.sh - PreToolUse: bloquea rutas y comandos sensibles antes de ejecutarlos

 
input=$(cat)
 
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')
command=$(echo "$input" | jq -r '.tool_input.command // empty')
 
BLOCKED_PATHS='\.env|secrets/|credentials|\.pem$|id_rsa'
BLOCKED_COMMANDS='rm -rf|DROP TABLE|DROP DATABASE'
 
if [[ "$file_path" =~ $BLOCKED_PATHS ]]; then
  echo "🚫 Bloqueado: '$file_path' es una ruta sensible (credenciales/datos). Requiere aprobación explícita del equipo." >&2
  exit 2
fi
 
if [[ -n "$command" && "$command" =~ $BLOCKED_COMMANDS ]]; then
  echo "🚫 Bloqueado: el comando coincide con un patrón destructivo no permitido." >&2
  exit 2
fi
 
exit 0
