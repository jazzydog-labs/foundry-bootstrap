#!/usr/bin/env python3
"""
foundry-bootstrap orchestrator

This script handles the installation of development tools based on configuration files.
It reads YAML configs and installs tools via subprocess calls.
"""

import os
import sys
import subprocess
import yaml
from pathlib import Path
from typing import List, Dict, Any
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

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
        
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def run_command(self, cmd: List[str], description: str) -> bool:
        """Run a command and return success status."""
        try:
            self.console.print(f"[blue]Running: {description}[/blue]")
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True
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
    
    def install_brew_packages(self) -> bool:
        """Install Homebrew packages from config."""
        config = self.load_config('brew.yaml')
        packages = config.get('packages', [])
        
        if not packages:
            self.console.print("[yellow]No Homebrew packages configured[/yellow]")
            return True
        
        # Check if brew is available
        if not self.check_command_exists('brew'):
            self.console.print("[red]Homebrew not found. Please install it first.[/red]")
            return False
        
        # Get list of already installed packages
        try:
            result = subprocess.run(['brew', 'list'], capture_output=True, text=True, check=True)
            installed = result.stdout.split()
        except subprocess.CalledProcessError:
            installed = []
        
        # Install missing packages
        to_install = [pkg for pkg in packages if pkg not in installed]
        
        if not to_install:
            self.console.print("[green]All Homebrew packages already installed[/green]")
            return True
        
        self.console.print(f"[blue]Installing {len(to_install)} Homebrew packages...[/blue]")
        
        for package in to_install:
            if not self.run_command(['brew', 'install', package], f"brew install {package}"):
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
        
        # Install Homebrew packages
        if not self.install_brew_packages():
            success = False
        
        # Install pipx packages
        if not self.install_pipx_packages():
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