
import argparse
from argparse import RawTextHelpFormatter


class arguments():
    """docstring for ClassName"""

    def __init__(self, sysArgsList):
        # super(ClassName, self).__init__()
        self.sysArgsList = list(sysArgsList)
        programName = self.sysArgsList[0]
        del self.sysArgsList[0]
        argUsage = str(programName) + ''' <dns-server> [options]

Version 1.00

Notes:


'''

        self.parser = argparse.ArgumentParser(
            usage=argUsage, formatter_class=RawTextHelpFormatter)
        self.parser.add_argument('-c', '--concurrent', dest='concurrent',
                                 default=1,
                                 type=int,
                                 help="Specify the concurrent threads number.")
        self.parser.add_argument('-r', '--requests',
                                 dest='requests',
                                 default=1,
                                 type=int,
                                 help="Specify the requests number per thread.")
        self.parser.add_argument('-i', '--interval',
                                 dest='interval',
                                 default=0.0,
                                 type=float,
                                 help='Interval between requests, default is 1.')
        self.parser.add_argument('-d', '--dns-port',
                                 dest='dstPort',
                                 default=53, type=int,
                                 help='Specify the destination DNS port.')
        self.parser.add_argument('-t', '--tcp', dest='isTcp',
                                 action='store_true',
                                 help='Use TCP as transport protocol once it is taken.')
        self.parser.add_argument('-l', '--length',
                                 dest='loadLength', default=None,
                                 type=int,
                                 help='Specify the payload length of DNS query.')
        self.parser.add_argument('-n', '--timeout',
                                 dest='timeout',
                                 default=2.0,
                                 type=float,
                                 help='Specify the socket timeout.')
        self.parser.add_argument('-b', '--buffer-size',
                                 dest='bufferSize',
                                 default=1024,
                                 type=int,
                                 help='Specify the buffer size for socket.')
        self.parser.add_argument('--debug',
                                 dest='debug',
                                 action='store_true',
                                 help='Enable debug mode.')

        self.args, self.remaining = self.parser.parse_known_args(
            self.sysArgsList)

        if len(self.remaining) < 1:
            self.parser.print_help()
            exit()

        self.concurrent = self.args.concurrent
        self.requests = self.args.requests
        self.interval = self.args.interval
        self.dstPort = self.args.dstPort
        self.isTcp = self.args.isTcp
        self.loadLength = self.args.loadLength
        self.timeout = self.args.timeout
        self.bufferSize = self.args.bufferSize
        self.debug = self.args.debug

        self.dnsServer = self.remaining[0]

    def printHelp(self):
        self.parser.print_help()
        exit()
