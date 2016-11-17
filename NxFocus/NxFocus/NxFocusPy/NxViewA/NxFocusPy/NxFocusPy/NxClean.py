#!/usr/bin/python


from NxSanfran.NxEtc.NxPublic.NxPredefault.Default import *
from NxSanfran.NxTools import RemovePyc
from NxSanfran.NxUsr.NxLib import NxFiles
from NxSanfran.NxUsr.NxLib.NxLogging import setSimpleLogging
import logging


exceptList = [
    'README.rst',
    '__init__.py',
    'NxPrjcts'

]


setSimpleLogging()


def clearFiles(path, additionalExceptList=[]):
    logging.info('Clearing the files in '+str(path)+' ...')
    filesInPath = NxFiles.listDir(path)
    for i in filesInPath:
        if i not in exceptList and i not in additionalExceptList:
            NxFiles.removeForce(path+'/'+str(i))
            logging.warning(path+'/'+str(i)+' has been removed!')





logging.info('Clean up the ".pyc" file ...')
RemovePyc.delPycFile()

clearFiles(NxSanfranRunPath)
clearFiles(NxLogPrjctsPath)
clearFiles(NxVarLogPath)
clearFiles(NxSanfranTmpPath)
clearFiles(NxTmpPrjctsPath)

logging.info('Clean up the geo_ip_sub folder ...')
geoIpSubParentFolder = NxUsrLibPath+'/NxCallSystem/ADC/IpLibrary'
if NxFiles.isDir(geoIpSubParentFolder):
    if NxFiles.isDir(geoIpSubParentFolder+'/geo_ip_sub'):
        NxFiles.removeForce(geoIpSubParentFolder+'/geo_ip_sub')
        logging.warning(geoIpSubParentFolder+'/geo_ip_sub'+' has been removed.')








