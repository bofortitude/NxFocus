#!/usr/bin/python


import DnsQuery



DnsSender = DnsQuery.DnsQuery('10.0.12.195')
print DnsSender.start('app1.testglb.com')





