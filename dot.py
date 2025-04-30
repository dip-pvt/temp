import os
import subprocess
import re

# Define tools with their names, config cloning commands, and package names
TOOLS = [
    {
        "name": "nvim",
        "config_clone": "mkdir -p ~/.config && git clone https://github.com/dip-pvt/nvim.git ~/.config/nvim",
        "pkg_name": "neovim",
    },
    {
        "name": "tmux",
        "config_clone": "mkdir -p ~/.config && git clone https://github.com/dip-pvt/tmux.git ~/.config/tmux",
        "pkg_name": "tmux",
    },
    {
        "name": "kitty",
        "config_clone": "mkdir -p ~/.config && git clone https://github.com/dip-pvt/kitty.git ~/.config/kitty",
        "pkg_name": "kitty",
    },
]

def run_command(command, description):
    """Run a shell command and show errors in real-time."""
    print(f"Running: {description}...")
    try:
        subprocess.run(command, shell=True, text=True, check=True)
        print(f"Success: {description} completed.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {description} failed: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False

def clone_config(command):
    """Clone a configuration repository."""
    return run_command(command, "Cloning configuration")

def install_pkg(pkg_name):
    """Install a package using apt, dnf, or pacman."""
    if not pkg_name:
        print("No package installation required.")
        return True

    # Detect package manager
    if os.system("command -v apt >/dev/null 2>&1") == 0:
        command = f"sudo apt update && sudo apt install -y {pkg_name}"
    elif os.system("command -v dnf >/dev/null 2>&1") == 0:
        command = f"sudo dnf install -y {pkg_name}"
    elif os.system("command -v pacman >/dev/null 2>&1") == 0:
        command = f"sudo pacman -S --noconfirm {pkg_name}"
    else:
        print("Error: No supported package manager found (apt, dnf, or pacman).")
        return False

    return run_command(command, f"Installing {pkg_name}")

def run_tool(tool):
    """Run all steps for a tool."""
    if not clone_config(tool["config_clone"]):
        return False
    if not install_pkg(tool["pkg_name"]):
        return False
    return True

def display_menu():
    """Show the tool selection menu."""
    print("Select tools to install:")
    for idx, tool in enumerate(TOOLS, start=1):
        print(f"[{idx}] {tool['name']}")
    print("[0] Install all tools")

def get_user_selection():
    """Get and validate user tool selections."""
    while True:
        choice = input("Enter numbers of tools to install (e.g., '1,3' or '0' for all): ")
        if not re.match(r'^[\d, ]*$', choice):
            print("Invalid input. Use numbers and commas only.")
            continue

        choices = [x.strip() for x in choice.split(",") if x.strip()]
        selected_tools = set()

        for c in choices:
            if c == "0":
                selected_tools.update(tool["name"] for tool in TOOLS)
                break
            elif c.isdigit() and 1 <= int(c) <= len(TOOLS):
                selected_tools.add(TOOLS[int(c) - 1]["name"])
            else:
                print(f"Invalid option: {c}. Please try again.")
                break
        else:  # No break occurred, input is valid
            if selected_tools:
                return list(selected_tools)
            print("No valid tools selected. Please try again.")

def main():
    """Main function to run the installer."""
    display_menu()
    selected_tools = get_user_selection()

    print("\nStarting installation...")
    success = True
    for tool_name in selected_tools:
        tool = next((t for t in TOOLS if t["name"] == tool_name), None)
        if tool:
            print(f"\nInstalling {tool_name}...")
            if not run_tool(tool):
                success = False
                print(f"Failed to install {tool_name}.")

    if success:
        print("\nInstallation complete.")
    else:
        print("\nInstallation completed with errors.")

if __name__ == "__main__":
    main()
