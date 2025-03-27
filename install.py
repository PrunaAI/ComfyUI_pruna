import subprocess
import sys

def install(package, extra_index_url=None):
    """
    Install a pip package, optionally using an extra index URL.
    
    Args:
        package (str): The package to install.
        extra_index_url (str, optional): URL of the extra package index.
    """
    command = [sys.executable, "-m", "pip", "install", package]
    if extra_index_url:
        command.extend(["--extra-index-url", extra_index_url])
    try:
        subprocess.check_call(command)
    except subprocess.CalledProcessError as e:
        print(f"Installation failed for {package}: {e}")
        sys.exit(1)

def ask_choice(prompt, choices, default=None):
    """
    Prompt the user to select from a list of choices.
    
    Args:
        prompt (str): The question to display.
        choices (list): List of valid choices.
        default (str, optional): The default choice if no input is given.
    
    Returns:
        str: The validated user choice.
    """
    choices_str = "/".join(
        [f"[{c}]" if c == default else c for c in choices]
    )
    while True:
        response = input(f"{prompt} ({choices_str}): ").strip().lower()
        if not response and default:
            return default
        if response in choices:
            return response
        print(f"Invalid choice. Please choose from: {', '.join(choices)}")

if __name__ == "__main__":
    # Ask the user which package to install
    pkg = ask_choice("Which package do you want to use?", ["pruna", "pruna_pro"], default="pruna")

    # Ask for CPU or GPU version
    hardware = ask_choice("For which hardware do you want to install the package?", ["gpu", "cpu"], default="gpu")
    extra_index_url = "https://download.pytorch.org/whl/cpu" if hardware == "cpu" else None


    print(f"\nInstalling: {pkg} for {hardware} ...")
    if hardware == "cpu":
        install(pkg, extra_index_url)
    else:
        install("pruna[stable-fast]")
        if pkg == "pruna_pro":
            install("pruna_pro")