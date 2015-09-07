import os
import fnmatch
import functools

class PatternFile:
    """Handler for files containing patterns"""

    # Default pattern directory
    PATTERN_DIR = os.path.join(os.getenv('HOME', './'), '.config/clean/')
    
    def __init__(self, name, allow_env = True, mode='r'):
        
        # Find the directory to store patterns
        if allow_env and 'CLEAN_PATTERN' in os.environ:
            config_dir = os.getenv('CLEAN_PATTERN')
        else:
            config_dir = self.PATTERN_DIR

        # Create the directory if he doesn't exist
        if not os.path.isdir(config_dir):
            os.makedirs(config_dir)

        # Append filename to config_dir
        self.fullpath = os.path.join(config_dir, name + '.ptrn')

        self.mode = mode


    def __iter__(self):
        """Iterator on the patterns stored in the pattern file"""

        # Create the file if he doesn't exist
        if not os.path.exists(self.fullpath):
            open(self.fullpath, 'a').close()

        with open(self.fullpath) as file:
            for pattern in file:
                yield pattern.strip()


    def __next__(self):
        try:
            return next(self.pattern_iterator)
        except StopIteration:
            self.pattern_file.close()
            raise


    def __enter__(self):
        """Return file handler, open with the mode given at initialisation"""

        self.file = open(self.fullpath, self.mode)
        return self.file


    def __exit__(self, type, value, traceback):
        self.file.close()

class CleaningFile:

    # Asking user
    prompt = 'Do your really want to remove {} ? '
    yes = ['yes', 'y']

    # Informing user
    removal_log = "{} has been removed"

    def __init__(self, fullpath, verbose=False, force=False):
        self.fullpath = fullpath
        self.verbose = verbose
        self.force = force

    def remove(self):
        """Remove the file"""

        # Has it been removed ?
        removed = False

        if not self.force:
            # Ask the user before removal
            if input(self.prompt.format(self.fullpath)).lower() in self.yes:
                os.remove(self.fullpath)
                removed = True
        else: # If self.force
            os.remove(self.fullpath)
            removed = True

        if self.verbose and removed:
            print(self.removal_log.format(self.fullpath))

class CleaningRequest:

    def __init__(self, patterns, directories=None, recursive=False):
        self.patterns = patterns
        self.directories = directories
        self.recursive = recursive


    def recursive_cleaning(self, directory):
        for root, dirs, files in os.walk(directory):
            fullpath = lambda f: os.path.join(root, f)
            rv = list(map(fullpath, self.match_files(files)))
            for directory in dirs:
                rv.extend(self.recursive_cleaning(directory))
            return rv
        return list()


    def flat_cleaning(self, directory):
        return self.match_files(os.listdir(directory))


    def __call__(self, directory, recursive=False):
        if recursive:
            return self.recursive_cleaning(directory)
        return self.flat_cleaning(directory)


    def match_files(self, entities):
        entities = set(entities)

        for pattern in self.patterns:
            matched_files = set(fnmatch.filter(entities, pattern))
            entities = entities.symmetric_difference(matched_files)
            yield from matched_files


    def __iter__(self):

        if not self.directories:
            self.directories = list()

        for directory in self.directories:
            for file in self(directory, self.recursive):
                yield file
