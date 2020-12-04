#!/usr/bin/env python

#
# Command Line Countdown Timer
#

# -------------------------

class ArgumentsParser:

    def __init__(self):
        import argparse

        self.desc_str = 'Countdown Timer - command line utility'
        self.parser = argparse.ArgumentParser(description = self.desc_str)

        self.init_arguments()

    def init_arguments(self):
        self.add_start_from_argument(default_start_from = 30)

    def add_start_from_argument(self, default_start_from):
        self.parser.add_argument('--start_from',
                                 metavar='start_from_minutes',
                                 default=default_start_from,
                                 type=int,
                                 help='initial countdown value (minutes)')

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
