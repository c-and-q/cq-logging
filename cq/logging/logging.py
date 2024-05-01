import os
import machine
import gc

# FIXME: change API:
#  some python.logging ideas
#  logging class
#    named logging
#    set_log_level
#    disable file logging
#   review truncate()
#   maintain in-memory log file size
#   multitasking ?
#   CPython compatibility?
#     test it
#   review forks of pimoroni/phew

log_file = "log.txt"

LOG_DEBUG = 1
LOG_INFO = LOG_DEBUG << 1
LOG_WARNING = LOG_INFO << 1
LOG_ERROR = LOG_WARNING << 1
LOG_EXCEPTION = LOG_ERROR << 1
LOG_CRITICAL = LOG_EXCEPTION << 1
LOG_ALL = LOG_DEBUG | LOG_INFO | LOG_WARNING | LOG_ERROR | LOG_EXCEPTION | LOG_CRITICAL

_logging_types = LOG_ALL

# the log file will be truncated if it exceeds _log_truncate_at bytes in
# size. the defaults values are designed to limit the log to at most
# three blocks on the Pico
_log_truncate_at = 11 * 1024
_log_truncate_to = 8 * 1024


def datetime_string():
    dt = machine.RTC().datetime()
    return "{0:04d}-{1:02d}-{2:02d} {4:02d}:{5:02d}:{6:02d}".format(*dt)


def file_size(file):
    try:
        return os.stat(file)[6]
    except OSError:
        return None


def set_truncate_thresholds(truncate_at, truncate_to):
    global _log_truncate_at
    global _log_truncate_to
    _log_truncate_at = truncate_at
    _log_truncate_to = truncate_to


def enable_logging_types(types):  # FIXME change logic to minimal debug level
    global _logging_types
    _logging_types = _logging_types | types


def disable_logging_types(types):  # FIXME change logic to minimal debug level
    global _logging_types
    _logging_types = _logging_types & ~types


# truncates the log file down to a target size while maintaining
# clean line breaks
def truncate(file, target_size):  # FIXME: efficiency?
    size = file_size(file)

    # calculate how many bytes we're aiming to discard
    discard = size - target_size
    if discard <= 0:
        return

    with open(file, "rb") as infile:
        with open(file + ".tmp", "wb") as outfile:
            # skip a bunch of the input file until we've discarded
            # at least enough
            while discard > 0:
                chunk = infile.read(1024)
                discard -= len(chunk)

            # try to find a line break nearby to split first chunk on
            break_position = max(
                chunk.find(b"\n", -discard),  # search forward
                chunk.rfind(b"\n", -discard)  # search backwards
            )
            if break_position != -1:  # if we found a line break..
                outfile.write(chunk[break_position + 1:])

            # now copy the rest of the file
            while True:
                chunk = infile.read(1024)
                if not chunk:
                    break
                outfile.write(chunk)

    # delete the old file and replace with the new
    os.remove(file)
    os.rename(file + ".tmp", file)


def log(level, text):
    datetime = datetime_string()
    log_entry = "{0} [{1:8} /{2:>4}kB] {3}".format(datetime, level, round(gc.mem_free() / 1024), text)
    print(log_entry)
    with open(log_file, "a") as logfile:  # FIXME avoid closing log file
        logfile.write(log_entry + '\n')

    if _log_truncate_at and file_size(
            log_file) > _log_truncate_at:  # FIXME size of log file can be maintained in memory
        truncate(log_file, _log_truncate_to)


def info(*items):
    if _logging_types & LOG_INFO:
        log("info", " ".join(map(str, items)))


def warn(*items):
    if _logging_types & LOG_WARNING:
        log("warning", " ".join(map(str, items)))


def error(*items):
    if _logging_types & LOG_ERROR:
        log("error", " ".join(map(str, items)))


def debug(*items):
    if _logging_types & LOG_DEBUG:
        log("debug", " ".join(map(str, items)))


def exception(*items):
    if _logging_types & LOG_EXCEPTION:
        log("exception", " ".join(map(str, items)))


def critical(*items):
    if _logging_types & LOG_CRITICAL:
        log("critical", " ".join(map(str, items)))
