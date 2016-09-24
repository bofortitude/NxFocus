#!/usr/bin/python


from ...NxLib import argparse
from ...NxLib.argparse import RawTextHelpFormatter
from ...NxUsr.NxLib import NxFiles










def enMain(argsList):
    print NxFiles.sortDir('/root/NxFocus/NxFocus')
    print NxFiles.sortDirReverse('/root/NxFocus/NxFocus')










