import subprocess
import sys


def install(package):
    """
    Install a pip package.

    Args:
        package (str): The package to install.
    """
    command = [sys.executable, "-m", "pip", "install", package]
    try:
        subprocess.check_call(command)
    except subprocess.CalledProcessError as e:
        print(f"Installation failed for {package}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    install("pruna_pro")
    install("pruna[stable-fast]")
