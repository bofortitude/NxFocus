#!/usr/bin/python

import sys
import ConfigParser
import re
import logging
import ClearServerNetConfig
from ....NxUsr.NxLib.NxCallSystem import SshRemote



def setupEnv(topologyFile, logger=None):
    conf = ConfigParser.ConfigParser()
    conf.read(topologyFile)
    if logger is None:
        logger = logging.getLogger()

    sectionList = conf.sections()
    for i in sectionList:
        if not conf.has_option(i, 'ip'):
            logger.info('Node '+str(i)+' has no "ip" option, skip the operation of this node!')
            continue
        serverIp = conf.get(i, 'ip')
        if not conf.has_option(i, 'port'):
            serverPort = 22
        else:
            serverPort = int(conf.get(i, 'port'))
        if not conf.has_option(i, 'username'):
            username = 'root'
        else:
            username = conf.get(i, 'username')
        if not conf.has_option(i, 'password'):
            password = 'fortinet'
        else:
            password = conf.get(i, 'password')

        cmdSequenceListRaw = []
        optionList = conf.options(i)
        cmdPattern = re.compile(r'^cmd[0-9]+$')
        for j in optionList:
            if cmdPattern.match(j):
                cmdSequenceListRaw.append(int(j.replace('cmd', '')))

        cmdSequenceList = sorted(cmdSequenceListRaw)

        logger.info('Starting to configure the server "'+serverIp+'" ...')
        ClearServerNetConfig.clearNetworkConfig(serverIp, username=username, passwd=password, serverPort=serverPort)
        ClearServerNetConfig.initNetworkConfig(serverIp, username=username, passwd=password, serverPort=serverPort)
        mySshAgent = SshRemote.SshAgent(serverIp, username, password, remotePort=serverPort)
        mySshAgent.connectRemote()
        for j in cmdSequenceList:
            mySshAgent.execCommand(conf.get(i, 'cmd'+str(j)))
        mySshAgent.closeSsh()
        logger.info('Configuring server "'+serverIp+'" over.')



