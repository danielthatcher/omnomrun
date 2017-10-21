#! /usr/bin/env python3

import os
import time
import sys
import subprocess
import csv
import argparse


def parseArgs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--input-file", help="The CSV input file to use", default="omnomrun.csv")
    parser.add_argument("-t", "--time", help="The time between checking for updates to the input file", type=int, default=5)
    parser.add_argument("-v", "--verbose", help="Print the output of the running commands", action="store_true", default=False)
    parser.add_argument("-d", "--delimiter", help="The delimiter of the CSV file", default=",")
    parser.add_argument("-q", "--quotechar", help="The quote char for the CSV file", default="\"")
    parser.add_argument("-c", "--clean", help="Clean up old .omnomrun hidden file", action="store_true", default=False)
    parser.add_argument("command",
                        help="A python format string that will be formatted with each line of the input file to give the command to run")
    return parser.parse_args(argv)

def runCommand(comm, opts):
    """Run the command given the line of the input file as opts"""
    comm = comm.format(*opts)
    print("Running '{}'...".format(comm))
    process = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
    for line in iter(process.stdout.readline, ""):
        yield line

    print("Completed")
    print("")
    process.stdout.close()

def newlines(filename, delimiter=",", quotechar="\""):
    """Check for updated contents of a file and yield any new lines"""
    outname = ".{}.omnomrun".format(filename)
    with open(filename, "r") as infile, open(outname, "r+") as outfile:
        # Compare the in and out CSV files for differences
        inreader = csv.reader(infile, delimiter=delimiter, quotechar=quotechar)
        outreader = csv.reader(outfile, delimiter=delimiter, quotechar=quotechar)
        outwriter = csv.writer(outfile, delimiter=delimiter, quotechar=quotechar)

        inlines = list(inreader)
        outlines = list(outreader)

        difflines = [x for x in inlines if x not in outlines]
        for line in difflines:
            yield line
            outwriter.writerow(line)

if __name__ == "__main__":
    args = parseArgs(sys.argv[1:])

    metafile = ".{}.omnomrun".format(args.input_file)
    if args.clean and os.path.exists(metafile):
        os.remove(metafile)

    # Check the input file exists
    if not os.path.exists(args.input_file):
        open(args.input_file, "a").close()

    if not os.path.exists(metafile):
        open(metafile, "a").close()

    while True:
        for line in newlines(args.input_file, args.delimiter, args.quotechar):
            for output in runCommand(args.command, line):
                if args.verbose and output is not b'':
                    print(output, end="")

        time.sleep(args.time)
