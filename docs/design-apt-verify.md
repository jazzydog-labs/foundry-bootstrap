# Design: apt package verification

## Rationale

The first task in `TODO.md` requests confirmation that every tool listed in
`config/packages.yaml` is available in the Ubuntu apt repositories. Any tool not
present should still be installed by some other method. We already skip unknown
packages during bootstrap, but we do not have a lightweight way to audit the
configuration up front.

## Approach

Provide a small verification script `scripts/verify_apt_packages.py` that reads
`config/packages.yaml` and checks each package name (or `apt-override`) using
`apt-cache show`. Missing packages are reported and appended to `TODO.md` just
like the orchestrator does. The script exits with status code `1` when any
package is missing so CI can detect configuration drift.

This keeps the check independent from the full bootstrap flow and allows quick
validation of new package lists.

## Touchpoints

```
config/packages.yaml   # source list
scripts/verify_apt_packages.py  # new audit helper
TODO.md               # updated automatically when packages are missing
README.md             # document the helper
```

## Alternatives considered

- Reusing the orchestrator directly. Rejected to avoid pulling in Python
  dependencies when only verifying apt packages.
- Writing the helper in Bash. Possible, but Python provides clearer YAML parsing
  and aligns with the rest of the project.
