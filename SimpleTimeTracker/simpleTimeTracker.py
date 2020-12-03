#!/usr/bin/python

import os, sys
import time
import argparse

from logswriter import LogsWriter
from dateformatter import DateFormatter

#
# A very simple time tracker. Tracks time spend on a single activity.
# (I don't know Python well, this script may contain silly code)
#

version = '1.0.5'

# TODO: get rid of those global vars
time_elapsed = 0
task_name = ''
logs_dir_name = 'logs'
income_per_hour = 0
currency = ''
already_earned = 0

# -------------------------

def add_shared_dir_to_path():
    import os, sys

    current_dir = os.path.dirname(__file__)
    shared_dir = os.path.join(current_dir, '../Shared')
    sys.path.append(shared_dir)

# -------------------------

def as_two_digits_string(nr):
    result = str(nr)
    if nr < 10:
        result = "0" + str(nr)
    return result


def format_time(in_time):
    hours = time_to_hours(in_time)
    minutes = time_to_minutes_after_full_hour(in_time)
    seconds = in_time - hours * 3600 - minutes * 60

    result = as_two_digits_string(hours) + ":"
    result += as_two_digits_string(minutes) + ":"
    result += as_two_digits_string(seconds)

    return result


def time_to_hours(in_time):
    return in_time/3600

def time_to_minutes_after_full_hour(in_time):
    return (in_time % 3600) / 60

def count_time(task_name):
    add_shared_dir_to_path()
    import shared

    global time_elapsed
    global income_per_hour, currency

    time_step = 1 # sleeping time

    show_time_interval = 1 # update printed time info only after # seconds - it is NOT the same as time_step, don't mix those two
    ctr = 0

    while True:
        if ctr % show_time_interval == 0:

            income_line = ''
            if income_per_hour != 0:
                income_line = ". Earned " + str(money_earned()) + currency

            shared.print_inline(task_name + " - " + format_time(time_elapsed) + income_line)

        ctr += 1

        time.sleep(time_step)
        time_elapsed += time_step
    return

# -------------------------

def money_earned():
    global time_elapsed
    global income_per_hour, currency
    global already_earned

    money_earned_this_hour = int(income_per_hour * float(time_to_minutes_after_full_hour(time_elapsed)) / 60.0)
    money_earned_before_this_hour = already_earned + income_per_hour * time_to_hours(time_elapsed)
    return money_earned_this_hour + money_earned_before_this_hour

# -------------------------

def pause_or_abort():
    quit = False
    try:
        time_now = time.strftime("%H:%M", time.localtime())
        input_msg = "\n/Paused (" + time_now + ")/ - press [enter] to unpause or ^C to quit\n"
        temp = raw_input(input_msg)
    except KeyboardInterrupt:
        print
        quit = True

    print
    return quit

# -------------------------

def start():
    global version
    global time_elapsed, task_name

    print '\n-----------------------------------------'
    print 'A very simple Time Tracking Utility v' + str(version)
    print '-----------------------------------------\n'

    if not len(task_name):
        try:
            task_name = raw_input('Enter task name: ')
        except KeyboardInterrupt:
            quit = True
            print
            return
        print

    quit = False
    while not quit:
        try:
            while(1):
                count_time(task_name)
        except KeyboardInterrupt:
            quit = pause_or_abort()

# -------------------------

def print_time_parse_error():
    print 'Consult --help for supported time formats!'
    print 'Sorry, defaulting elapsed time to 0!'


def filtertime_str(time_str):
    # remove invalid characters
    allowedChars = ':hm'
    filteredStr = ''.join(c for c in time_str if c.isdigit() or c in allowedChars)

    # convert format HH'h'MM'm', convert to hh:mm
    str = filteredStr
    str = str.replace('h', ':')
    str = str.replace('m', '')

    return str


def setup_start_time(time_str):
    global time_elapsed

    # character validation & filtering
    if time_str == 0:
        return

    time_str = filtertime_str(time_str)

    # problably simple integer value
    if time_str.find(':') == -1:
        try:
            int_time = int(time_str)
            time_elapsed = int_time * 60 # convert value to # of minutes
        except ValueError:
            print 'Error: unknown time format!'
            print_time_parse_error()
            return
    # probably format hh:mm
    else:
        time = time_str.split(':')

        # check for unsupported characters # obsolete - done during filtering
        for c in time_str:
            if c.isdigit() == False and c != ':':
                print ("Error: unknown time format! Unsupported character: '" + c + "'")
                print_time_parse_error()
                return

        # validate time array length and element types
        if len(time) > 2 or (time[0].isdigit() == False) or (time[1].isdigit() == False):
            print "Error: unknown time format!"
            print_time_parse_error()
            return

        # everything seems fine, set elapsed time
        try:
            hours = int(time[0])
            minutes = int(time[1])
        except ValueError:
            print 'Error: unknown time format!'
            print_time_parse_error()
            return

        time_elapsed = hours * 3600 + minutes * 60

# -------------------------

def parse_args():
    global time_elapsed, task_name
    global income_per_hour, currency, already_earned

    start_time_arg_name = 'start_time'
    task_arg_name = 'task'
    income_per_hour_arg_name = 'income_per_hour'
    currency_arg_name = 'currency'
    already_earned_arg_name = 'already_earned'

    # prepare arg parser
    descStr = ("A very simple time tracker. Shows time spend on a single activity.\n\n"
              "Example usage: \n"
              "\tpython simpleTimeTracker.py --{} 'Gardening'\n".format(task_arg_name) +
              "\tpython simpleTimeTracker.py --{} 'Planning' --{} 3:10\n".format(task_arg_name, start_time_arg_name) +
              "\tpython simpleTimeTracker.py --{} 'Article writing' --{} 25 --{} '$'\n".format(task_arg_name, income_per_hour_arg_name, currency_arg_name) +
              "\tpython simpleTimeTracker.py --{} 'job' --{} 25 --{} $ --{} 125\n".format(task_arg_name, income_per_hour_arg_name, currency_arg_name, already_earned_arg_name)
              )

    parser = argparse.ArgumentParser(description = descStr, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--{}'.format(start_time_arg_name), metavar='StartTime', default=0, type=str, help='Start Time (in minutes or format HH:MM, eg: \'3:23\' or format with \'h\' and \'m\' characters, like \'3h15m\').')
    parser.add_argument('--{}'.format(task_arg_name), metavar='task_name', type=str, help='Name of the activity which you want to track')

    parser.add_argument('--{}'.format(income_per_hour_arg_name), metavar='income_per_hour', type=int, help='Amount of money earned every hour')
    parser.add_argument('--{}'.format(currency_arg_name), metavar='currency', type=str, help='Currency of money earned')
    parser.add_argument('--{}'.format(already_earned_arg_name), metavar='already_earned', type=int, help='Initial amount of money for total earnings calculation. Defaults to 0')

    # parse & handle args
    args = parser.parse_args()
    setup_start_time(args.start_time)

    # TODO: get rid of the global variables
    task_name = args.task
    if not task_name:
        task_name = ''

    income_per_hour = args.income_per_hour
    if not income_per_hour:
        income_per_hour = 0

    currency = args.currency
    if not currency:
        currency = ''

    already_earned = args.already_earned
    if not already_earned:
        already_earned = 0

    return

# -------------------------

def main():
    today = DateFormatter().today()

    writer = LogsWriter(logs_dir_name, today)
    writer.create_logs_dir()

    parse_args()
    start()
    return

# -------------------------

main()
