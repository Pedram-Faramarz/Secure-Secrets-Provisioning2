# Secure-Secrets-Provisioning
Try all mechanisms of secrets provisioning

Directory:
├─ app/
│  ├─ app.py
│  ├─ requirements.txt
│  ├─ Dockerfile
│  └─ secrets.yaml
├─ docker-compose.yml
├─ sops/
│  ├─ README_SOPS.md
│  └─ .sops/          (ignored in git)
├─ vault/
│  ├─ vault-init.sh
│  └─ policies/
│     └─ app-policy.hcl
├─ .gitignore
└─ README.md


# Secure Secrets Lab - README

This repo demonstrates three secrets provisioning methods:
1. Environment variables
2. Encrypted config file (sops + age)
3. HashiCorp Vault (KV v2)

## Quick run (local, Docker)
Prereqs:
- docker & docker-compose
- sops and age (for encrypt/decrypt)
- jq (optional, for JSON formatting)

Steps:
1. Build & start vault:
   docker-compose up -d vault
2. Initialize vault secrets:
   ./vault/vault-init.sh
3. Encrypt the secrets file with sops (see sops/README_SOPS.md)
4. Start the app:
   docker-compose up -d app
5. Visit:
   http://localhost:5000/          # env + file
   http://localhost:5000/vault    # read from vault
