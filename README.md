# foundry-bootstrap

A minimal bootstrapper for the **foundry** development environment. It installs shared tooling across the foundry ecosystem using a small Bash layer and a Python orchestrator. Package lists live in the `config/` directory so that all projects use the same versions.

## Quick start

```bash
git clone https://github.com/jazzydog-labs/foundry-bootstrap.git
cd foundry-bootstrap
./bootstrap.sh
```

The script installs the required package manager (Homebrew on macOS or apt on Linux), pyenv, Python and pipx. It then delegates to `orchestrate/main.py` to install everything defined in the YAML files. If an apt package is unavailable the orchestrator now tries a small fallback installer (for example a curl script) and still records the item in `TODO.md`. At the end `test_setup.py` verifies the tools are available.

When running on Linux the bootstrapper installs the build dependencies needed by
pyenv. Set the environment variable `PYENV_ARCHIVE` to the path of a tarball
containing a cloned `pyenv` repository to perform the installation without
network access. Use `PYENV_SKIP_DEPS=1` to skip the dependency step if required.

## Configuration

- `config/packages.yaml` – system packages with optional apt overrides
- `config/pipx.yaml` – Python CLI tools
- `config/npm.yaml`  – global npm packages
- `config/pyenv_version.txt` – Python version for pyenv

Edit these files to customise your environment. Re-run the bootstrap script to apply changes.

## Repository layout

```
.
├── bootstrap.sh             # entry point
├── install/                 # Bash installers
├── orchestrate/main.py      # Python orchestrator
├── config/                  # package lists and templates
└── test_setup.py            # verification script
```

## Testing

After bootstrapping you can rerun the verification script at any time:

```bash
python3 test_setup.py
```

To confirm that all system packages are available in the Ubuntu repositories
without running the full bootstrap, execute:

```bash
scripts/verify_apt_packages.py
```

## Container info

The development container for this repo uses Ubuntu 24.04.2 LTS.
See `docs/container-info.md` for a Docker snippet to replicate it locally.

## Contributing

Fork the repo, create a branch and open a pull request. Keep configuration files and documentation in sync.

## License

This project is provided as is for experimentation.
