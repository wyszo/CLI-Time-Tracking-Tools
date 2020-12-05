#
# cli-tools
# This file contains code shared between timer subprojects
#
# -------------------------

def print_inline(text):
    """
    Print by replacing current line
    """
    import sys
    to_print = '\r' + text
    sys.stdout.write(to_print)
    sys.stdout.flush()

# -------------------------

def print_version(script_name, script_version, newline=True):
    """
    Print script name and version applying default formatting
    """
    newline_char = ''

    if newline:
        newline_char = '\n'
    print newline_char + script_name + ' v' + str(script_version)

# -------------------------

def try_read_keyboard_input(text):

    try:
        input = raw_input(text)
    except KeyboardInterrupt:
        print
        import sys
        sys.exit()
    return input

# -------------------------
