# vault/policies/app-policy.hcl
path "secret/data/myapp" {
  capabilities = ["read", "list"]
}
