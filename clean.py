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

def remove(to_clean):
    for file in to_clean:
        os.remove(file)

def run(args):
    """run the program"""
    pattern_list = pattern_to_use()
    cible = os.getenv("PWD", '.')
    file_list = list_file_fullpath(cible)
    to_clean = list_files_to_clean(pattern_list, file_list)
    remove(to_clean)

def main():
    """Parse the arguments and pass it to run"""
    version = 0.1
    parser = argparse.ArgumentParser(prog="clean")
    parser.add_argument("--version", action="version", version="%(prog)s {}".format(version))
    run(parser.parse_args())

if __name__ == '__main__':
    main()
