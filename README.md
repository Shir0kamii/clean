clean
=====

# Objective

The python script "clean" allow the user to clean directory off temporary files with its default behavior.
With anoter configuration, it can allow you to clean a working directory before committing.

The final goal is to provide multiple configurations to clean a directory the exact way you want it.

# Suggestion

The best way to use this script at its fullest is to place clean.py in a personnal bin directory.
For example, you can create a directory "bin" in your home and add it to the variable $PATH.
Then, place the binaries and script you want to execute them wherever you are.
You can of course rename clean.py to clean or another name you prefer.

# Important options

## Help

./clean -h or ./clean --help

Print basical informations to the user, with a summary of the available commands.

## Pattern

./clean -p PATTERN or ./clean --pattern PATTERN

Allow the user to search for one or more pattern, overridding the default patterns.
You can use this option multiple times. For example, this command imitate the normal behavior : "./clean.py -p '#*#' -p '*~'"

## Force

./clean -f or ./clean --force

Skip the prompt for all the files targeted.
Use this command with prudence, and verify that the command will not remove a file you want to keep.

## Recursive

./clean -r or ./clean --recursive

Make a recursion to clean every subdirectory found.
Usefull if your working directory is subdivised into multiple directories.