#!/usr/bin/env python3
"""
Test script to verify foundry-bootstrap setup

This script checks that all required tools are properly installed and accessible.
"""

import subprocess
import sys
import yaml
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

def load_test_overrides(config_dir: Path) -> dict:
    """Load test configuration overrides."""
    overrides_file = config_dir / "test_overrides.yaml"
    if overrides_file.exists():
        try:
            with open(overrides_file, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            console.print(f"[yellow]⚠️  Error reading test overrides: {e}[/yellow]")
    return {}

def check_command(cmd: str, name: str, version_flag='--version') -> bool:
    """Check if a command is available and working."""
    try:
        result = subprocess.run([cmd, version_flag], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip().split('\n')[0]
            console.print(f"[green]✅ {name}: {version}[/green]")
            return True
        else:
            console.print(f"[red]❌ {name}: Command failed[/red]")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        console.print(f"[red]❌ {name}: Not found[/red]")
        return False

def load_requirements_file(filepath: Path) -> list:
    """Load requirements from a file."""
    if not filepath.exists():
        console.print(f"[yellow]⚠️  {filepath} not found[/yellow]")
        return []
    
    try:
        with open(filepath, 'r') as f:
            if filepath.suffix == '.yaml' or filepath.suffix == '.yml':
                data = yaml.safe_load(f)
                return data.get('packages', [])
            else:
                # Handle requirements.txt
                lines = f.readlines()
                packages = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Extract package name (remove version specifiers)
                        package = line.split('>=')[0].split('==')[0].split('<=')[0].split('~=')[0].split('!=')[0]
                        packages.append(package.strip())
                return packages
    except Exception as e:
        console.print(f"[red]❌ Error reading {filepath}: {e}[/red]")
        return []

def get_command_and_version(package: str, overrides: dict) -> tuple:
    """Get the actual command name and version flag for a package."""
    command_mappings = overrides.get('command_mappings', {})
    version_flags = overrides.get('version_flags', {})
    
    # Get the actual command name
    actual_command = command_mappings.get(package, package)
    
    # Get the version flag
    version_flag = version_flags.get(package, '--version')
    
    return actual_command, version_flag

def main():
    """Run the test suite."""
    console.print("[bold blue]🧪 Testing foundry-bootstrap setup[/bold blue]\n")
    
    script_dir = Path(__file__).parent
    config_dir = script_dir / "config"
    
    # Load test overrides
    overrides = load_test_overrides(config_dir)
    
    # Load tools from configuration files
    brew_packages = load_requirements_file(config_dir / "brew.yaml")
    pipx_packages = load_requirements_file(config_dir / "pipx.yaml")
    python_packages = load_requirements_file(script_dir / "requirements.txt")
    
    console.print(f"[dim]Loaded {len(brew_packages)} Homebrew packages, {len(pipx_packages)} pipx packages, {len(python_packages)} Python packages[/dim]\n")
    
    # Special cases: brew and pyenv are always required
    special_tools = [
        ('brew', 'Homebrew'),
        ('pyenv', 'pyenv'),
        ('python3', 'Python 3'),
        ('pip3', 'pip3'),
        ('pipx', 'pipx'),
    ]
    
    # Test special tools first
    console.print("[bold]Core Tools (Special):[/bold]")
    special_success = all(check_command(cmd, name) for cmd, name in special_tools)
    console.print()
    
    # Test Homebrew packages
    console.print("[bold]Homebrew Packages:[/bold]")
    brew_results = []
    for package in brew_packages:
        actual_command, version_flag = get_command_and_version(package, overrides)
        display_name = f"{package} ({actual_command})" if actual_command != package else package
        brew_results.append(check_command(actual_command, display_name, version_flag))
    brew_success = all(brew_results)
    console.print()
    
    # Test pipx packages
    console.print("[bold]pipx Packages:[/bold]")
    pipx_results = []
    for package in pipx_packages:
        actual_command, version_flag = get_command_and_version(package, overrides)
        display_name = f"{package} ({actual_command})" if actual_command != package else package
        pipx_results.append(check_command(actual_command, display_name, version_flag))
    pipx_success = all(pipx_results)
    console.print()
    
    # Test Python packages (import them)
    console.print("[bold]Python Packages:[/bold]")
    python_results = []
    for package in python_packages:
        # Use command mapping for Python packages too
        actual_import_name, _ = get_command_and_version(package, overrides)
        try:
            __import__(actual_import_name)
            display_name = f"{package} ({actual_import_name})" if actual_import_name != package else package
            console.print(f"[green]✅ {display_name}: Imported successfully[/green]")
            python_results.append(True)
        except ImportError:
            console.print(f"[red]❌ {package}: Import failed[/red]")
            python_results.append(False)
    python_success = all(python_results)
    console.print()
    
    # Summary
    total_tools = len(special_tools) + len(brew_packages) + len(pipx_packages) + len(python_packages)
    successful_tools = sum([
        special_success * len(special_tools),
        brew_success * len(brew_packages),
        pipx_success * len(pipx_packages),
        python_success * len(python_packages)
    ])
    
    console.print(f"[bold]Summary:[/bold] {successful_tools}/{total_tools} tools available")
    
    if successful_tools == total_tools:
        console.print("[bold green]🎉 All tools installed successfully![/bold green]")
        return 0
    else:
        console.print("[bold yellow]⚠️  Some tools are missing. Check the installation.[/bold yellow]")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 