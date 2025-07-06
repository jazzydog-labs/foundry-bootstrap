#!/usr/bin/env python3
"""
foundry-bootstrap orchestrator

This script handles the installation of development tools based on configuration files.
It reads YAML configs and installs tools via subprocess calls.
"""

import os
import sys
import subprocess
from ruamel.yaml import YAML
from pathlib import Path
from typing import List, Dict, Any
import click
from rich.console import Console

console = Console()

class BootstrapOrchestrator:
    """Orchestrates the installation of development tools."""
    
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.console = Console()
    
    def load_config(self, filename: str) -> Dict[str, Any]:
        """Load a YAML configuration file."""
        config_path = self.config_dir / filename
        if not config_path.exists():
            self.console.print(f"[red]Config file not found: {config_path}[/red]")
            return {}
        
        yaml = YAML(typ='safe')
        with open(config_path, 'r') as f:
            return yaml.load(f)
    
    def run_command(self, cmd: List[str], description: str, env: Dict[str, str] | None = None) -> bool:
        """Run a command and return success status."""
        try:
            self.console.print(f"[blue]Running: {description}[/blue]")
            subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                env=env
            )
            self.console.print(f"[green]✅ {description} completed[/green]")
            return True
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]❌ {description} failed: {e.stderr}[/red]")
            return False
    
    def check_command_exists(self, cmd: str) -> bool:
        """Check if a command exists in PATH."""
        try:
            subprocess.run([cmd, '--version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def apt_package_exists(self, package: str) -> bool:
        """Return True if an apt package is available."""
        try:
            result = subprocess.run(
                ['apt-cache', 'show', package], capture_output=True, text=True, check=True
            )
            return 'No packages found' not in result.stdout
        except subprocess.CalledProcessError:
            return False

    def record_missing_package(self, package: str) -> None:
        """Append a TODO entry for a missing apt package."""
        todo_path = Path(__file__).resolve().parent.parent / 'TODO.md'
        line = f"- [ ] Add apt installation method for {package}\n"
        try:
            if todo_path.exists():
                with open(todo_path, 'r+') as f:
                    contents = f.read()
                    if line.strip() not in contents:
                        f.write(line)
        except Exception as e:
            self.console.print(f"[red]Failed to write to {todo_path}: {e}[/red]")
    
    def install_system_packages(self) -> bool:
        """Install system packages using brew on macOS or apt on Linux."""
        config = self.load_config('packages.yaml')
        package_entries = config.get('packages', [])

        if not package_entries:
            self.console.print("[yellow]No system packages configured[/yellow]")
            return True

        os_name = sys.platform
        if os_name.startswith('darwin'):
            manager = 'brew'
        else:
            manager = 'apt'

        packages: List[str] = []
        for item in package_entries:
            name = None
            override = None
            if isinstance(item, str):
                name = item
            elif isinstance(item, dict):
                if 'name' in item:
                    name = item.get('name')
                    override = item.get('apt-override')
                elif len(item) == 1:
                    name, meta = next(iter(item.items()))
                    if isinstance(meta, dict):
                        override = meta.get('apt-override')
            if not name:
                continue
            packages.append(override if manager == 'apt' and override else name)

        if not packages:
            self.console.print(f"[yellow]No packages defined for {manager}[/yellow]")
            return True

        if manager == 'brew':
            if not self.check_command_exists('brew'):
                self.console.print("[red]Homebrew not found. Please install it first.[/red]")
                return False

            try:
                result = subprocess.run(['brew', 'list'], capture_output=True, text=True, check=True)
                installed = result.stdout.split()
            except subprocess.CalledProcessError:
                installed = []

            to_install = [pkg for pkg in packages if pkg not in installed]

            if not to_install:
                self.console.print("[green]All Homebrew packages already installed[/green]")
                return True

            self.console.print(f"[blue]Installing {len(to_install)} Homebrew packages...[/blue]")
            for package in to_install:
                if not self.run_command(['brew', 'install', package], f"brew install {package}"):
                    return False

        else:  # apt
            if not self.check_command_exists('apt-get'):
                self.console.print("[red]apt-get not found. Cannot install packages[/red]")
                return False

            self.console.print("[blue]Updating apt package list...[/blue]")
            if not self.run_command(['apt-get', 'update'], 'apt-get update'):
                return False

            valid_packages: List[str] = []
            for package in packages:
                if self.apt_package_exists(package):
                    valid_packages.append(package)
                else:
                    self.console.print(f"[yellow]⚠️  apt package not found: {package}. Skipping.[/yellow]")
                    self.record_missing_package(package)

            if not valid_packages:
                self.console.print("[yellow]No valid apt packages to install[/yellow]")
                return True

            self.console.print(f"[blue]Installing {len(valid_packages)} apt packages...[/blue]")
            install_cmd = ['apt-get', 'install', '-y'] + valid_packages
            if not self.run_command(install_cmd, 'apt-get install'):
                return False

        return True
    
    def install_pipx_packages(self) -> bool:
        """Install pipx packages from config."""
        config = self.load_config('pipx.yaml')
        packages = config.get('packages', [])
        
        if not packages:
            self.console.print("[yellow]No pipx packages configured[/yellow]")
            return True
        
        # Check if pipx is available
        if not self.check_command_exists('pipx'):
            self.console.print("[red]pipx not found. Please install it first.[/red]")
            return False
        
        # Get list of already installed packages
        try:
            result = subprocess.run(['pipx', 'list'], capture_output=True, text=True, check=True)
            installed = [line.split()[0] for line in result.stdout.split('\n') if line.strip()]
        except subprocess.CalledProcessError:
            installed = []
        
        # Install missing packages
        to_install = [pkg for pkg in packages if pkg not in installed]
        
        if not to_install:
            self.console.print("[green]All pipx packages already installed[/green]")
            return True
        
        self.console.print(f"[blue]Installing {len(to_install)} pipx packages...[/blue]")
        
        for package in to_install:
            if not self.run_command(['pipx', 'install', package], f"pipx install {package}"):
                return False
        
        return True
    
    def install_npm_packages(self) -> bool:
        """Install npm global packages from config."""
        config = self.load_config('npm.yaml')
        packages = config.get('packages', [])
        
        if not packages:
            self.console.print("[yellow]No npm packages configured[/yellow]")
            return True
        
        # Check if npm is available
        if not self.check_command_exists('npm'):
            self.console.print("[red]npm not found. Please install Node.js first.[/red]")
            return False
        
        # Get list of already installed packages
        try:
            result = subprocess.run(['npm', 'list', '-g', '--depth=0'], capture_output=True, text=True, check=True)
            installed = []
            for line in result.stdout.split('\n'):
                if line.strip() and not line.startswith('/') and not line.startswith('npm'):
                    # Extract package name from npm list output
                    parts = line.split()
                    if parts:
                        installed.append(parts[0])
        except subprocess.CalledProcessError:
            installed = []
        
        # Install missing packages
        to_install = [pkg for pkg in packages if pkg not in installed]
        
        if not to_install:
            self.console.print("[green]All npm packages already installed[/green]")
            return True
        
        self.console.print(f"[blue]Installing {len(to_install)} npm packages...[/blue]")
        
        env = os.environ.copy()
        # Some npm packages (like mermaid-cli) download large browsers via puppeteer.
        # Skip those downloads in restricted environments.
        env.setdefault('PUPPETEER_SKIP_DOWNLOAD', '1')

        for package in to_install:
            if not self.run_command(['npm', 'install', '-g', package], f"npm install -g {package}", env=env):
                return False
        
        return True
    
    def setup_direnv(self) -> bool:
        """Setup direnv configuration."""
        if not self.check_command_exists('direnv'):
            self.console.print("[yellow]direnv not installed, skipping setup[/yellow]")
            return True
        
        # Create .envrc template in home directory
        template_path = self.config_dir / 'envrc_template'
        home_envrc = Path.home() / '.envrc'
        
        if template_path.exists() and not home_envrc.exists():
            try:
                import shutil
                shutil.copy2(template_path, home_envrc)
                self.console.print("[green]✅ Created .envrc template in home directory[/green]")
            except Exception as e:
                self.console.print(f"[red]❌ Failed to create .envrc template: {e}[/red]")
                return False
        
        return True
    
    def run(self) -> bool:
        """Run the complete orchestration process."""
        self.console.print("[bold blue]🔧 foundry-bootstrap orchestrator[/bold blue]")
        
        success = True
        
        # Install system packages
        if not self.install_system_packages():
            success = False
        
        # Install pipx packages
        if not self.install_pipx_packages():
            success = False
        
        # Install npm packages
        if not self.install_npm_packages():
            success = False
        
        # Setup direnv
        if not self.setup_direnv():
            success = False
        
        if success:
            self.console.print("[bold green]✅ All tools installed successfully![/bold green]")
        else:
            self.console.print("[bold red]❌ Some installations failed[/bold red]")
        
        return success

@click.command()
@click.option('--config-dir', default='../config', help='Path to configuration directory')
def main(config_dir: str):
    """foundry-bootstrap orchestrator."""
    config_path = Path(config_dir).resolve()
    
    if not config_path.exists():
        console.print(f"[red]Configuration directory not found: {config_path}[/red]")
        sys.exit(1)
    
    orchestrator = BootstrapOrchestrator(config_path)
    success = orchestrator.run()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 