"""
Main entry point for the bosskit CLI.
"""

import argparse
import sys
from typing import List

from bosskit import __version__


def main(argv: List[str] = None) -> int:
    """Main CLI entry point."""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="BossNet AI Agent Toolkit",
        epilog="For more information, see https://bosskit.readthedocs.io/",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    # Add subcommands
    subparsers = parser.add_subparsers(dest="command", title="commands")

    # Example command
    example_parser = subparsers.add_parser(
        "example",
        help="Example command",
    )
    example_parser.add_argument(
        "--message",
        type=str,
        help="Message to display",
        default="Hello, World!",
    )

    args = parser.parse_args(argv)

    if args.command == "example":
        print(args.message)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
