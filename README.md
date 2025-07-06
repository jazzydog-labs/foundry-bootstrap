# foundry-bootstrap

A minimal bootstrapper for the **foundry** development environment. It installs shared tooling across the foundry ecosystem using a small Bash layer and a Python orchestrator. Package lists live in the `config/` directory so that all projects use the same versions.

## Quick start

```bash
git clone https://github.com/jazzydog-labs/foundry-bootstrap.git
cd foundry-bootstrap
./bootstrap.sh
```

The script installs Homebrew, pyenv, Python and pipx, then delegates to `orchestrate/main.py` to install everything defined in the YAML files. At the end `test_setup.py` verifies the tools are available.

## Configuration

- `config/brew.yaml` – Homebrew packages
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

## Contributing

Fork the repo, create a branch and open a pull request. Keep configuration files and documentation in sync.

## License

This project is provided as is for experimentation.
