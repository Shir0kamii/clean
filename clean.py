#!/usr/bin/python3

import argparse, os, fnmatch

def list_file_fullpath(directory):
    """return the list of files in directory with full path"""
    _ = [os.path.join(directory, file) for file in os.listdir(directory)]
    return [file for file in _ if os.path.isfile(file)]

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

def list_files_to_clean(pattern_list, file_list):
    """Return all the files in file_list that match at least one of the patterns in pattern_list"""
    return [file for pattern in pattern_list for file in file_list if fnmatch.fnmatch(file, pattern)]

def ask_user_before_remove(file):
    prompt = "Do you want to remove {} ? "
    prompt = prompt.format(file)
    answer = input(prompt)
    while (answer != "n" and answer != "y"):
        print("Please answer y for yes or n for no.")
        answer = input(prompt)
    return (answer == 'y')

def remove(to_clean, force, verbose):
    for file in to_clean:
        removed = False
        if not force: 
            if ask_user_before_remove(file):
                os.remove(file)
                removed = True
        else:
            os.remove(file)
            removed = True
        if (verbose and removed):
            print("Removed {}.".format(file))

def run(args):
    """run the program"""
    pattern_list = pattern_to_use()
    cible = os.getenv("PWD", '.')
    file_list = list_file_fullpath(cible)
    to_clean = list_files_to_clean(pattern_list, file_list)
    remove(to_clean, args.force, args.verbose)

def main():
    """Parse the arguments and pass it to run"""
    version = 0.2
    parser = argparse.ArgumentParser(prog="clean")
    parser.add_argument("--version", action="version", version="%(prog)s {}".format(version))
    parser.add_argument("-f", "--force", action="store_true", help="Don't prompt the user before removal")
    parser.add_argument("-v", "--verbose", action="store_true", help="Explain what is being done")
    run(parser.parse_args())

if __name__ == '__main__':
    main()
