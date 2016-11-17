#!/usr/bin/python


import dns.name
import dns.message
import dns.query
import dns.flags
import subprocess
import predefined
import threading
import TalkToSystem
import atexit
from signal import signal, SIGTERM
import time
import logging


logger = logging.getLogger()


def dump_info(msg, raw=False):
    if raw == True:
        print str(msg)
    else:
        print '[' + time.ctime() + '] ' + str(msg)


class answer_stat(threading.Thread):

    def __init__(self, thread_list, public_stat_dict, thread_lock, interval=1.0):
        super(answer_stat, self).__init__(name='Thread_monitor')
        self.thread_list = thread_list
        self.public_stat_dict = public_stat_dict
        self.thread_lock = thread_lock
        self.interval = interval

    def run(self):
        while True:
            all_threads_dead = True
            for i in self.thread_list:
                if i.isAlive() == True:
                    all_threads_dead = False
                    break
            if all_threads_dead == True:
                logger.info(str(self.public_stat_dict))
                self.thread_lock.acquire()
                # dump_info(str(self.public_stat_dict))
                self.public_stat_dict.clear()
                self.thread_lock.release()
                break
            logger.info(str(self.public_stat_dict))
            self.thread_lock.acquire()
            # dump_info(str(self.public_stat_dict))
            self.public_stat_dict.clear()
            self.thread_lock.release()

            time.sleep(self.interval)


class ThreadingDnsQuery(threading.Thread):

    def __init__(self, thread_name, lock, request, dns_server, dns_server_port, requests_per_thread=1, interval=1.0, reuse_session=False, same_id=True,
                 src_ip=None, src_port=0, tcp=False, timeout=5.0,
                 record_type='A', show_statistics=False, show_full=False, public_stat_dict={}):
        super(ThreadingDnsQuery, self).__init__(name=thread_name)

        self.lock = lock
        self.requests_per_thread = requests_per_thread
        self.interval = interval
        self.reuse_session = reuse_session
        self.src_ip = src_ip
        self.src_port = src_port
        self.tcp = tcp
        self.timeout = timeout
        self.dns_server = dns_server
        self.dns_server_port = dns_server_port
        self.record_type = record_type
        self.show_statistics = show_statistics
        self.show_full = show_full
        self.request = request
        self.same_id = same_id
        self.public_stat_dict = public_stat_dict

        self.rcode_reason_dict = dns.rcode._by_value

    def _send_request_standard(self, request):
        if self.tcp == False:
            try:
                response = dns.query.udp(request, self.dns_server, timeout=self.timeout,
                                         port=self.dns_server_port, source=self.src_ip, source_port=self.src_port)
                return response
            except Exception as err:
                # dump_info('The query meets error!', raw=True)
                logger.warning('The query meets error!')
                logger.debug(err)
                return False
        else:
            try:

                response = dns.query.tcp(request, self.dns_server, timeout=self.timeout,
                                         port=self.dns_server_port, source=self.src_ip, source_port=self.src_port)
                return response
            except Exception as err:
                # dump_info('The query meets error!', raw=True)
                logger.warning('The query meets error!')
                logger.debug(err)
                return False
        # return  response

    def _response_line(self, section):
        line_result = []
        for i in section:
            result_per_rrset = i.to_text().split('\n')
            for j in result_per_rrset:
                line_result.append(j)
        return line_result

    def _response_handle(self, response):
        status_code = response.rcode()
        status_reason = self.rcode_reason_dict[status_code]
        answers = self._response_line(response.answer)
        additional = self._response_line(response.additional)
        authority = self._response_line(response.authority)
        flags = dns.flags.to_text(response.flags)

        result_dict = {'status_code': status_code,
                       'status_reason': status_reason,
                       'answers': answers,
                       'additional': additional,
                       'authority': authority,
                       'flags': flags}
        return result_dict

    def _statistics_mode(self, response, results):
        if results['status_code'] != 0:
            self.lock.acquire()
            if results['status_reason'] in self.public_stat_dict:
                self.public_stat_dict[results['status_reason']] = self.public_stat_dict[
                    results['status_reason']] + 1
            else:
                self.public_stat_dict[results['status_reason']] = 1
            self.lock.release()
            return False
        else:
            my_answers = results['answers']
            if len(my_answers) < 1:
                return
            p_ansr = my_answers[0].split()
            primary_answer = p_ansr[len(p_ansr) - 1]
            self.lock.acquire()
            if primary_answer in self.public_stat_dict:
                self.public_stat_dict[primary_answer] = self.public_stat_dict[
                    primary_answer] + 1
            else:
                self.public_stat_dict[primary_answer] = 1
            self.lock.release()

    def _query_standard(self):
        for i in xrange(self.requests_per_thread):
            response = self._send_request_standard(self.request)
            if response == False:
                if self.show_statistics == True:
                    self.lock.acquire()
                    if 'Error' in self.public_stat_dict:
                        self.public_stat_dict[
                            'Error'] = self.public_stat_dict['Error'] + 1
                    else:
                        self.public_stat_dict['Error'] = 1
                    self.lock.release()
                time.sleep(self.interval)
                continue
            results = self._response_handle(response)
            if self.show_full == True:
                # self.lock.acquire()
                # dump_info(response, raw=True)
                # dump_info('', raw=True)
                # self.lock.release()
                logger.info(
                    '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n'
                    + 'src ' + str(self.src_ip) + '\n'
                    + str(response) + '\n')
            else:
                if self.show_statistics == True:
                    mode_return = self._statistics_mode(response, results)

                else:

                    if self.record_type == 'A' or self.record_type == 'AAAA':
                        if results['status_code'] != 0:
                            # self.lock.acquire()
                            # dump_info('src ' + str(self.src_ip), raw=True)
                            # dump_info(response, raw=True)
                            # dump_info('', raw=True)
                            # self.lock.release()
                            logger.info(
                                '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n'
                                + 'src ' + str(self.src_ip) + '\n'
                                + str(response) + '\n')
                            if self.same_id == False:
                                self.request.id = dns.entropy.random_16()
                            time.sleep(self.interval)
                            continue
                        my_answers = results['answers']
                        if len(my_answers) < 1:
                            primary_answer = None
                            remain_answers = None
                        else:
                            p_ansr = my_answers[0].split()
                            primary_answer = p_ansr[len(p_ansr) - 1]
                            remain_answers = '('
                            for j in xrange(1, len(my_answers)):
                                c_ansr = my_answers[j].split()
                                remain_answers = remain_answers + \
                                    c_ansr[len(c_ansr) - 1] + ' '
                            remain_answers = remain_answers.rstrip() + ')'

                        shown_result = 'id=' + str(self.request.id) + ' src=' + str(
                            self.src_ip) + ' primary=' + str(primary_answer) + ' remain=' + str(remain_answers)
                        # self.lock.acquire()
                        # dump_info(shown_result, raw=True)
                        # dump_info('', raw=True)
                        # self.lock.release()
                        logger.info(shown_result + '\n')
                    else:
                        # self.lock.acquire()
                        # dump_info('src ' + str(self.src_ip), raw=True)
                        # dump_info(response, raw=True)
                        # dump_info('', raw=True)
                        # self.lock.release()
                        logger.info(
                            '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n'
                            + 'src ' + str(self.src_ip) + '\n'
                            + str(response) + '\n')
            if self.same_id == False:
                self.request.id = dns.entropy.random_16()
            if i != self.requests_per_thread - 1:
                time.sleep(self.interval)

    def _query_reuse(self, statistics):
        pass

    def run(self):

        if self.reuse_session == False:
            self._query_standard()
        else:
            self._query_reuse()


