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
    import shared, version, settings
    shared.print_version(settings.printable_script_name, version.version)

main()
