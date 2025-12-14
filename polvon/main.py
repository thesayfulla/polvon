import argparse
import sys
import os

from .tui import PolvonApp
from . import __version__


def check_systemd():
    if not os.path.exists("/usr/bin/systemctl") and not os.path.exists("/bin/systemctl"):
        print("Error: systemctl not found. This tool requires systemd.", file=sys.stderr)
        return False
    return True


def main():
    """Main function to start the Polvon CLI."""
    parser = argparse.ArgumentParser(
        prog="polvon",
        description="Polvon - CLI tool for managing Linux systemd services",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Keyboard shortcuts:
  q          - Quit
  r          - Refresh service list
  a          - Toggle between all services and active services
  /          - Focus search input to filter services
  Esc        - Clear search and return to service list
  s          - Start selected service
  Shift+S    - Stop selected service
  Shift+R    - Restart selected service
  e          - Enable selected service
  d          - Disable selected service
  v          - View status of selected service
  l          - View logs of selected service
  ↑/↓        - Navigate through services
        """
    )
    
    parser.add_argument(
        "--sudo",
        action="store_true",
        help="Use sudo for systemctl commands (required for service management without root)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s v{__version__}",
    )
    
    args = parser.parse_args()
    
    # Check if systemd is available
    if not check_systemd():
        sys.exit(1)
    
    if not args.sudo and os.geteuid() != 0:
        print("Note: Running without sudo. You may need --sudo flag for service management.")
        print("      Some operations may fail without proper permissions.\n")
    
    try:
        app = PolvonApp(use_sudo=args.sudo)
        app.run()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
