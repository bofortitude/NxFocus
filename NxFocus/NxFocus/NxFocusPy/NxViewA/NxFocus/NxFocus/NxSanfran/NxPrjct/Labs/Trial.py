#!/usr/bin/python


from ...NxLib import argparse
from ...NxLib.argparse import RawTextHelpFormatter
from ...NxUsr.NxLib import NxFiles










def enMain(argsList):
    from ..NxTestingMate.AdcPatroller.BackupConfig import getAdcSystemStatus
    getAdcSystemStatus('10.160.41.193')










