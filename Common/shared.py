#
# This file contains code shared between timer subprojects
#

def print_inline(text):
    """Print by replacing last line"""
    import sys
    to_print = '\r' + text
    sys.stdout.write(to_print)
    sys.stdout.flush()
