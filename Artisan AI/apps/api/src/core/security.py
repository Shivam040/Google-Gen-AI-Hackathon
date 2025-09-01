# security.py

# Purpose: AuthN/Z helpers.
# Put inside: Firebase/OIDC token verifier, role checks (artisan/buyer/admin).
# Exports: get_current_user() dependency; require_role("admin").
# Tip: Start with “allow-all” in dev, swap later.