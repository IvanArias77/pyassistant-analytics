#!/bin/sh
set -e

# Asegura que el comando start.sh exista antes de intentar ejecutarlo
if [ ! -f "backend/start.sh" ]; then
    echo 'Error: start.sh no existe'
    exit 1
fi

# Si existe, ejecútalo
exec backend/start.sh