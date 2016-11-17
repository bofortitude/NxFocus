#!/usr/bin/python

import logging
import socket

def ab():
    UDP_IP = '127.0.0.1'
    UDP_PORT = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while  True:
        data, addr = sock.recvfrom(1024)
        sock.sendto('reply message', addr)
        print 'received message:', data
        print addr






def enMain(*args, **kwargs):
    ab()
