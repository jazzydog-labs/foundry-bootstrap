#!/usr/bin/env python3
"""
Test script to verify foundry-bootstrap setup

This script checks that all required tools are properly installed and accessible.
"""

import subprocess
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

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

def main():
    """Run the test suite."""
    console.print("[bold blue]🧪 Testing foundry-bootstrap setup[/bold blue]\n")
    
    # Core tools
    core_tools = [
        ('brew', 'Homebrew'),
        ('pyenv', 'pyenv'),
        ('python3', 'Python 3'),
        ('pip3', 'pip3'),
        ('pipx', 'pipx'),
    ]
    
    # Development tools
    dev_tools = [
        ('direnv', 'direnv'),
        ('just', 'just'),
        ('gh', 'GitHub CLI'),
        ('jq', 'jq'),
        ('fzf', 'fzf'),
        ('rg', 'ripgrep'),
        ('bat', 'bat'),
        ('git', 'git'),
        ('tree', 'tree'),
        ('htop', 'htop'),
        ('tmux', 'tmux', '-V'),  # tmux uses -V instead of --version
        ('nvim', 'neovim'),
    ]
    
    # Python tools
    python_tools = [
        ('black', 'black'),
        ('mypy', 'mypy'),
        ('ruff', 'ruff'),
        ('isort', 'isort', '--version-number'),  # isort uses --version-number for clean output
        ('poetry', 'poetry'),
        ('cookiecutter', 'cookiecutter'),
        ('pre-commit', 'pre-commit'),
        ('pytest', 'pytest'),
        ('http', 'httpie'),
    ]
    
    # Test core tools
    console.print("[bold]Core Tools:[/bold]")
    core_success = all(check_command(cmd, name) for cmd, name in core_tools)
    console.print()
    
    # Test development tools
    console.print("[bold]Development Tools:[/bold]")
    dev_results = []
    for tool in dev_tools:
        if len(tool) == 3:
            cmd, name, version_flag = tool
            dev_results.append(check_command(cmd, name, version_flag))
        else:
            cmd, name = tool
            dev_results.append(check_command(cmd, name))
    dev_success = all(dev_results)
    console.print()
    
    # Test Python tools
    console.print("[bold]Python Tools:[/bold]")
    python_results = []
    for tool in python_tools:
        if len(tool) == 3:
            cmd, name, version_flag = tool
            python_results.append(check_command(cmd, name, version_flag))
        else:
            cmd, name = tool
            python_results.append(check_command(cmd, name))
    python_success = all(python_results)
    console.print()
    
    # Summary
    total_tools = len(core_tools) + len(dev_tools) + len(python_tools)
    successful_tools = sum([
        core_success * len(core_tools),
        dev_success * len(dev_tools), 
        python_success * len(python_tools)
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