#!/usr/bin/python


import logging
import time

from NxSanfran.NxUsr.NxLib.NxRequests import NxRequests
from NxSanfran.NxUsr.NxLib import NxFiles
from NxSanfran.NxUsr.NxLib.NxCallSystem.ADC.AdcCommandLine.TelnetCommandLine import TelCmdLine
from .PushInfo import wechat2Me





'''
login:

General:
Request URL:http://10.160.41.195/api/user/login
Request Method:POST


request headers:

Accept:application/json, text/javascript, */*; q=0.01
Accept-Encoding:gzip, deflate
Accept-Language:en-US,en;q=0.8
Connection:keep-alive
Content-Length:34
Content-Type:application/json; charset=UTF-8
Cookie:adc_session=%7B%22slim.flash%22%3A%5B%5D%7D
Host:10.160.41.195
Origin:http://10.160.41.195
Referer:http://10.160.41.195/ui/
User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36
X-Requested-With:XMLHttpRequest


request payload:
{username: "admin", password: ""}


====================================================================================
backup config:

General:
Request URL:http://10.160.41.195/api/downloader/config?entire=enable
Request Method:GET

requests headers:
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding:gzip, deflate, sdch
Accept-Language:en-US,en;q=0.8
Connection:keep-alive
Cookie:adc_session=%7B%22slim.flash%22%3A%5B%5D%2C%22user%22%3A%7B%22sid%22%3A777311349%2C%22username%22%3A%22admin%22%7D%2C%22last_access_time%22%3A1474607368%7D
Host:10.160.41.195
Referer:http://10.160.41.195/ui/
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36

'''



invalidLicenseString = '{"payload":"Invalid VM License"}'