class DnsQuery():

    def __init__(self, dns_server, dns_server_port=53):
        self.dns_server = dns_server
        self.dns_server_port = dns_server_port
        self.flag_type_dict = dns.flags._by_text
        self.record_type_dict = dns.rdatatype._by_text
        self.record_class_dict = dns.rdataclass._by_text
        self.rcode_reason_dict = dns.rcode._by_value

        self.dig_dopt_aaonly = False
        self.dig_dopt_adflag = False
        self.dig_dopt_cdflag = False
        self.dig_dopt_recurse = True

        self.clean_up_resource = TalkToSystem.clean_up()
        atexit.register(self.clean_up_resource.run)
        signal(SIGTERM, lambda signum, stack_frame: exit(1))

        self.ip_cmd = TalkToSystem.IpAddr()
        self.threads_list = []
        self.threading_lock = threading.Lock()
        self.show_full = False
        self.show_statistics = False

    def _request_flag(self, recurse):
        request_flags = 0
        if recurse != None:
            if recurse == True:
                request_flags |= self.flag_type_dict['RD']
        else:
            if self.dig_dopt_recurse == True:
                request_flags |= self.flag_type_dict['RD']
        if self.dig_dopt_aaonly == True:
            request_flags |= self.flag_type_dict['AA']
        if self.dig_dopt_adflag == True:
            request_flags |= self.flag_type_dict['AD']
        if self.dig_dopt_cdflag == True:
            request_flags |= self.flag_type_dict['CD']
        return request_flags

    def _request_domain(self, domain_name):
        my_domain = dns.name.from_text(domain_name)
        if not my_domain.is_absolute():
            my_domain = my_domain.concatenate(dns.name.root)
        return my_domain

    def _assign_ip(self, ip_list):
        self.ip_cmd.config_ip_list(ip_list, self.dns_server)
        for i in self.ip_cmd.ip_cmd_to_clear:
            self.clean_up_resource.add_cmd(i)

    def _new_thread(self, thread_name, request, src_ip=None, src_port=0):
        same_id = self.thopt_same_id
        requests_per_thread = self.thopt_requests_per_thread
        interval = self.thopt_interval
        reuse_session = self.thopt_reuse_session
        tcp = self.thopt_tcp
        timeout = self.thopt_timeout
        record_type = self.thopt_record_type
        show_statistics = self.thopt_show_statistics
        show_full = self.thopt_show_full
        public_stat_dict = self.public_stat_dict

        threading_dns_query_thread = ThreadingDnsQuery(thread_name, self.threading_lock, request, self.dns_server, self.dns_server_port,
                                                       requests_per_thread=requests_per_thread, interval=interval, same_id=same_id,
                                                       reuse_session=reuse_session, tcp=tcp, timeout=timeout, src_ip=src_ip, src_port=src_port,
                                                       record_type=record_type, show_statistics=show_statistics, show_full=show_full, public_stat_dict=public_stat_dict)
        threading_dns_query_thread.setDaemon(True)
        self.threads_list.append(threading_dns_query_thread)

    def _is_thread_alive(self):
        for i in self.threads_list:
            if i.isAlive() == True:
                return True
        return False  # All dead

    def _start_thread(self):
        for i in self.threads_list:
            i.start()
        if self.monitor != None:
            self.monitor.start()

    def _wait_for_thread(self):

        for i in self.threads_list:
            i.join(timeout=31536000)

        if self.monitor != None:
            self.monitor.join(timeout=31536000)

    def _generate_request(self, record_type, rdclass, domain_name, recurse):
        ADDITIONAL_RDCLASS = 4096
        if record_type not in self.record_type_dict:
            record_type = 'A'
        if rdclass not in self.record_class_dict:
            rdclass = 'IN'

        my_domain = self._request_domain(domain_name)
        request = dns.message.make_query(my_domain, self.record_type_dict[record_type],
                                         rdclass=self.record_class_dict[rdclass])

        request.flags = self._request_flag(recurse)
        request.find_rrset(request.additional, dns.name.root, ADDITIONAL_RDCLASS, dns.rdatatype.OPT,
                           create=True, force_unique=True)
        return request

    def start(self, domain_name,
              concurrent_threads=1, requests_per_thread=1, interval=1.0, reuse_session=False,
              src_ip_list=None, src_port_list=None, tcp=False, timeout=5.0,
              record_type='A', recurse=None, rdclass='IN', show_statistics=False, show_full=False, same_id=False):

        self.thopt_same_id = same_id
        self.thopt_requests_per_thread = requests_per_thread
        self.thopt_interval = interval
        self.thopt_reuse_session = reuse_session
        self.thopt_tcp = tcp
        self.thopt_timeout = timeout
        self.thopt_record_type = record_type
        self.thopt_show_statistics = show_statistics
        self.thopt_show_full = show_full
        self.show_full = show_full
        self.show_statistics = show_statistics
        self.public_stat_dict = {}

        if src_ip_list == []:
            src_ip_list = None
        if src_port_list == []:
            src_port_list = None

        if src_ip_list != None:
            # dump_info('Here you can run the look up command from GLB:')
            logger.info('Here you can run the look up command from GLB:\n')
            # dump_info('', raw=True)
            exeCmdString = ''
            for ip_addr in src_ip_list:
                exeCmdString = exeCmdString+'\n'+'execute glb-dprox-lookup ' + ip_addr
                # dump_info('execute glb-dprox-lookup ' + ip_addr, raw=True)
            # dump_info('', raw=True)
            logger.info(exeCmdString+'\n')
            self._assign_ip(src_ip_list)

        if src_ip_list == None:
            if src_port_list != None:
                # dump_info('Generating threads...')
                logger.info('Generating threads...')
                thread_num = 0
                for i in src_port_list:
                    self._new_thread('Thread-' + str(thread_num), self._generate_request(
                        record_type, rdclass, domain_name, recurse), src_port=i)
                    thread_num += 1

            else:
                # dump_info('Generating threads...')
                logger.info('Generating threads...')
                for i in xrange(concurrent_threads):
                    self._new_thread(
                        'Thread-' + str(i), self._generate_request(record_type, rdclass, domain_name, recurse))

        else:
            if src_port_list != None:
                # dump_info('Generating threads...')
                logger.info('Generating threads...')
                thread_num = 0
                for j in src_ip_list:
                    for k in src_port_list:
                        self._new_thread('Thread-' + str(thread_num), self._generate_request(
                            record_type, rdclass, domain_name, recurse), src_ip=j, src_port=k)
                        thread_num += 1

            else:
                thread_num = 0
                # dump_info('Generating threads...')
                logger.info('Generating threads...')
                for j in src_ip_list:
                    for k in xrange(concurrent_threads):
                        self._new_thread('Thread-' + str(thread_num), self._generate_request(
                            record_type, rdclass, domain_name, recurse), src_ip=j)
                        thread_num += 1
        self.monitor = None
        if self.show_statistics == True:
            self.monitor = answer_stat(
                self.threads_list, self.public_stat_dict, self.threading_lock)
            self.monitor.setDaemon(True)

