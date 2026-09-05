#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f .env ]]; then
  cp .env.example .env
fi

if [[ "${CODESPACES:-false}" != "true" ]]; then
  exit 0
fi

forwarding_domain="${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN:-app.github.dev}"
web_origin="https://${CODESPACE_NAME}-3000.${forwarding_domain}"
ops_origin="https://${CODESPACE_NAME}-3001.${forwarding_domain}"
api_origin="https://${CODESPACE_NAME}-8000.${forwarding_domain}"

set_env_value() {
  local key="$1"
  local value="$2"

  if grep -q "^${key}=" .env; then
    sed -i "s|^${key}=.*$|${key}=${value}|" .env
  else
    printf '\n%s=%s\n' "$key" "$value" >> .env
  fi
}

set_env_value NEXT_PUBLIC_API_URL "$api_origin"
set_env_value ALLOWED_ORIGINS "${web_origin},${ops_origin}"

echo "Codespaces origins written to the ignored .env file."
