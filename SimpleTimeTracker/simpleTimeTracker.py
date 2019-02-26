
import os, sys
import time
import argparse

from logswriter import LogsWriter
from dateformatter import DateFormatter

#
# A very simple time tracker. Tracks time spend on a single activity.
# (I don't know Python well, this script may contain silly code)
#

version = 1.04
time_elapsed = 0
task_name = ''
logs_dir_name = 'logs'

# -------------------------

def as_two_digits_string(nr):
    result = str(nr)
    if nr < 10:
        result = "0" + str(nr)
    return result


def format_time(in_time):
    hours = in_time/3600
    minutes = (in_time % 3600) / 60
    seconds = in_time - hours * 3600 - minutes * 60

    result = as_two_digits_string(hours) + ":"
    result += as_two_digits_string(minutes) + ":"
    result += as_two_digits_string(seconds) 

    return result 


def count_time(task_name):
    global time_elapsed

    time_step = 1 # sleeping time

    show_time_interval = 1 # update printed time info only after # seconds - it is NOT the same as time_step, don't mix those two
    ctr = 0
    
    while True:
        if ctr % show_time_interval == 0:
            print task_name + " - " + format_time(time_elapsed)
        ctr += 1

        time.sleep(time_step)
        time_elapsed += time_step
    return

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
    
    # prepare arg parser
    descStr = "A very simple time tracker. Shows time spend on a single activity."
    parser = argparse.ArgumentParser(description = descStr)
    
    parser.add_argument('--time', metavar='StartTime', default=0, type=str, help='Start Time (in minutes or format HH:MM, eg: \'3:23\' or format with \'h\' and \'m\' characters, like \'3h15m\').')
    parser.add_argument('--task', metavar='task_name', type=str, help='Name of the activity which you want to track')
    
    # parse & handle args
    args = parser.parse_args()
    setup_start_time(args.time)
    task_name = args.task
    if not task_name:
        task_name = ''
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
