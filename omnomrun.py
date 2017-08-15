#! /usr/bin/env python3

import os
import time
import sys
import subprocess
import shlex
import csv
import argparse


def parseArgs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--input-file", help="The CSV input file to use", default="omnomrun.csv")
    parser.add_argument("-t", "--time", help="The time between checking for updates to the input file", type=int, default=5)
    parser.add_argument("-v", "--verbose", help="Print the output of the running commands", action="store_true", default=False)
    parser.add_argument("-d", "--delimiter", help="The delimiter of the CSV file", default=",")
    parser.add_argument("-q", "--quotechar", help="The quote char for the CSV file", default="\"")
    parser.add_argument("command",
                        help="A python format string that will be formatted with each line of the input file to give the command to run")
    return parser.parse_args(argv)

def runCommand(comm, opts, verbose=False):
    """Run the command given the line of the input file as opts"""
    comm = comm.format(*opts)
    if verbose:
        out = subprocess.PIPE
    else:
        out = None

    process = subprocess.Popen(shlex.split(comm), stdout=out, stderr=out)
    return process.communicate()

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

    # Check the input file exists
    if not os.path.exists(args.input_file):
        open(args.input_file, "a").close()

    outfilename = ".{}.omnomrun".format(args.input_file)
    if not os.path.exists(outfilename):
        open(outfilename, "a").close()

    while True:
        for line in newlines(args.input_file, args.delimiter, args.quotechar):
            runCommand(args.command, line, args.verbose)

        time.sleep(args.time)
