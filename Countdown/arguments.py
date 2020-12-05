#
# Command Line Countdown Timer
#
# -------------------------

def parse_script_arguments_or_ask():
    """
    Parses the cli script arguments and asks for missing ones

    Returns:
        int: start_from (time in minutes)
    """
    import arguments_parser
    arguments_parser = arguments_parser.ArgumentsParser()
    arguments_parser.parse_arguments()

    import shared
    start_from = arguments_parser.start_from
    if start_from is None:
        start_from = shared.try_read_keyboard_input('Enter time (in min): ')

    return start_from

