#!/usr/bin/env python

#
# A simple command line countdown timer
#

# -------------------------

def main():
    import os, sys
    current_dir = os.path.dirname(__file__)
    shared_dir = os.path.join(current_dir, '../Shared')
    sys.path.append(shared_dir)

    import shared, version
    shared.print_version('Countdown Timer', version.version)

main()