def httpDownload(url, cookieString, location, isEntireConfig=True,  fileName=None, timeout=60, logger=None):
    if logger is None:
        logger = logging.getLogger()
    if fileName is None:
        if isEntireConfig:
            fileName = 'AdcConfig'+time.strftime('%Y%m%d%H%M%S', time.localtime())+'.tar'
        else:
            fileName = 'AdcConfig'+time.strftime('%Y%m%d%H%M%S', time.localtime())

    logger.debug('Checking the location '+str(location))
    if not NxFiles.isDir(location):
        logger.debug('The location '+str(location)+' is not a directory, attempting to make it.')
        NxFiles.makeDirs(location)
        logger.debug('The location '+str(location)+' has been made.')
    else:
        logger.debug('The location '+str(location)+' is a valid directory.')

    if NxFiles.isFile(location+'/'+fileName):
        logger.warning('The file '+location+'/'+fileName+' exists, delete it now!')
        NxFiles.removeForce(location+'/'+fileName)

    try:
        r = NxRequests()
        r.addCookie('adc_session', cookieString)
        r.setTimeout(timeout)
        r.addHeader('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        r.addHeader('Accept-Encoding', 'gzip, deflate, sdch')
        r.addHeader('Accept-Language', 'en-US,en;q=0.8')
        r.addHeader('Connection', 'keep-alive')
        r.addHeader('Upgrade-Insecure-Requests', '1')
        r.addHeader('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')
        #r.addHeader('referer', refererString)

        logger.info('Starting to download...')
        response = r.get(url, stream=True)
        if response.status_code != 200:
            logger.warning('The status code from ADC is not 200, return False!')
            #wechat2Me('[AdcPatroller] The status code from ADC is not 200! URL is '+str(url)+' .')
            return False
        if not response.content:
            logger.warning('The response from ADC has no content, return False!')
            #wechat2Me('[AdcPatroller] The response from ADC has no content! The URL is '+str(url)+' .')
            return False
        else:
            if str(response.content).find(invalidLicenseString) != -1:
                logger.warning('The response content contains '+invalidLicenseString+' , return False!')
                return False

        with open(location+'/'+fileName, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        logger.info('The config file has been downloaded to '+location+'/'+fileName+' .')

    except Exception as err:
        logger.debug('Downloading meete exception:')
        logger.debug(str(err))
        return False




def backupConfig(mgmtIp, location, isEntireConfig=True, username='admin', password='', mgmtPort=None, isHttps=False, logger=None):
    if logger is None:
        logger = logging.getLogger()
    if isHttps:
        urlPrefix = 'https://'
        if mgmtPort is None:
            mgmtPort = 443
    else:
        urlPrefix = 'http://'
        if mgmtPort is None:
            mgmtPort = 80

    if isEntireConfig:
        entireOption = 'entire=enable'
    else:
        entireOption = 'entire=disable'


    logger.info('Start to backup the full config from '+str(mgmtIp)+' ...')
    loginUrl = urlPrefix+str(mgmtIp)+':'+str(mgmtPort)+'/api/user/login'
    backupConfigUrl = urlPrefix+str(mgmtIp)+':'+str(mgmtPort)+'/api/downloader/config?'+entireOption

    logger.debug('The login url is: '+str(loginUrl))
    logger.debug('The backup config url is: '+str(backupConfigUrl))

    logger.debug('Building the login request sender ...')
    loginSender = NxRequests()
    loginSender.addHeader('Accept', 'application/json, text/javascript, */*; q=0.01')
    loginSender.addHeader('Accept-Encoding', 'gzip, deflate')
    loginSender.addHeader('Accept-Language', 'en-US,en;q=0.8')
    loginSender.addHeader('Connection', 'keep-alive')
    loginSender.addHeader('Content-Type', 'application/json; charset=UTF-8')
    #loginSender.addHeader('Referer', 'http://'+str(mgmtIp)+'/ui/')
    loginSender.addHeader('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36')
    loginSender.addHeader('X-Requested-With', 'XMLHttpRequest')
    loginSender.addData('username', username)
    loginSender.addData('password', password)

    logger.info('Sending the login request ...')
    try:
        loginResponse = loginSender.post(loginUrl)
    except Exception as err:
        logger.warning('Login meets exception:')
        logger.warning(str(err))
        return False
    logger.debug('The login response is:')
    logger.debug(str(loginResponse))
    logger.debug('The login cookie is:')
    logger.debug(str(loginResponse.cookies))
    loginCookie = loginResponse.cookies['adc_session']

    httpDownload(backupConfigUrl, loginCookie, location,  isEntireConfig=isEntireConfig)



def checkDirectorySize(path, directorySize):
    directorySize = long(directorySize)
    logger = logging.getLogger()
    if not NxFiles.isDir(path):
        return
    logger.debug('The size of directory '+str(path)+' is '+str(NxFiles.dirSize(path)))
    if NxFiles.dirSize(path) > directorySize:
        logger.info('The size of ' + str(path) + ' is greater than ' + str(
            directorySize) + ', apttempting to remove files from early to late.')
        filesList = NxFiles.sortDir(path)
        count = 0
        for i in filesList:
            NxFiles.removeForce(path + '/' + i)
            logger.warning('The file ' + str(path + '/' + i) + ' has been removed!')
            if NxFiles.dirSize(path) <= directorySize:
                break
            if count >= 100:
                break
            count += 1
    else:
        logger.debug('The size of ' + str(path) + ' is lower than ' + str(
            directorySize))

def forceMakeDirectory(path, logger=None):
    if logger is None:
        logger = logging.getLogger()
    if not NxFiles.isDir(path):
        logger.info(str(path) + ' does not exist, attempting to make it.')
        NxFiles.makeDirs(path)


def getAdcSystemStatus(mgmtIp, telnetPort=23, username='admin', password='', logger=None):
    '''Return a dict'''
    statusDict = {}
    if logger is None:
        logger = logging.getLogger()
    logger.debug('Starting to get the ADC system status')
    adcCli = TelCmdLine(mgmtIp, adc_port=telnetPort, username=username, passwd=password)
    try:
        logger.debug('Try to login ADC ...')
        adcCli.login()
        logger.debug('Sending command get sys status ...')
        responseMsg = adcCli.run_cmd('get system status')
        logger.debug('The response message from ADC is :')
        logger.debug(str(responseMsg))
        statusLineList = str(responseMsg).split('\r\n')
        del statusLineList[0]
        del statusLineList[-1]
        del statusLineList[-1]
        for i in statusLineList:
            itemList = i.split(':')
            if len(itemList) >= 2:
                statusDict[itemList[0].strip()] = itemList[1].strip()
        logger.debug('The ADC system status dict is: '+str(statusDict)+' .')
        return statusDict
    except Exception as err:
        logger.warning('Getting ADC system status meets exception:')
        logger.warning(str(err))
        return False


def backupAdcConfig(mgmtIp, location, interval=7200, directorySize=100000000,
                    username='admin', password='', mgmtPort=None, telnetPort=23, isHttps=False):
    interval = float(interval)
    directorySize = long(directorySize)
    logger = logging.getLogger()
    logger.info('Starting the process to backup the ADC configs...')
    subRootPath = location+'/'+str(mgmtIp)


    while True:
        logger.info('Starting new round backup ...')

        finalRootPath = subRootPath
        adcSystemStatusDict = getAdcSystemStatus(mgmtIp, telnetPort=telnetPort, username=username, password=password)
        if not adcSystemStatusDict:
            logger.warning('Getting system status meets error, skip making sub directories.')
        else:
            if 'Version' in adcSystemStatusDict:
                platformMark = str(adcSystemStatusDict['Version']).split()[0]
                versionMark = str(adcSystemStatusDict['Version']).split()[1].replace(',','_')
                finalRootPath += '/'+platformMark+'/'+versionMark
            else:
                logger.warning('"Version" is not in ADC system status dict, skip making sub directories.')

        fullConfigRootPath = finalRootPath + '/' + 'fullConfigBackup'
        plainConfigRootPath = finalRootPath+ '/' + 'plainConfigBackup'
        forceMakeDirectory(fullConfigRootPath)
        forceMakeDirectory(plainConfigRootPath)
        checkDirectorySize(fullConfigRootPath, directorySize)
        checkDirectorySize(plainConfigRootPath, directorySize)

        try:
            logger.info('Backup the full config from '+str(mgmtIp)+' ...')
            backupConfig(mgmtIp, fullConfigRootPath, isEntireConfig=True,
                                      username=username, password=password, mgmtPort=mgmtPort, isHttps=isHttps)
            logger.info('Backup the plain config from '+str(mgmtIp)+' ...')
            backupConfig(mgmtIp, plainConfigRootPath, isEntireConfig=False,
                                      username=username, password=password, mgmtPort=mgmtPort, isHttps=isHttps)

        except Exception as err:
            logger.warning('This rounc backup meets exception:')
            logger.warning(err)
        logger.info('Sleep ' + str(interval) + 's for next round backup ...')
        time.sleep(float(interval))


















