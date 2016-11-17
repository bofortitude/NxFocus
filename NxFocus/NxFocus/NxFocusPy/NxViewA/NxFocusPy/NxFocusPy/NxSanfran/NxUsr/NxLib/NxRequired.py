#!/usr/bin/python


import sys
from NxSanfran.NxEtc.NxPublic.NxPredefault.Default import *




def addSanfranLibPath():
	sys.path.insert(0, NxSanfranLibPath)




def delSanfranLibPath():
	while NxSanfranLibPath in sys.path:
		location = sys.path.index(NxSanfranLibPath)
		del sys.path[location]



def doFundamental():
	addSanfranLibPath()








