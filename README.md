# omnomrun.py
Use new entries in a CSV file to run shell command through python format strings.

This is a simple (and very quickly hacked together) script that continuously checks for new lines in a CSV file, and then uses those new lines as arguments to a python format string which gets executed as a shell command. For instance, as a demo with no practical use, to move files you can use:

```
$ ./omnomrun.py -v -f in.csv 'mv {0} {1}'
```

Then, and entry in in.csv which looks like the following will cause a.txt to be moved to b.txt.
```
a.txt,b.txt
```

The full help text for this program is shown below.
```
$ ./omnomrun.py -h
usage: omnomrun.py [-h] [-f INPUT_FILE] [-t TIME] [-v] [-d DELIMITER]
                   [-q QUOTECHAR] [-c]
                   command

positional arguments:
  command               A python format string that will be formatted with
                        each line of the input file to give the command to run

optional arguments:
  -h, --help            show this help message and exit
  -f INPUT_FILE, --input-file INPUT_FILE
                        The CSV input file to use
  -t TIME, --time TIME  The time between checking for updates to the input
                        file
  -v, --verbose         Print the output of the running commands
  -d DELIMITER, --delimiter DELIMITER
                        The delimiter of the CSV file
  -q QUOTECHAR, --quotechar QUOTECHAR
                        The quote char for the CSV file
  -c, --clean           Clean up old .omnomrun hidden file
```

## Current issues
* Only lines not previously seen in the input file will be run, even if the line is new
