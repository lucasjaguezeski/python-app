#!/usr/bin/env sh
set -eu

USE_WHEEL=0

for arg in "$@"; do
  case $arg in
    --wheel|-w)
      USE_WHEEL=1
      shift
      ;;
  esac
done

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")

if [ "$USE_WHEEL" -eq 1 ]; then
  COMPOSE_FILE="$SCRIPT_DIR/whl/docker-compose.yml"
  echo "=> Modo Wheel ativado. Compilando o pacote antes (uv build)..."
  cd "$PROJECT_ROOT"
  uv build
else
  COMPOSE_FILE="$SCRIPT_DIR/docker-compose.yml"
fi

ENV_FILE="$SCRIPT_DIR/.env.prod"

if ! command -v docker >/dev/null 2>&1; then
  echo "Erro: docker nao encontrado no PATH." >&2
  exit 1
fi

if [ ! -f "$ENV_FILE" ]; then
  echo "Erro: arquivo de ambiente nao encontrado em $ENV_FILE" >&2
  exit 1
fi

cd "$PROJECT_ROOT"

echo "[1/2] Build da imagem da API..."
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" build api

echo "[2/2] Subindo containers..."
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d --remove-orphans api

echo "Containers em execucao."
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" ps
