# foundry-bootstrap

The canonical bootstrapper for the `foundry` ecosystem — a local-first, agent-augmented, multi-repo environment. This repository sets up global tooling and environment configuration so that all related projects (`foundry`, `anvil`, `archives`, etc.) work consistently across machines.

## 🎯 Purpose

`foundry-bootstrap` provides a standardized development environment setup that:

- **Installs global development tools** and environment dependencies
- **Uses minimal bash** for early-stage bootstrapping (just enough to get Python running)
- **Delegates orchestration to Python** for structured tool management
- **Stores tool declarations in structured configuration files** (YAML), not hardcoded in scripts
- **Ensures consistency** across all foundry ecosystem projects

## 🏗️ Architecture

### Philosophy

- **Minimize bash scripting** - Use bash only for bootstrapping core dependencies
- **Declarative configuration** - All tool lists stored in YAML config files
- **Python orchestration** - After Python is available, delegate all tool management to Python
- **Extensible design** - Easy to add new tool types and configurations

### Repository Layout

```
foundry-bootstrap/
├── bootstrap.sh                    # Entry point: minimal bash bootstrapper
├── install/                        # Bash installation scripts
│   ├── install_brew.sh            # Installs Homebrew if missing
│   ├── install_pyenv.sh           # Installs pyenv and sets global Python
│   ├── install_python.sh          # Installs Python 3.12 (via pyenv)
│   └── setup_python_orchestrator.sh # Bootstraps pipx, poetry, etc.
├── config/                         # Declarative configuration files
│   ├── brew.yaml                  # Tools to install via brew
│   ├── pipx.yaml                  # Python CLI tools
│   ├── pyenv_version.txt          # Python version
│   └── envrc_template             # Template for .envrc
├── orchestrate/
│   └── main.py                    # Python entrypoint for tool orchestration
├── requirements.txt               # Python dependencies
├── test_setup.py                  # Verification script
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- macOS (tested on macOS 12+)
- Internet connection for downloading tools
- User with sudo privileges (for Homebrew installation)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jazzydog-labs/foundry-bootstrap.git
   cd foundry-bootstrap
   ```

2. **Run the bootstrap:**
   ```bash
   ./bootstrap.sh
   ```
   
   The bootstrap will automatically run verification tests at the end to ensure all tools are properly installed.

### What Gets Installed

#### Core Tools (via bash)
- **Homebrew** - Package manager for macOS
- **pyenv** - Python version manager
- **Python 3.12** - Latest stable Python version
- **pip** - Latest version (automatically upgraded)
- **pipx** - Python CLI tool installer

#### Development Tools (via Python orchestration)
- **direnv** - Directory-based environment variables
- **just** - Command runner
- **gh** - GitHub CLI
- **jq, fzf, ripgrep, bat** - Text processing and search tools
- **git, tree, htop, tmux, neovim** - Development utilities

#### Python Tools (via pipx)
- **black, mypy, ruff, isort** - Code quality and formatting
- **poetry, cookiecutter, pre-commit** - Development tools
- **pytest, httpie** - Testing and utilities

## ⚙️ Customization

### Adding New Tools

#### Homebrew Packages
Edit `config/brew.yaml`:
```yaml
packages:
  - existing-tool
  - your-new-tool
```

#### Python CLI Tools
Edit `config/pipx.yaml`:
```yaml
packages:
  - existing-tool
  - your-new-tool
```

#### Changing Python Version
Edit `config/pyenv_version.txt`:
```
3.12.0
```

### Extending Orchestration

The Python orchestrator (`orchestrate/main.py`) is designed to be extensible:

1. **Add new tool types** by creating new methods in `BootstrapOrchestrator`
2. **Add new configuration files** in the `config/` directory
3. **Create plugins** for specialized tool management

Example extension:
```python
def install_npm_packages(self) -> bool:
    """Install npm packages from config."""
    config = self.load_config('npm.yaml')
    packages = config.get('packages', [])
    # ... implementation
```

## 🔄 Bootstrap Flow

1. **`bootstrap.sh` (bash):**
   - Installs Homebrew, pyenv, and Python 3.12
   - Upgrades pip to latest version
   - Boots a minimal Python environment (pipx)
   - Configures PATH for Python user bin directory
   - Hands off to Python orchestrator (`main.py`)

2. **`main.py` (Python):**
   - Reads configuration files
   - Installs Homebrew packages, pipx CLIs, and other global tools
   - Sets up environment configuration (direnv, etc.)

3. **Verification (automatic):**
   - Runs `test_setup.py` to verify all tools are properly installed
   - Provides clear success/failure feedback

## 🧪 Testing

The bootstrap process automatically runs verification tests at the end. You can also run the test suite manually to verify your setup:

```bash
python3 test_setup.py
```

This will check that all configured tools are properly installed and accessible.

## 🔧 Troubleshooting

### Common Issues

**Homebrew installation fails:**
- Ensure you have admin privileges
- Check your internet connection
- Try running the Homebrew installation manually

**Python tools not found:**
- Ensure pipx is in your PATH: `export PATH="$HOME/.local/bin:$PATH"`
- Ensure Python user bin directory is in PATH: `export PATH="$HOME/Library/Python/3.12/bin:$PATH"`
- Restart your shell after installation

**Permission errors:**
- Some tools may require sudo access
- Check file permissions on the bootstrap scripts

### Debug Mode

Run with verbose output:
```bash
bash -x bootstrap.sh
```

## 📚 Related Projects

- **foundry** - Main development workspace
- **anvil** - Environment surface
- **archives** - Historical artifacts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is experimental and provided as-is.

---

**Note:** This is a bootstrapper for the foundry ecosystem. After running this, you'll have a consistent development environment across all foundry-related projects. 