#!/usr/bin/python

import logging


class cls1(object):
    """docstring for cls1"""

    def __init__(self):
        # super(cls1, self).__init__()
        # self.arg = arg
        pass


def enMain(*args, **kwargs):

    aa = cls1()
    # logger = logging.getLogger()
    # logger.critical(str(aa))
    logging.critical(aa)
