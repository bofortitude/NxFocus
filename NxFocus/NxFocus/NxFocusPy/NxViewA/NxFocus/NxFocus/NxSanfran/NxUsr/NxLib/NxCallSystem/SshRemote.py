#!/usr/bin/python

import paramiko
import logging


class SshAgent():
    def __init__(self, remoteIp, username, passwd, remotePort=22, retry=5, logger=None):
        self.remoteIp = str(remoteIp)
        self.username = str(username)
        self.passwd = str(passwd)
        self.remotePort = int(remotePort)
        self.retry = int(retry)
        if logger is None:
            self.logger = logging.getLogger()
        else:
            self.logger = logger

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connectRemote(self):
        for i in xrange(self.retry):
            try:
                self.logger.info('Connecting remote server "'+self.remoteIp+':'+str(self.remotePort)+'" ...')
                self.ssh.connect(self.remoteIp, self.remotePort, self.username, self.passwd)
                self.logger.info('Connecting remote server "'+self.remoteIp+':'+str(self.remotePort)+' succeeds.')
                return True
            except Exception as err:
                self.logger.warning('Connecting remote server meets exception!')
                self.logger.debug(str(err))
        return False

    def execCommand(self, command):
        self.logger.info('Executing command "'+str(command)+'" on server "'+self.remoteIp+':'+str(self.remotePort)+'" ...')
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
        except Exception as err:
            self.logger.warning('Executing command meets exception!')
            self.logger.debug(str(err))
            return False
        stdoutList = stdout.readlines()
        stderrList = stderr.readlines()
        #print 'The result from remote server "'+self.remoteIp+':'+str(self.remotePort)+'" is:'
        if stdoutList != []:
            self.logger.info('\n---------------- Result ----------------')
            self.logger.info(self.username+'@'+self.remoteIp+':~# '+str(command))
            for i in stdoutList:
                self.logger.info(str(i))
            self.logger.info(self.username + '@' + self.remoteIp + ':~# ')
            self.logger.info('----------------------------------------\n')
        if stderrList != []:
            #print 'The error from remote server "'+self.remoteIp+':'+str(self.remotePort)+'" is:\n'
            self.logger.warning('\n!!!!!!!!!!!!!! Error !!!!!!!!!!!!!!')
            for j in stderrList:
                self.logger.warning(str(j))
            self.logger.warning('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
        return stdoutList, stderrList


    def closeSsh(self):
        self.logger.info('Closing the connection to server "'+self.remoteIp+':'+str(self.remotePort)+'" ...')
        self.ssh.close()
        self.logger.info('Connection to server "'+self.remoteIp+':'+str(self.remotePort)+'" has been closed.')





