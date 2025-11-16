#!/usr/bin/env bash
set -e
VAULT_ADDR=${VAULT_ADDR:-http://127.0.0.1:8200}
VAULT_TOKEN=${VAULT_TOKEN:-root-token}

echo "[*] Using VAULT_ADDR=$VAULT_ADDR VAULT_TOKEN=$VAULT_TOKEN"

export VAULT_ADDR
export VAULT_TOKEN

# create KV v2 secret at secret/data/myapp
curl --silent --fail --header "X-Vault-Token: ${VAULT_TOKEN}" \
  --request POST \
  --data '{"data": {"db_user":"vault_user","db_pass":"vault_pass","api_key":"vault-api-key-123"}}' \
  ${VAULT_ADDR}/v1/secret/data/myapp | jq .

echo "Wrote secret to secret/data/myapp"
