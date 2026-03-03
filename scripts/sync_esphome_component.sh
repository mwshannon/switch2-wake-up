#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST="root@homeassistant"
REMOTE_BASE_DIR="/root/config/esphome/my_components"
LOCAL_COMPONENT_DIR="components/switch2_wake"

if [[ ! -d "${LOCAL_COMPONENT_DIR}" ]]; then
  echo "Local component directory not found: ${LOCAL_COMPONENT_DIR}" >&2
  exit 1
fi

ssh "${REMOTE_HOST}" "mkdir -p '${REMOTE_BASE_DIR}'"
tar \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  -C "$(dirname "${LOCAL_COMPONENT_DIR}")" \
  -cf - "$(basename "${LOCAL_COMPONENT_DIR}")" \
  | ssh "${REMOTE_HOST}" "tar -C '${REMOTE_BASE_DIR}' -xf -"

echo "Deployed ${LOCAL_COMPONENT_DIR} to ${REMOTE_HOST}:${REMOTE_BASE_DIR}/"
