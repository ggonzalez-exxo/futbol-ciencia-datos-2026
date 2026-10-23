#!/usr/bin/env bash
# Genera todos los assets del video (figuras + animaciones).
# Uso:
#   bash video/scripts/generar_todo.sh
#   PY=.venv-video/bin/python bash video/scripts/generar_todo.sh

set -euo pipefail

cd "$(dirname "$0")/../.."

PY="${PY:-.venv-video/bin/python}"

if [ ! -x "$PY" ]; then
  echo "No se encontró el intérprete: $PY"
  echo "Creá el entorno primero (ver video/README.md):"
  echo "  uv venv --python 3.12 .venv-video"
  echo "  uv pip install --python .venv-video/bin/python -r video/scripts/requirements.txt"
  exit 1
fi

echo "== 1/2 Extrayendo figuras de los notebooks =="
"$PY" video/scripts/extraer_figuras.py

echo
echo "== 2/2 Generando animaciones =="
"$PY" video/scripts/generar_animaciones.py

echo
echo "Listo. Assets en video/graficos/ y video/animaciones/"
