#!/usr/bin/env python

#
# Command Line Countdown Timer
#

# -------------------------

class ArgumentsParser:
    import argparse

    desc_str = 'Countdown timer'
    parser = argparse.ArgumentParser(description = desc_str)

    def parse_arguments(self):
        arguments = self.parser.parse_args()

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

    arguments_parser = ArgumentsParser()
    arguments_parser.parse_arguments()

main()
