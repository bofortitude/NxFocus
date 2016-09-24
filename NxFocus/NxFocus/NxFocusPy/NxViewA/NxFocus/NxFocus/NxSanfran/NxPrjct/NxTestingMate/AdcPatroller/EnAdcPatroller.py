#!/usr/bin/python

import logging
import multiprocessing

from ....NxUsr.NxLib.NxLogging import setSimpleLogging
import Arguments
from ....NxUsr.NxLib import NxFiles
from BackupConfig import backupAdcConfig






def enMain(sysArgsList):
    setSimpleLogging()
    logger = logging.getLogger()
    args = Arguments.argument(sysArgsList)
    args.parseArgs()


    logger.info('Starting the AdcPatroller...')
    processList = []

    backupProcess = multiprocessing.Process(target=backupAdcConfig, args=(args.adcIp, args.location),
        kwargs={'directorySize':args.directorySize, 'interval':args.backupInterval, 'username':args.username,
                'password':args.password, 'mgmtPort':args.mgmtPort, 'isHttps':args.isHttps})
    logger.info('"backupAdcConfig" process has been created.')
    processList.append(backupProcess)


    logger.info('Starting all processes ...')
    for i in processList:
        i.start()

    for j in processList:
        j.join()














