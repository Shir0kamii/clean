#!/usr/bin/python3

import argparse

def run(args):
    pass

def main():
    version = 0.1
    parser = argparse.ArgumentParser(prog="clean")
    parser.add_argument("--version", action="version", version="%(prog)s {}".format(version))
    run(parser.parse_args())

if __name__ == '__main__':
    main()
