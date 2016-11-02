import threading
import logging
import socket
import time


from .MalQueryArguments import arguments
from . import RandomGenerator
from NxSanfran.NxUsr.NxLib.NxLogging import setSimpleLogging


logger = logging.getLogger()


class ThreadingMalQuery(threading.Thread):
    """docstring for ClassName"""

    def __init__(self, args):
        super(ThreadingMalQuery, self).__init__()
        self.args = args

    def _buildSock(self):
        logger.debug('Building socket...')
        if str(self.args.dnsServer).find(':') == -1:
            logger.debug('The destination server IP is IPv4 format.')
            afInet = socket.AF_INET
        else:
            logger.debug('The destination server IP is IPv6 format.')
            afInet = socket.AF_INET6
        if self.args.isTcp:
            sock = socket.socket(afInet, socket.SOCK_STREAM)
        else:
            sock = socket.socket(afInet, socket.SOCK_DGRAM)
        sock.settimeout(self.args.timeout)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        logger.debug('The socket has been built over.')
        return sock

    def _send(self, sock, payload):
        logger.debug('Sending malformed query...')
        if self.args.isTcp:
            try:
                sock.connect((self.args.dnsServer, self.args.dstPort))
                sock.send(payload)
            except Exception as err:
                logger.warning('Sending payload via TCP meets error.')
                logger.debug(err)
        else:
            sock.sendto(payload, (self.args.dnsServer, self.args.dstPort))
        logger.info('Malformed query has been sent over.')

    def _checkResult(self, sock):
        logger.debug('Checking the result...')
        if self.args.isTcp:
            try:
                result = sock.recvfrom(self.args.bufferSize)
                logger.warning('Incorrect!! Received payload from remote server:')
                logger.warning(result)
            except Exception as err:
                if str(err).find('Connection reset') != -1:
                    logger.info('The connection has been reset, it is correct.')
                else:
                    logger.warning('The connection meets other error!')
                    logger.debug(err)

        else:
            try:
                result = sock.recvfrom(self.args.bufferSize)
                logger.warning('Incorrect!! Received payload from remote server:')
                logger.warning(result)
            except Exception as err:
                if str(err).find('timed out') != -1:
                    logger.info('The UDP session timed out, it is correct.')
                else:
                    logger.warning('The UDP session meets other error!')
                    logger.debug(err)

    def _close(self, sock):
        if self.args.isTcp:
            try:
                logger.debug('Close TCP socket...')
                sock.close()
            except:
                pass


    def run(self):
        for i in xrange(self.args.requests):
            payload = RandomGenerator.genMalString(self.args.loadLength)
            mySock = self._buildSock()
            self._send(mySock, payload)
            self._checkResult(mySock)
            self._close(mySock)

            logger.debug('Sleep ' + str(self.args.interval) + 's ...')
            time.sleep(self.args.interval)


class MalQuery():
    """docstring for Clas"""

    def __init__(self, args):
        # super(ClassName, self).__()
        self.args = args
        self.threadsList = []

    def _handleArgs(self):
        pass

    def start(self):
        self._handleArgs()
        for i in xrange(self.args.concurrent):
            self.threadsList.append(ThreadingMalQuery(self.args))
        logger.info('All the threads have been generated over.')
        logger.info('Starting all the threads...')
        for j in self.threadsList:
            j.start()
        for k in self.threadsList:
            k.join(timeout=31536000)




def enMain(sysArgsList):
    myArgs = arguments(sysArgsList)
    if myArgs.debug:
        setSimpleLogging(debug=True)
    else:
        setSimpleLogging(debug=False)
    malQuerier = MalQuery(myArgs)
    malQuerier.start()





