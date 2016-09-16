#!/usr/bin/python


import subprocess
import logging

def runShellCmd(command, logger=None):
    '''Return the status code'''
    if logger is None:
        logger = logging.getLogger()
    logger.debug('Run: '+str(command)+' ...')

    shell_run = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    return_string = ''
    status_code = shell_run.wait()
    for line in shell_run.stdout.readlines():
        logger.debug(str(line))
        return_string = return_string + line
    if status_code == 0:
        logger.debug('Running command '+str(command)+' OK.')

    else:
        logger.debug('Running command '+str(command)+' failed!')
    return return_string


class RunShellCommands():
    def __init__(self, logger=None):
        self.cmdSubprocessDict = {}
        self.incompleteCommandsList = []

        if logger is None:
            self.logger = logging.getLogger()
        else:
            self.logger = logger

    def addRunningCommand(self, command):
        self.logger.info('Run command: '+str(command)+' ...')
        shellRun = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.cmdSubprocessDict[str(command)] = shellRun
        self.logger.info('Command '+str(command)+' has been started.')

    def wait4Subprocess(self):
        self.logger.info('Waiting for all the shell commands over...')
        for (i, j) in self.cmdSubprocessDict.items():

            statusCode = j.wait()
            self.logger.info('The command "'+i+'" status cde is:')
            self.logger.info(str(statusCode))

            returnString = ''
            for line in j.stdout.readlines():
                self.logger.info(str(line))
            if statusCode != 0:
                self.incompleteCommandsList.append(i)

    def getIncompleteCommands(self):
        return self.incompleteCommandsList








