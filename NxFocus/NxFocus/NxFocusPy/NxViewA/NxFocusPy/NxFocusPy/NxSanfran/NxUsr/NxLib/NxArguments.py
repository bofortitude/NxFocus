#!/usr/bin/python


import argparse
from argparse import RawTextHelpFormatter


def parseArgs(sysArgsList, argUsage, definedArgsList):
    mySysArgsList = list(sysArgsList)
    programName = mySysArgsList[0]
    del mySysArgsList[0]
    myArgUsage = '\n' + str(programName) + str(argUsage)
    parser = argparse.ArgumentParser(
        usage=myArgUsage, formatter_class=RawTextHelpFormatter)
    for i in definedArgsList:
        parser.add_argument(*i[0], **i[1])
    args, remainingArgs = parser.parse_known_args(mySysArgsList)
    return (parser, args, remainingArgs)
