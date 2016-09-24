#!/usr/bin/python


from ....NxUsr.NxLib.NxWechat2.WechatActiveAgent import WechatActive
from ....NxEtc.NxPublic.NxPredefault.PreWechat import *


def wechat2Me(message):
    wechatSender = WechatActive(corpId, secret)
    wechatSender.sendText(agentIdDict['QAinfo'], str(message), toUserList=['bofei'])





