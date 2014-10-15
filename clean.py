#!/usr/bin/python3

import argparse, os, fnmatch

def question_yn(prompt):
    """Ask the user for a yes/no answer"""
    answer = input(prompt)
    while (answer != "n" and answer != "y"):
        print("Please answer y for yes or n for no.")
        answer = input(prompt)
    return (answer =="y")

def security(to_clean, files, patterns, args):
    if len(to_clean) >= 5:
        if args.force and not question_yn("You're about to remove {} files. Do you want to continue ? ".format(len(to_clean))):
            return True
    return (False)

def list_files(directories, recursive=False):
    """return the list of files in directory with full path"""
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
    """return the list of patterns in a file"""
    with open(fullpath) as file:
        l = list(map(str.strip, file.readlines()))
    return l

def pattern_to_use():
    """function used to find which list of pattern the program will use"""
    dir_config = os.getenv("HOME") + "/.config/clean/"
    pattern_list = list()
    if not (os.path.isdir(dir_config)):
        os.makedirs(dir_config)
        with open(dir_config + "default", mode='w') as default:
            default.write("#*#\n*~\n")
        print("Created a default configuration")
    return read_pattern_file(dir_config + "default")

def select_files_to_clean(pattern_list, file_list):
    """Return all the files in file_list that match at least one of the patterns in pattern_list"""
    return [file for pattern in pattern_list for file in file_list if fnmatch.fnmatch(file, pattern)]

def remove(to_clean, force, verbose):
    """Remove a file, respecting the given options"""
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
    """run the program"""
    pattern_list = args.pattern if args.pattern else pattern_to_use()

    cibles = args.target if args.target != [] else [os.getenv("PWD", '.')]

    file_list = list_files(cibles, args.recursive)

    to_clean = select_files_to_clean(pattern_list, file_list)

    if(security(to_clean, file_list, pattern_list, args)):
        return False

    remove(to_clean, args.force, args.verbose)

def main():
    """Parse the arguments and pass it to run"""
    version = 0.4
    parser = argparse.ArgumentParser(prog="clean")
    parser.add_argument("--version", action="version", version="%(prog)s {}".format(version))
    parser.add_argument("-f", "--force", action="store_true", help="Don't prompt the user before removal")
    parser.add_argument("-v", "--verbose", action="store_true", help="Explain what is being done")
    parser.add_argument("-p", "--pattern", action="append", help="Use these patterns instead of pattern files")
    parser.add_argument("-r", "--recursive", action="store_true", help="Make a recursive clean")
    parser.add_argument("target", nargs="*", help="The directories to clean")
    run(parser.parse_args())

if __name__ == '__main__':
    main()
