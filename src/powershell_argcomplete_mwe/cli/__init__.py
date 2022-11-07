#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK


"""
Parses command line arguments and provides argument completion.
"""


import argparse
import codecs
import os
import sys
from pathlib import Path

import argcomplete

from ..__about__ import __version__


def subparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """
    Unifies the look of a subparser in the --help outpul.
    Avoids repeating the following definition pattern:
    ```
    {name}_sp: argparse.ArgumentParser = {name}_parser.add_subparsers(
        dest="{name}_command",
        title="{name} subcommands",
        metavar="<{NAME}_SUBCOMMAND>",
    )
    ```

    Instead, we can write:
    ```
    my_sp = subparser(my_parser)
    ```
    """
    name = parser.prog.split()[-1]
    new_sp = parser.add_subparsers(
        dest=f"{name}_command",
        title=f"{name} subcommands",
        metavar=f"<{name.upper()}_SUBCOMMAND>",
    )
    return new_sp


def argument_parser() -> argparse.ArgumentParser:
    """
    Defines the whole CLI
    """
    psamwe_parser = argparse.ArgumentParser(prog="psamwe")

    # Top-level arguments
    psamwe_parser.add_argument(
        "-v",
        "--version",
        action="version",
        help="show psamwe version",
        version=f"%(prog)s {__version__}",
    )
    psamwe_parser.add_argument(
        "-a",
        "--about",
        action="store_true",
        help="show more information about psamwe",
    )
    psamwe_sp = subparser(psamwe_parser)

    # shave command
    shave = psamwe_sp.add_parser(
        "shave",
        help="shave an animal",
        description="shave an animal",
    )
    shave.add_argument(
        "animal",
        metavar="ANIMAL",
        choices=("yak", "sheep"),
        help="animal to shave, choices: %(choices)s",
    )
    shave.add_argument("--manually", action="store_true")
    shave.add_argument("--quickly", action="store_true")

    # milk command
    milk = psamwe_sp.add_parser(
        "milk",
        help="milk an animal",
        description="milk an animal",
    )
    milk.add_argument(
        "animal",
        metavar="ANIMAL",
        choices=("yak", "sheep"),
        help="animal to shave, choices: %(choices)s",
    )
    milk.add_argument("--carefully", action="store_true")
    milk.add_argument("--lovingly", action="store_true")

    return psamwe_parser


def run(args: argparse.Namespace) -> None:
    """
    Main CLI logic
    """
    print(f"{args}")


def main() -> None:  # no cov
    """
    Provides CLI argument completion, parses CLI arguments,
    and passes them to an entry point
    """
    parser = argument_parser()
    output_stream = None
    if "_ARGCOMPLETE_POWERSHELL" in os.environ:
        output_stream = codecs.getwriter("utf-8")(sys.stdout.buffer)
    argcomplete.autocomplete(parser, output_stream=output_stream)
    args = parser.parse_args()
    sys.exit(run(args))
