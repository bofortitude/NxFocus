#!/usr/bin/python



from NxSanfran.NxLib import argparse
from NxSanfran.NxLib.argparse import RawTextHelpFormatter



class argument():
    '''Handle arguments'''

    def __init__(self, sysArgsList):
        self.sysArgsList = list(sysArgsList)

    def parseArgs(self):
        programName = self.sysArgsList[0]
        del self.sysArgsList[0]
        arg_usage = str(programName) + ''' <adc-ip> <location> [options]

Notes:
        '''

        self.parser = argparse.ArgumentParser(usage=arg_usage, formatter_class=RawTextHelpFormatter)
        self.parser.add_argument('-u', '--username', dest='username', default='admin',
                            help="Specify the username, default is 'admin'.")
        self.parser.add_argument('-p', '--password', dest='password', default='',
                                 help="Specify the password, default is ''.")
        self.parser.add_argument('-s', '--https', dest='isHttps', action='store_true',
                                 help='Use HTTPS session to ADC once it is specified.')
        self.parser.add_argument('-l', '--log', dest='logFile', help='Specify the AdcPatroller log file.')

        self.parser.add_argument('--directory-size', dest='directorySize', default=100000000,
                                 help='Specify the max directory size, default is 100000000.')
        self.parser.add_argument('--backup-interval', dest='backupInterval', default=7200,
                                 help='Specify the backup config interval, default is 7200.')
        self.parser.add_argument('--mgmt-port', dest='mgmtPort',
                                 help="Specify the admin mgmt port.")
        self.parser.add_argument('--telnet-port', dest='telnetPort', default=23, help='Specify the telnet dst port, default is 23.')



        self.args, self.remaining = self.parser.parse_known_args(self.sysArgsList)

        if len(self.remaining) < 2:
            self.print_help()

        self.username = self.args.username
        self.password = self.args.password
        self.isHttps = self.args.isHttps
        self.logFile = self.args.logFile
        self.mgmtPort = self.args.mgmtPort
        self.telnetPort = self.args.telnetPort
        self.backupInterval = self.args.backupInterval
        self.directorySize = self.args.directorySize

        self.adcIp = self.remaining[0]
        self.location = self.remaining[1]

    def print_help(self):
        self.parser.print_help()
        exit()









