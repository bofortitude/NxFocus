import logging

from .DnsKicker import argument
from . import DnsQuery
from NxSanfran.NxUsr.NxLib.NxLogging import setSimpleLogging


def enMain(sysArgsList):
    args = argument(sysArgsList)

    if args.debug:
        setSimpleLogging(debug=True)
    else:
        setSimpleLogging(debug=False)

    logger = logging.getLogger()

    dns_sender = DnsQuery.DnsQuery(
        args.dns_server, dns_server_port=args.destination_port)
    dns_sender.start(args.domain_name, concurrent_threads=args.concurrent, requests_per_thread=args.requests, interval=args.interval,
                     reuse_session=args.reuse_session, src_ip_list=args.source_address, src_port_list=args.source_port, tcp=args.is_tcp,
                     timeout=args.timeout, record_type=args.record_type, recurse=args.recurse, rdclass=args.rdclass,
                     show_statistics=args.show_statistics, show_full=args.show_full)
    logger.info('All threads have been generated.')
    logger.info('Starting threads...')
    dns_sender._start_thread()
    dns_sender._wait_for_thread()
