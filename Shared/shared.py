#
# This file contains code shared between timer subprojects
#

def print_inline(text):
    """
    Print by replacing current line
    """
    import sys
    to_print = '\r' + text
    sys.stdout.write(to_print)
    sys.stdout.flush()

def print_version(script_name, script_version):
    """
    Print script name and version applying default formatting
    """
    print '\n' + script_name + ' v' + str(script_version)

