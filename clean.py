#!/usr/bin/python3

import argparse, os, fnmatch

def question_yn(prompt):
    """Ask the user for a yes/no answer
    
    The user is stuck in a loop while he doesn't answer "y" or "n".
    The same question <prompt> will be asked each time."""

    answer = input(prompt) 
    while (answer != "n" and answer != "y"): 
        print("Please answer y for yes or n for no.")
        answer = input(prompt)
    return (answer =="y")

def security(to_clean, files, patterns, args):
    """Try to prevent the user from making big mistakes
    
    if the user is about to remove 5 or more files, ask if he's sure."""

    if len(to_clean) >= 5:
        if args.force and not question_yn("You're about to remove {} files. Do you want to continue ? ".format(len(to_clean))):
            return True

    if len(to_clean) >= len(files)//2+2:
        print("You're about to remove {} out of {} files.".format(len(to_clean), len(files)))
        if not question_yn("Is it really what you want to do ? "):
            return True

    return False

def list_files(directories, recursive=False):
    """return the list of files in directory with full path

    return only files, not directory
    Can be recursive"""
    lst = list()
    for directory in directories:
        for file in os.listdir(directory):
            filepath = os.path.join(directory, file)
            if os.path.isdir(filepath) and recursive:
                lst += list_files([filepath], recursive)
            elif os.path.isfile(filepath):
                lst += [filepath]
    return lst

def read_pattern_file(fullpath):
    """return the list of patterns in a file

    The file must have one pattern by line"""

    with open(fullpath) as file:
        l = list(map(str.strip, file.readlines()))
    return l

def init():
    """initialize the default configuration if not present

    create the directory clean in $HOME/.config and write a default file containing the default configuration"""

    if not (os.path.isdir(dir_config)):
        os.makedirs(dir_config)
        with open(dir_config + "default", mode='w') as default:
            default.write("#*#\n*~\n")
        print("Created a default configuration")
    

def select_patterns(list_files):
    """function used to find which list of pattern the program will use

    if the argument given is None, use the default config file.
    Else, combine all the config files given."""

    dir_config = os.getenv("HOME") + "/.config/clean/"
    
    pattern_list = list()
    if (list_files == None):
        return read_pattern_file(dir_config + "default")
    for config in list_files:
        pattern_list += read_pattern_file(dir_config + config)
    return list(set(pattern_list))

def select_files_to_clean(pattern_list, file_list):
    """Return all the files in file_list that match at least one of the patterns in pattern_list

    Filter the files to be clean.
    Can probably be done faster, but it's not the priority."""
    result = list()
    for file in file_list:
        for pattern in pattern_list:
            if fnmatch.fnmatch(os.path.basename(file), pattern):
                result += [file]
    return result

def remove(to_clean, force, verbose):
    """Remove a file, respecting the given options

    The force option skip the question, and the verbose option print which file have been removed."""
    for file in to_clean:
        removed = False
        if not force: 
            if question_yn("Do you want to remove {} ? ".format(file)):
                os.remove(file)
                removed = True
        else:
            os.remove(file)
            removed = True
        if (verbose and removed):
            print("Removed {}.".format(file))

def run(args):
    """run the program

    Launch one by one all the important functions of the program."""

    # patterns part
    if args.pattern:
        pattern_list = args.pattern
        if args.configuration:
            pattern_list += select_patterns(args.configuration)
    else:
        pattern_list = select_patterns(args.configuration)

    cibles = args.target if args.target != [] else [os.getenv("PWD", '.')]

    file_list = list_files(cibles, args.recursive)

    to_clean = select_files_to_clean(pattern_list, file_list)

    if(security(to_clean, file_list, pattern_list, args)):
        return False

    remove(to_clean, args.force, args.verbose)

def main():
    """Parse the arguments and pass it to run"""
    version = 0.7
    parser = argparse.ArgumentParser(prog="clean")
    parser.add_argument("--version", action="version", version="%(prog)s {}".format(version))
    parser.add_argument("-f", "--force", action="store_true", help="Don't prompt the user before removal")
    parser.add_argument("-v", "--verbose", action="store_true", help="Explain what is being done")
    parser.add_argument("-r", "--recursive", action="store_true", help="Make a recursive clean")
    parser.add_argument("-p", "--pattern", action="append", help="Use these patterns instead of pattern files")
    parser.add_argument("-c", "--configuration", action="append", help="Use the specified config file")
    parser.add_argument("target", nargs="*", help="The directories to clean")
    run(parser.parse_args())

if __name__ == '__main__':
    main()
