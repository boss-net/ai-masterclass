import os
import subprocess
import sys


def get_project_root():
    """Get the project root directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)


def ensure_uv():
    """Ensure uv is installed."""
    try:
        # First try to find uv in PATH
        result = subprocess.run(["which", "uv"], capture_output=True, text=True)
        if result.returncode == 0:
            print("uv found at:", result.stdout.strip())
            return

        # If not found, try to install it
        print("Installing uv...")
        subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)

        # Get Python version
        python_version = f"Python{sys.version_info.major}.{sys.version_info.minor}"

        # Try different possible paths for uv
        possible_paths = [
            os.path.expanduser(f"~/Library/Python/3.8/bin/uv"),
            os.path.expanduser(f"~/Library/Python/{python_version}/bin/uv"),
            os.path.join(os.path.dirname(sys.executable), "uv"),
            os.path.expanduser(f"~/.local/bin/uv"),
        ]

        # Check each path
        for uv_path in possible_paths:
            if os.path.exists(uv_path):
                print(f"Found uv at: {uv_path}")
                # Add the containing directory to PATH
                bin_dir = os.path.dirname(uv_path)
                os.environ["PATH"] = f"{bin_dir}:{os.environ['PATH']}"
                return

        raise FileNotFoundError("Could not find uv executable after installation")
    except Exception as e:
        print(f"Error installing uv: {e}")
        raise


def init_uv_project():
    """Initialize uv project."""
    project_root = get_project_root()
    print(f"Initializing uv project in {project_root}...")
    try:
        # Try to run uv directly
        subprocess.run(["uv", "init"], check=True, cwd=project_root)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to initialize uv project: {e}")
        return False
    return True


def run_uv(command):
    """Run a uv command with error handling."""
    try:
        # Use the fixed path for Python 3.8
        uv_path = os.path.expanduser("~/.local/bin/uv")

        if not os.path.exists(uv_path):
            raise FileNotFoundError(f"uv executable not found at {uv_path}")

        # Get the project root
        project_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        # Run uv command with workspace configuration
        result = subprocess.run(
            [uv_path, "--verbose", "--directory", project_root] + command.split(),
            check=True,
            capture_output=True,
            text=True,
        )

        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running uv command: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        raise
