import os
import sys
import typing as t

import configargparse
import git

from bosskit import __version__, models
from bosskit.coders import Coder
from bosskit.io import InputOutput


def get_git_root() -> t.Optional[str]:
    """Get the git root directory for the current working directory.

    Returns:
        str: Path to git root directory, or None if not in a git repository.
    """
    try:
        repo = git.Repo(search_parent_directories=True)
        return repo.working_tree_dir
    except git.InvalidGitRepositoryError:
        return None


def main(args: t.Optional[t.List[str]] = None, input: t.Optional[t.TextIO] = None, output: t.Optional[t.TextIO] = None) -> None:
    """Main entry point for the bosskit command-line interface.

    Args:
        args: Command line arguments (default: sys.argv[1:])
        input: Input stream (default: None)
        output: Output stream (default: None)
    """
    if args is None:
        args = sys.argv[1:]  # type: ignore

    git_root = get_git_root()

    default_config_files: t.List[str] = [
        os.path.expanduser("~/.bosskit.conf.yml"),
    ]
    if git_root:
        default_config_files.insert(0, os.path.join(git_root, ".bosskit.conf.yml"))

    parser = configargparse.ArgumentParser(
        description="BossKit is GPT powered coding in your terminal",
        add_config_file_help=True,
        default_config_files=default_config_files,
        config_file_parser_class=configargparse.YAMLConfigFileParser,
        auto_env_var_prefix="BOSSKIT_",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the version number and exit",
    )

    parser.add_argument(
        "-c",
        "--config",
        is_config_file=True,
        metavar="CONFIG_FILE",
        help=("Specify the config file (default: search for .bosskit.conf.yml in git root or home" " directory)"),
    )

    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="a list of source code files (optional)",
    )
    default_input_history_file = os.path.join(git_root, ".bosskit.input.history") if git_root else ".bosskit.input.history"
    default_chat_history_file = os.path.join(git_root, ".bosskit.chat.history.md") if git_root else ".bosskit.chat.history.md"

    parser.add_argument(
        "--input-history-file",
        metavar="INPUT_HISTORY_FILE",
        default=default_input_history_file,
        help=f"Specify the chat input history file (default: {default_input_history_file})",
    )
    parser.add_argument(
        "--chat-history-file",
        metavar="CHAT_HISTORY_FILE",
        default=default_chat_history_file,
        help=f"Specify the chat history file (default: {default_chat_history_file})",
    )
    parser.add_argument(
        "--model",
        metavar="MODEL",
        default=models.GPT4.name,
        help=f"Specify the model to use for the main chat (default: {models.GPT4.name})",
    )
    parser.add_argument(
        "-3",
        action="store_const",
        dest="model",
        const=models.GPT35_16k.name,
        help=f"Use {models.GPT35_16k.name} model for the main chat (gpt-4 is better)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        default=True,
        help="Enable pretty, colorized output (default: True)",
    )
    parser.add_argument(
        "--no-pretty",
        action="store_false",
        dest="pretty",
        help="Disable pretty, colorized output",
    )
    parser.add_argument(
        "--user-input-color",
        default="green",
        help="Set the color for user input (default: green)",
    )
    parser.add_argument(
        "--tool-output-color",
        default=None,
        help="Set the color for tool output (default: None)",
    )
    parser.add_argument(
        "--tool-error-color",
        default="red",
        help="Set the color for tool error messages (default: red)",
    )
    parser.add_argument(
        "--assistant-output-color",
        default="blue",
        help="Set the color for assistant output (default: blue)",
    )
    parser.add_argument(
        "--apply",
        metavar="FILE",
        help="Apply the changes from the given file instead of running the chat (debug)",
    )
    parser.add_argument(
        "--auto-commits",
        action="store_true",
        dest="auto_commits",
        default=True,
        help="Enable auto commit of GPT changes (default: True)",
    )

    parser.add_argument(
        "--no-auto-commits",
        action="store_false",
        dest="auto_commits",
        help="Disable auto commit of GPT changes (implies --no-dirty-commits)",
    )
    parser.add_argument(
        "--dirty-commits",
        action="store_true",
        dest="dirty_commits",
        help="Enable commits when repo is found dirty",
        default=True,
    )
    parser.add_argument(
        "--no-dirty-commits",
        action="store_false",
        dest="dirty_commits",
        help="Disable commits when repo is found dirty",
    )
    parser.add_argument(
        "--openai-api-key",
        metavar="OPENAI_API_KEY",
        help="Specify the OpenAI API key",
        env_var="OPENAI_API_KEY",
    )
    parser.add_argument(
        "--openai-api-base",
        metavar="OPENAI_API_BASE",
        default="https://api.openai.com/v1",
        help="Specify the OpenAI API base endpoint (default: https://api.openai.com/v1)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without applying changes (default: False)",
        default=False,
    )
    parser.add_argument(
        "--show-diffs",
        action="store_true",
        help="Show diffs when committing changes (default: False)",
        default=False,
    )
    parser.add_argument(
        "--map-tokens",
        type=int,
        default=1024,
        help="Max number of tokens to use for repo map, use 0 to disable (default: 1024)",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Always say yes to every confirmation",
        default=False,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
        default=False,
    )
    args = parser.parse_args(args)

    io = InputOutput(
        args.pretty,
        args.yes,
        args.input_history_file,
        args.chat_history_file,
        input=input,
        output=output,
        user_input_color=args.user_input_color,
        tool_output_color=args.tool_output_color,
        tool_error_color=args.tool_error_color,
    )

    if args.verbose:
        show = parser.format_values()
        io.tool_output(show)
        io.tool_output("Option settings:")
        for arg, val in sorted(vars(args).items()):
            io.tool_output(f"  - {arg}: {val}")

    io.tool_output(*sys.argv, log_only=True)

    if not args.openai_api_key:
        io.tool_error("No OpenAI API key provided. Use --openai-api-key or env OPENAI_API_KEY.")
        return 1

    coder = Coder(
        io,
        main_model=args.model,
        fnames=args.files,
        pretty=args.pretty,
        show_diffs=args.show_diffs,
        auto_commits=args.auto_commits,
        dirty_commits=args.dirty_commits,
        dry_run=args.dry_run,
        map_tokens=args.map_tokens,
        verbose=args.verbose,
        openai_api_key=args.openai_api_key,
        openai_api_base=args.openai_api_base,
        assistant_output_color=args.assistant_output_color,
    )

    if args.dirty_commits:
        coder.commit(ask=True, which="repo_files")

    if args.apply:
        with open(args.apply, "r") as f:
            content = f.read()
        coder.apply_updates(content)
        return

    io.tool_output("Use /help to see in-chat commands.")
    coder.run()


if __name__ == "__main__":
    status = main()
    sys.exit(status)
