#!/usr/bin/python


import time
import subprocess
import logging



from NxSanfran.NxUsr.NxLib.NxLogging import setSimpleLogging
from NxSanfran.NxUsr.NxLib.NxWechat2.WechatActiveAgent import WechatActive
from NxSanfran.NxEtc.NxPublic.NxPredefault import PreWechat as PredefinedWechat

def checkSubnet(dstIp):
    setSimpleLogging()
    subnetOk = True
    subnetOkCount = 0
    subnetFailCount = 0
    command = 'ping '+str(dstIp)+' -c 1'
    while True:
        logging.info('Starting to ping destination ...')
        shell_run = subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        if shell_run == 0:
            logging.info('Destination is reachable.')
            subnetOkCount += 1
            subnetFailCount = 0
        else:
            logging.info('Destination is unreachable.')
            subnetOkCount = 0
            subnetFailCount += 1

        if subnetFailCount >= 20:
            subnetFailCount = 0
            if subnetOk == True:
                unreachableMessage = '[Connectivity Fails!] IP address '+str(dstIp)+' for Sunnyvale is unreachable!'
                myAgent = WechatActive(PredefinedWechat.corpId, PredefinedWechat.secret)
                myAgent.sendText(PredefinedWechat.agentIdDict['QAinfo'], unreachableMessage, toUserList=['bofei', 'youjunsong'])
                subnetOk = False
        if subnetOkCount >= 20:
            subnetOkCount = 0
            if subnetOk == False:
                reachableMessage = '[Connectivity OK!] IP address '+str(dstIp)+' for Sunnyvale is reachable now.'
                myAgent = WechatActive(PredefinedWechat.corpId, PredefinedWechat.secret)
                myAgent.sendText(PredefinedWechat.agentIdDict['QAinfo'], reachableMessage, toUserList=['bofei', 'youjunsong'])
                subnetOk = True

        print 'Sleep 1 second ...'
        time.sleep(1)

def mainEn(dstIp = '172.22.15.1'):
    checkSubnet(dstIp)





