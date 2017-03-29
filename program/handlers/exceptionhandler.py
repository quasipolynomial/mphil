
class TimeoutError(Exception):
    pass

def signal_handler(signum, frame):
    raise TimeoutError()