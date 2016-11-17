

import logging

from NxSanfran.NxUsr.NxLib.NxLogging import setSimpleLogging
from . import ArgsDefine
from NxSanfran.NxUsr.NxLib import NxArguments


def argLimit(sysArgsList):
    parser, args, remaining = NxArguments.parseArgs(
        sysArgsList, ArgsDefine.argUsage, ArgsDefine.argsList)

    if len(remaining) < 2:
        parser.print_help()
        exit()
    return (args, remaining)


def enMain(sysArgsList):
    args, remaining = argLimit(sysArgsList)
    if args.debug:
        setSimpleLogging(debug=True)
    else:
        setSimpleLogging(debug=False)

    logger = logging.getLogger()
