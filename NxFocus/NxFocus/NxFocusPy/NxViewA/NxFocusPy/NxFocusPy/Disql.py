#!/usr/bin/python

from NxSanfran.NxUsr.NxLib.NxLogging import setSimpleLogging

from NxSanfran.NxPrjct.NxSqlMaster.DiSql import DiSql


if __name__ == '__main__':
    setSimpleLogging()


    DiSql.diSql()

