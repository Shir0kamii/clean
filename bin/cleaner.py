#! /usr/bin/env python3

from clize import run
from clean_directories import files

__prog__ = 'cleaner'
__version__ = 0.1

def version():
    """Print the version of the script"""
    return "{0} {1}".format(__prog__, __version__)


def main(configuration, *directories,
        non_recursive:'n'=False, verbose:'v'=False, force:'p'=False):

    if len(directories) == 0:
        directories = ('.',)

    patterns = list(files.PatternFile(configuration))

    request = files.CleaningRequest(patterns, directories, not non_recursive)

    for file in request:
        files.CleaningFile(file, verbose, force).remove()

if __name__ == '__main__':
    run(main, alt=version)
