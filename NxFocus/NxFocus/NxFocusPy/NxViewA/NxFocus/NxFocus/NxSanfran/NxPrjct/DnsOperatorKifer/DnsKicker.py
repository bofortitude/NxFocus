#!/usr/bin/python

import DnsQuery
import argparse
from argparse import RawTextHelpFormatter
from IpNet import ip_net as ip_net
import re
import time
import IpLibHandler

class argument():
    '''Handle arguments'''

    def __init__(self):
        self.ipaddress = ip_net()
        self.match_string1 = re.compile('\[[^][]+]\([^)(]+\)')  # match []()
        arg_usage = '''
./DnsKicker.py <dns-server> <domain-name> [options]

Version 1.00

Notes:


'''
        self.parser = argparse.ArgumentParser(usage=arg_usage, formatter_class=RawTextHelpFormatter)
        self.parser.add_argument('-c', '--concurrent', dest='concurrent', default=1, type=int,
                            help="Specify the concurrent threads number.")
        self.parser.add_argument('-r', '--requests', dest='requests', default=1, type=int,
                            help="Specify the requests number per thread.")
        self.parser.add_argument('-i', '--interval', dest='interval', default=1.0, type=float,
                            help='Interval between requests, default is 1.')
        self.parser.add_argument('-s', '--source-address', dest='source_address',
                            help="Kinds of format are supported:\n1) -s '10.76.1.1,10.77.2.1,10.88.1.1-10.88.2.10,10.100.1.3'\n2) -s '[10.76.1.0/24](10) [10.76.123.0/24](5)'")
        self.parser.add_argument('-p', '--source-port', dest='source_port',
                            help="Format: -p '2234,4532,5423-5490,2452'")
        self.parser.add_argument('-d', '--dns-port', dest='destination_port', default=53, type=int,
                            help='''Specify the dns port, default is 53.''')
        self.parser.add_argument('-n', '--timeout', dest='timeout', default=5, type=float,
                            help='Timeout or every request, default is 5s.')
        self.parser.add_argument('-t', '--tcp', dest='is_tcp', action='store_true',
                            help='Use TCP as transport protocol once it is taken.')
        self.parser.add_argument('-o', '--record-type', dest='record_type', default='A',
                            help='Specify the record type, default is "A".')
        self.parser.add_argument('-m', '--reuse-session', dest='reuse_session', action='store_true',
                            help='Reuse the session to send requests once it is taken.')
        self.parser.add_argument('-f', '--show-full', dest='show_full', action='store_true',
                            help='Show full response info once it is taken.')
        self.parser.add_argument('-w', '--watch-statistics', dest='show_statistics', action='store_true',
                            help='Show statistics info only once it is taken.')
        self.parser.add_argument('--isp-address', dest='isp_address', default=None,
                                 help='''Specify the source addresses from ISP predefined base. Format: \n--isp-address "china-telecom Anhui" \n--isp-address "any Henan"''')
        self.parser.add_argument('--geo-address', dest='geo_address', default=None,
                                 help='Specify the source addresses from GEO IP library. Format: --geo-address "Andorra".')
        self.parser.add_argument('--total-address', dest='total_address', default=1, type=int,
                                 help='Specify total isp address or total geo address, default is 1.')
        self.parser.add_argument('--same-id', dest='same_id', action='store_true',
                            help='Use same message ID for every thread once it is taken.')
        self.parser.add_argument('--no-recurse', dest='recurse', action='store_false',
                            help='Unset the recurse bit once it is taken.')
        self.parser.add_argument('--rdclass', dest='rdclass', default='IN',
                            help='Specify the rdclass, default is "IN".')
        self.parser.add_argument('--aaonly', dest='aaflag', action='store_true',
                            help='Set the aa bit once it is taken.')
        self.parser.add_argument('--adflag', dest='adflag', action='store_true',
                            help='Set the ad bit once it is taken.')
        self.parser.add_argument('--cdflag', dest='cdflag', action='store_true',
                            help='Set the cd bit once it is taken.')

        self.args, self.remaining = self.parser.parse_known_args()

        if len(self.remaining) < 2:
            self.print_help()

        self.concurrent = self.args.concurrent
        self.requests = self.args.requests
        self.interval = self.args.interval
        self.destination_port = self.args.destination_port
        self.timeout = self.args.timeout
        self.is_tcp = self.args.is_tcp
        self.record_type = self.args.record_type
        self.reuse_session = self.args.reuse_session
        self.show_full = self.args.show_full
        self.show_statistics = self.args.show_statistics
        self.same_id = self.args.same_id
        self.recurse = self.args.recurse
        self.rdclass = self.args.rdclass
        self.aaflag = self.args.aaflag
        self.adflag = self.args.adflag
        self.cdflag = self.args.cdflag

        self.dns_server = self.remaining[0]
        self.domain_name = self.remaining[1]


        if self.args.source_address == None:
            self.source_address = None
        else:
            self.source_address = self.handle_src_add()
        if self.args.source_port == None:
            self.source_port = None
        else:
            self.source_port = self.handle_src_port()


        if self.args.isp_address != None:

            isp_addr_list = IpLibHandler.get_ip_list('ISP', self.args.isp_address, self.args.total_address)
            if isp_addr_list != False:
                if self.source_address == None:
                    self.source_address = isp_addr_list
                else:
                    self.source_address = self.source_address+isp_addr_list
        if self.args.geo_address != None:
            if self.dns_server.find(':') == -1:
                #ipv4
                geo_addr_list = IpLibHandler.get_ip_list('Country', self.args.geo_address, self.args.total_address, ipv6=False)
            else:
                #ipv6
                geo_addr_list = IpLibHandler.get_ip_list('Country', self.args.geo_address, self.args.total_address,
                                                         ipv6=True)
            if geo_addr_list != False:
                if self.source_address == None:
                    self.source_address = geo_addr_list
                else:
                    self.source_address = self.source_address+geo_addr_list



    def print_help(self):
        self.parser.print_help()
        exit()


    def handle_src_add(self):
        '''handle source address'''
        src_add_result = []
        if self.match_string1.findall(self.args.source_address) != []:
            # []()
            for infor in self.match_string1.findall(self.args.source_address):
                src_add_result = src_add_result + self.ipaddress.ip_random(infor.split(']')[0].split('[')[1],
                                                                           int(infor.split('(')[1].split(')')[0]))
        else:
            src_add_result = src_add_result + self.ipaddress.ip_range(self.args.source_address)
        return src_add_result

    def handle_src_port(self):
        '''handle source port argument'''
        src_port_result = []
        my_src_port_raw = self.args.source_port
        for infor_comma_separated in my_src_port_raw.split(','):
            if infor_comma_separated.find('-') == -1:
                src_port_result.append(int(infor_comma_separated))
            else:
                by_separator_list = infor_comma_separated.split('-')
                for infor_separator_separated in range(min(int(by_separator_list[0]), int(by_separator_list[1])),
                                                       max(int(by_separator_list[0]), int(by_separator_list[1])) + 1):
                    src_port_result.append(infor_separator_separated)
        return src_port_result



def dump_info(msg, raw=False):
    if raw == True:
        print msg
    else:
        print '['+time.ctime()+'] '+msg





if __name__ == '__main__':
    args = argument()
    dns_sender = DnsQuery.DnsQuery(args.dns_server, dns_server_port=args.destination_port)
    dns_sender.start(args.domain_name, concurrent_threads=args.concurrent, requests_per_thread=args.requests, interval=args.interval,
                     reuse_session=args.reuse_session, src_ip_list=args.source_address, src_port_list=args.source_port, tcp=args.is_tcp,
                     timeout=args.timeout, record_type=args.record_type, recurse=args.recurse, rdclass=args.rdclass,
                     show_statistics=args.show_statistics, show_full=args.show_full)
    dump_info('All threads have been generated.')
    dump_info('Starting threads...')
    dns_sender._start_thread()
    dns_sender._wait_for_thread()

