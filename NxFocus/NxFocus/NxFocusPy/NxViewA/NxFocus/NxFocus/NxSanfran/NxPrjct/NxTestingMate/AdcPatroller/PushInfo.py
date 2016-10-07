#!/usr/bin/python



from NxSanfran.NxUsr.NxLib.NxWechat2.WechatActiveAgent import WechatActive
from NxSanfran.NxEtc.NxPublic.NxPredefault.PreWechat import *


def wechat2Me(message):
    wechatSender = WechatActive(corpId, secret)
    wechatSender.sendText(agentIdDict['QAinfo'], str(message), toUserList=['bofei'])





