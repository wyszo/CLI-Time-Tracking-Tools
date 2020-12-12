#
# Command Line Countdown Timer
#
# -------------------------

class Timer:
    DEFAULT_PAUSED_MESSAGE="Paused - press [Enter] to unpause or Ctrl-C to quit"

    def __init__(self, time_in_min, pause_message=None):
        self.total_time_in_min = int(time_in_min)
        self.remaining_time_in_sec = int(time_in_min) * 60

        if pause_message is None:
            pause_message = self.DEFAULT_PAUSED_MESSAGE
        self.pause_message = "\n" + pause_message + "\n"

    def tick(self):
        from shared import print_inline
        text = 'timer tick: ' + str(self.remaining_time_in_sec) + 's'
        print_inline(text)
        self.remaining_time_in_sec -= 1

    def sleep_1_sec(self):
        import time
        time.sleep(1)

    def pause_or_abort(self):
        abort = False
        try:
            input_value = raw_input(self.pause_message)
        except KeyboardInterrupt:
            print
            abort = True

        return abort

    def start(self):
        should_quit = False
        while not should_quit:
            try:
                while(True):
                    self.tick()
                    self.sleep_1_sec()
            except KeyboardInterrupt:
                should_quit = self.pause_or_abort()

