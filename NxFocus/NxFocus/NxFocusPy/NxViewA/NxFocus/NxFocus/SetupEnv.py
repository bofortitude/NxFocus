#!/usr/bin/python

import sys
from NxSanfran.NxPrjct.TestingMate.SetupEnvKifer.SetupEnv import setupEnv
from NxSanfran.NxUsr.NxLib.NxLogging import setSimpleLogging


if __name__ == '__main__':
    setSimpleLogging()
    if len(sys.argv) < 2:
        print ''
        print 'Usage:'
        print './SetupEnv.py <Topology File>'
        print '''
Topology File example:

[Client1]
ip = 10.0.12.11
cmd1 = ls
cmd2 = ip add add 10.76.1.11/16 dev eth1.1001

[Server1]
ip = 10.0.12.21
port = 22
username = root
password = fortinet
cmd1 = ip route add 200.1.1.0/24 via 10.78.1.1
        '''
        print ''
        exit()

    setupEnv(sys.argv[1])




