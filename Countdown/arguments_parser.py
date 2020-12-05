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
                                 type=int,
                                 help='initial countdown value (minutes)')

    def parse_arguments(self):
        arguments = self.parser.parse_args()
        self.start_from = arguments.start_from

