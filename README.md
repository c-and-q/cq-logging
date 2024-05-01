# cq_logging: micropython-**logging**

Part of [micropython-phew](https://github.com/pimoroni/phew) module by Pimoroni.

Extracted to follow single responsibility principle.

- [logging module](#logging-module)
    - [log(level, text)](#loglevel-text)
    - [debug(\*items)](#debugitems)
    - [info(\*items)](#infoitems)
    - [warn(\*items)](#warnitems)
    - [error(\*items)](#erroritems)
    - [set\_truncate\_thresholds(truncate\_at, truncate\_to)](#set_truncate_thresholdstruncate_at-truncate_to)

## Details

* name: cq_logging
* version: 0.1.0
* description:  Micropython logging, part of Pimoroni logging
* project_url: https://github.com/c-and-q/cq-logging
* license="MIT",

---

## Function reference

### logging module

#### log(level, text)

Add a new entry into the log file.

```python
log("info", "> i'd like to take a minute, just sit right there")
log("error", "> the license plate said 'Fresh' and it had dice in the mirror")
```

The entry will automatically have the current date and time, the `level` value, and the amount of free memory in kB
prepended:

```
2022-09-04 15:29:20 [debug    / 110kB] > performing startup
2022-09-04 15:30:42 [info     / 113kB]   - wake reason: rtc_alarm
2022-09-04 15:30:42 [debug    / 112kB]   - turn on activity led
2022-09-04 15:30:43 [info     / 102kB] > running pump 1 for 0.4 second
2022-09-04 15:30:46 [info     / 110kB] > 5 cache files need uploading
2022-09-04 15:30:46 [info     / 107kB] > connecting to wifi network 'yourssid'
2022-09-04 15:30:48 [debug    / 100kB]   - connecting
2022-09-04 15:30:51 [info     /  87kB]   - ip address:  192.168.x.x
2022-09-04 15:30:57 [info     /  79kB]   - uploaded 2022-09-04T15:19:03Z.json 2022-09-04 15:31:01 [info     /  82kB]   - uploaded 2022-09-04T15:28:17Z.json 2022-09-04 15:31:06 [info     /  88kB]   - uploaded 2022-09-04T15:30:43Z.json 2022-09-04 15:31:11 [info     /  95kB]   - uploaded 2022-09-04T15:29:00Z.json 2022-09-04 15:31:16 [info     / 100kB]   - uploaded 2022-09-04T15:29:21Z.json 2022-09-04 15:31:16 [info     /  98kB] > going to sleep
```

#### debug(*items)

Shorthand method for writing debug messages to the log.

```python
warn("> this is a story")
```

#### info(*items)

Shorthand method for writing information to the log.

```python
num = 123
info("> all about how", num, time.time())
```

#### warn(*items)

Shorthand method for writing warnings to the log.

```python
warn("> my life got flipped")
```

#### error(*items)

Shorthand method for writing errors to the log.

```python
warn("> turned upside down")
```

#### set_truncate_thresholds(truncate_at, truncate_to)

Will automatically truncate the log file to `truncate_to` bytes long when it reaches `truncate_at` bytes in length.

```python
# automatically truncate when we're closed to the 
# filesystem block size to keep to a single block
set_truncate_thresholds(3.5 * 1024, 2 * 1.024)
```

Truncation always happens on the nearest line ending boundary so the truncated file may not exactly match the size
specified.
