#!/usr/bin/python


import sys


def getFuncList():
    funcList = []
    exceptList = ['getFuncList', 'showHelp', 'sys']

    for i in entireFuncList:
        if i not in exceptList and i[0] != '_':
            funcList.append(i)
    return funcList

def showHelp():
    print ''
    print 'Usage:'
    print ''
    print str(sys.argv[0])+' <project name> [arguments]'
    print ''
    print 'Available projects:'
    print getFuncList()
    print ''
    exit()

def Info4Us(argsList):
    from NxSanfran.NxPrjct.iMer.Info4Us.Info4Us import mainEn
    mainEn()

def checkConnBeijing(argsList):
    from NxSanfran.NxPrjct.iMer.CheckConnectivity.CheckConnToBeijing import mainEn
    mainEn()

def Trial(*argsList):
    from NxSanfran.NxPrjct.Labs.Trial import enMain
    enMain(*argsList)



entireFuncList = dir()

if __name__ == '__main__':
    if len(sys.argv) <2:
        showHelp()
    else:
        try:
            eval(str(sys.argv[1]))(sys.argv[2:])
        except Exception as err:
            showHelp()








