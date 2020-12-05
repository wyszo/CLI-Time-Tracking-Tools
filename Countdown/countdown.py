#!/usr/bin/env python

#
# Command Line Countdown Timer
#
# -------------------------

def add_shared_dir_to_path():
    import os, sys

    current_dir = os.path.dirname(__file__)
    shared_dir = os.path.join(current_dir, '../Shared')
    sys.path.append(shared_dir)

# -------------------------

def main():
    add_shared_dir_to_path()
    import header
    header.print_header()

    import arguments
    start_from = arguments.parse_script_arguments_or_ask()
    import timer
    timer = timer.Timer(start_from)

main()
