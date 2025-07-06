# Design: apt package handling

## Rationale

`bootstrap.sh` delegates package installation to `orchestrate/main.py` and a small `install/install_apt.sh` helper. Currently the script blindly passes all packages from `config/packages.yaml` to `apt-get install`. When a tool is not available in the configured apt repositories the command fails and aborts the whole bootstrap. The TODO asks to confirm all apt package names and gracefully handle missing ones.

## Approach

1. Add a helper `apt_package_exists()` inside `BootstrapOrchestrator` that runs `apt-cache show <pkg>` and returns `False` when "No packages found" appears.
2. Filter the package list in `install_system_packages()` using this helper when the package manager is apt. Packages not found will be skipped *and* appended as TODO items for later handling.
3. Apply the same check in `install/install_apt.sh` for the bash-only path.
4. Document the behaviour in `README.md` and capture the container OS version for easy reproduction.

This keeps the logic simple and avoids failures when a package is missing. No changes to the YAML format are required.

## Touchpoints

```
config/packages.yaml    # unchanged list of packages
install/install_apt.sh  # adds existence check and writes to TODO
orchestrate/main.py     # skip missing packages and log TODO items
README.md               # mention automatic skipping and TODO log
docs/container-info.md  # document container OS
```

## Alternatives considered

- Extending the YAML schema with an explicit `apt: false` flag. Rejected for now to keep configuration minimal.
- Attempting to auto-install via alternative methods (e.g. from source) when a package is missing. Out of scope and increases complexity.

