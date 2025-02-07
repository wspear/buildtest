import os
import shutil

from buildtest.cli.build import resolve_testdirectory
from buildtest.defaults import (
    BUILD_HISTORY_DIR,
    BUILD_REPORT,
    BUILDSPEC_CACHE_FILE,
    BUILDTEST_REPORTS,
)
from buildtest.utils.file import is_dir, is_file
from rich.prompt import Prompt


def clean(configuration, yes):
    """Entry point for ``buildtest clean`` command which will clean up directories and configuration files generated by buildtest.
    User will be prompted for series of question with (Y/N) to select response to each action which can be ignored by passing ``--yes`` option.

    Args:
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class
        yes (bool): boolean to control whether user response is required before cleaning up tasks.
    """
    remove_report = "y"
    remove_history = "y"
    remove_buildspec_cache = "y"
    remove_testdir = "y"

    resolved_testdir = resolve_testdirectory(configuration)

    # request user prompt when 'buildtest clean' is specified without '-y' option. Default selection is 'y' for confirmation
    if not yes:

        remove_testdir = Prompt.ask(
            f"Remove Test Directory {resolved_testdir}",
            default="y",
            choices=["y", "n"],
            show_choices=True,
        )

        remove_report = Prompt.ask(
            f"Remove Report File {BUILD_REPORT}",
            default="y",
            choices=["y", "n"],
            show_choices=True,
        )

        remove_history = Prompt.ask(
            f"Remove History Directory {BUILD_HISTORY_DIR}",
            default="y",
            choices=["y", "n"],
            show_choices=True,
        )
        remove_buildspec_cache = Prompt.ask(
            f"Remove Buildspec Cache {BUILDSPEC_CACHE_FILE}",
            default="y",
            choices=["y", "n"],
            show_choices=True,
        )

    if remove_testdir == "y":
        print("======> Remove Test Directory")
        if is_dir(resolved_testdir):
            shutil.rmtree(resolved_testdir)

    if remove_report == "y":
        print("======> Removing Report File")
        if is_file(BUILD_REPORT):
            os.remove(BUILD_REPORT)
        if is_file(BUILDTEST_REPORTS):
            os.remove(BUILDTEST_REPORTS)

    if remove_history == "y":
        print("======> Removing History Directory")
        if is_dir(BUILD_HISTORY_DIR):
            shutil.rmtree(BUILD_HISTORY_DIR)

    if remove_buildspec_cache == "y":
        print("======> Removing buildspec cache")
        if is_file(BUILDSPEC_CACHE_FILE):
            os.remove(BUILDSPEC_CACHE_FILE)
