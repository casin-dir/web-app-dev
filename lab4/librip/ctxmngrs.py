import time


class timer:
    def __enter__(self):
        time.clock()

    def __exit__(self, exp_type, exp_value, traceback):
        print(time.clock())
