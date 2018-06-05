#! /usr/bin/env python3

from clize import run
from clean_directories import PatternFile, CleaningFile, CleaningRequest

__prog__ = 'cleaner'
__version__ = 0.1

def version():
    """Print the version of the script"""
    return "{0} {1}".format(__prog__, __version__)


def edit(pattern_name):
    PatternFile(pattern_name).edit()


def _main(configuration, *directories,
        non_recursive:'n'=False, verbose:'v'=False, force:'p'=False):
    """

    non_recursive: Don't make a recursive walk

    verbose: Print what the script is doing

    force: Don't ask the user before removal
    """

    # Default parameter
    if len(directories) == 0:
        directories = ('.',)

    # Read patterns
    patterns = list(PatternFile(configuration))

    # Creating and processing the request
    request = CleaningRequest(patterns, directories, not non_recursive)
    for file in request:
        CleaningFile(file, verbose, force).remove()

def main():
    run(_main, alt=[version, edit])

if __name__ == '__main__':
    main()
