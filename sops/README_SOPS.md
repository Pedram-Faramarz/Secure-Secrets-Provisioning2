I'll use sops + age (modern and simple). Steps:

Install sops (https://github.com/mozilla/sops
) and age (https://github.com/FiloSottile/age
).

macOS: brew install sops age

Linux (Debian/Ubuntu): follow the sops release binary; or apt if available.

Generate an age keypair:

# run in repo root
mkdir -p .sops
# create an age keypair; this prints the public key and private key
age-keygen -o .sops/age_key.txt
# Show public key to add as a key for sops
AGE_PRIVATE_KEY=$(sed -n '1p' .sops/age_key.txt)
AGE_PUBLIC_KEY=$(sed -n '2p' .sops/age_key.txt)
echo "private key is in .sops/age_key.txt (protect this!)"
echo "public key:"
sed -n '2p' .sops/age_key.txt


The .sops/age_key.txt contains two lines: private, then public. Keep the private key secret and add the public key to sops config or your teammates' config.

Encrypt the template app/secrets_template.yaml to app/secrets.yaml:

# from repo root
export SOPS_AGE_KEY=$(sed -n '1p' .sops/age_key.txt)
# Use sops to encrypt; supply the recipient public key (line 2)
RECIPIENT=$(sed -n '2p' .sops/age_key.txt)
sops --encrypt --age "$RECIPIENT" app/secrets_template.yaml > app/secrets.yaml
# Verify it's encrypted
file app/secrets.yaml
head -n 5 app/secrets.yaml


Commit encrypted app/secrets.yaml to git. Do not commit .sops/age_key.txt (private key). Add .sops/age_key.txt to .gitignore.

.gitignore:

.sops/age_key.txt
venv/
__pycache__/
*.pyc
.env


To decrypt locally:

export SOPS_AGE_KEY="$(sed -n '1p' .sops/age_key.txt)"
sops --decrypt app/secrets.yaml > app/secrets_decrypted.yaml
# or overwrite the file (careful)
# sops -d -i app/secrets.yaml


You can also configure your editor to use sops to decrypt on the fly.