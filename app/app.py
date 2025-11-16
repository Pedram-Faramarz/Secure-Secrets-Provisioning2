from flask import Flask, jsonify
import os
import yaml
import hvac



app = Flask(__name__)


# helper:read secrets.yaml (decrypted file)
def read_secrets_file(path="C:\\Users\\pedra\\Desktop\\Secure-Secrets-Provisioning\\app\\secrets_template.yaml"):
    if not os.path.exists(path):
        return {"error" : f"{path} not found"}
    with open(path, 'r') as file:
        try:
            return yaml.safe_load(file)
        except Exception as e:
            return {"error" : f"failed to parse {path}: {str(e)}"}
        



@app.route("/")
def index():
    # secrets from environment variables
    env_secret = os.environ.get("ENV_SECRET",None)
    env_user = os.environ.get("ENV_USER",None)

    #secrets from local secrets.yaml file (assume decrypted)
    file_secrets = read_secrets_file()


    return jsonify({
        "from_evn" : {
            "ENV_USER": env_user,"ENV_SECRET": bool(env_secret)},
            "from_file": file_secrets
    })


@app.route("/vault")
def vault_secrets():
    #connect to vault
   
    vault_addr = os.environ.get("VAULT_ADDR", "http://localhost:8200")
    vault_token = os.environ.get("VAULT_TOKEN", None)
    secret_path = os.environ.get("VAULT_SECRET_PATH", "Pedram")  # just the secret name

    if not vault_token:
        return jsonify({"error": "VAULT_TOKEN not set"}), 400

    client = hvac.Client(url=vault_addr, token=vault_token)
    if not client.is_authenticated():
        return jsonify({"error": "failed to authenticate"}), 401

    try:
        # specify your KV mount explicitly
        read_resp = client.secrets.kv.v2.read_secret_version(
            path=secret_path,
            mount_point="secret"  # <-- important: your mount is 'secret'
        )
        secret_data = read_resp['data']['data']
        return jsonify(secret_data)
    except Exception as e:
        return jsonify({"error": f"failed to read secret from vault: {str(e)}"}), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)