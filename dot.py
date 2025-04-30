import os
import subprocess
import re
import logging
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress

# Initialize logging
logging.basicConfig(filename="dot_installer.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize the rich console object
console = Console()

# Define tools with their names, config cloning commands, and package installation commands
TOOLS = [
    {
        "name": "nvim",
        "config_clone": "mkdir -p ~/.config && git clone https://github.com/dip-pvt/nvim.git ~/.config/nvim",
        "pkg_name": "neovim",  # Use correct package name
        "additional_commands": [],  # Optional field for extra steps
    },
    {
        "name": "tmux",
        "config_clone": "mkdir -p ~/.config && git clone https://github.com/dip-pvt/tmux.git ~/.config/tmux",  # Fixed URL
        "pkg_name": "tmux",
        "additional_commands": [],
    },
    {
        "name": "kitty",
        "config_clone": "mkdir -p ~/.config && git clone https://github.com/dip-pvt/kitty.git ~/.config/kitty",
        "pkg_name": "kitty",
        "additional_commands": [],
    },
]

def run_command(command, description, progress=None, task=None):
    """Run a shell command with error handling and progress feedback."""
    console.print(f"Running: {description}...", style="bold green")
    try:
        process = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
        logging.info(f"Successfully ran: {command}")
        if progress and task:
            progress.advance(task)
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Error: {description} failed: {e.stderr}[/bold red]")
        logging.error(f"Failed to run {command}: {e.stderr}")
        return False
    except Exception as e:
        console.print(f"[bold red]Unexpected error: {str(e)}[/bold red]")
        logging.error(f"Unexpected error in {command}: {str(e)}")
        return False

def clone_config(command):
    """Clone a configuration repository."""
    return run_command(command, "Config clone step")

def install_pkg(pkg_name):
    """Install a package using the system package manager."""
    if not pkg_name:
        console.print("No package installation required.", style="bold cyan")
        return True

    # Detect package manager (simplified; could be expanded)
    pkg_manager = "apt" if os.system("command -v apt >/dev/null 2>&1") == 0 else "brew"
    if pkg_manager == "apt":
        command = f"sudo apt update && sudo apt install -y {pkg_name}"
    elif pkg_manager == "brew":
        command = f"brew install {pkg_name}"
    else:
        console.print("[bold red]No supported package manager found.[/bold red]")
        logging.error("No supported package manager found.")
        return False

    return run_command(command, f"Installing {pkg_name}")

def run_tool(tool):
    """Run all steps for a tool with progress tracking."""
    with Progress(console=console) as progress:
        task_clone = progress.add_task(f"Cloning {tool['name']} config...", total=1)
        if not clone_config(tool["config_clone"]):
            return False

        task_install = progress.add_task(f"Installing {tool['pkg_name']}...", total=1)
        if not install_pkg(tool["pkg_name"]):
            return False

        # Run additional commands if any
        for cmd in tool.get("additional_commands", []):
            task_extra = progress.add_task(f"Running extra step for {tool['name']}...", total=1)
            if not run_command(cmd, f"Extra step: {cmd}", progress, task_extra):
                return False

    return True

def display_menu():
    """Display the tool selection menu."""
    console.print("[bold magenta]Select tools to install:[/bold magenta]")
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Option", justify="center")
    table.add_column("Tool Name", justify="center")

    for idx, tool in enumerate(TOOLS, start=1):
        table.add_row(f"[{idx}]", tool["name"])
    table.add_row("[0]", "Install all tools")

    console.print(table)

def get_user_selection():
    """Get and validate user tool selections."""
    while True:
        choice = Prompt.ask(
            "Enter the numbers of the tools to install (comma-separated, e.g., '1,3' or '0' for all)"
        )
        # Validate input with regex
        if not re.match(r'^[\d, ]*$', choice):
            console.print("[bold red]Invalid input. Use numbers and commas only.[/bold red]")
            continue

        choices = [x.strip() for x in choice.split(",") if x.strip()]
        selected_tools = set()  # Use set to avoid duplicates

        for c in choices:
            if c == "0":
                selected_tools.update(tool["name"] for tool in TOOLS)
                break
            elif c.isdigit() and 1 <= int(c) <= len(TOOLS):
                selected_tools.add(TOOLS[int(c) - 1]["name"])
            else:
                console.print(f"[bold red]Invalid option: {c}. Please try again.[/bold red]")
                break
        else:  # No break occurred, input is valid
            if selected_tools:
                return list(selected_tools)
            console.print("[bold red]No valid tools selected. Please try again.[/bold red]")

def main():
    """Main function to run the installer."""
    display_menu()
    selected_tools = get_user_selection()

    console.print("\n[bold yellow]Starting installation...[/bold yellow]")
    success = True
    for tool_name in selected_tools:
        tool = next((t for t in TOOLS if t["name"] == tool_name), None)
        if tool:
            console.print(f"\n[bold green]Installing {tool_name}...[/bold green]")
            if not run_tool(tool):
                success = False
                console.print(f"[bold red]Failed to install {tool_name}.[/bold red]")
                logging.error(f"Installation failed for {tool_name}")

    if success:
        console.print("\n[bold green]Installation complete.[/bold green]")
    else:
        console.print("\n[bold red]Installation completed with errors. Check dot_installer.log for details.[/bold red]")

if __name__ == "__main__":
    main()
