# Design: apt fallback installers

## Rationale
The bootstrapper already skips missing apt packages and records them in `TODO.md`.
However the first task in `TODO.md` asks to "confirm apt package names for all tools and ensure installation for packages unavailable via apt".
All tools currently listed in `config/packages.yaml` exist in Ubuntu 24.04's
repositories, but future additions might not. To keep the environment usable we
add a small fallback mechanism that runs a custom install command when a package
is not found in apt.

## Approach
1. Maintain a mapping `APT_FALLBACKS` in `BootstrapOrchestrator` from package
   name to a command list. The command installs the tool from its official
   upstream (curl script or similar).
2. During `install_system_packages()` collect packages missing from apt. After
   the normal `apt-get install` step, invoke the fallback command for each
   missing package if available. When no fallback exists we keep the existing
   behaviour of appending a TODO entry.
3. Add a small pytest using `monkeypatch` to assert that the fallback command is
   executed when a package is absent.
4. Document the behaviour in the README.

This keeps the bootstrapping flow simple and avoids manual steps when a tool is
not packaged for Debian-based systems.
