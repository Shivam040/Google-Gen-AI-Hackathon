# auth.py

# Purpose: Request authentication middleware/dependency.
# Put inside: header parsing (Authorization: Bearer …), decode/verify, attach user to request state.
# Exports: get_actor() dependency returning {id, role, locale}.