#!/usr/bin/python

import subprocess
import time


def run_shell_cmd(command, ok_msg=None, error_msg=None, doRaise=True, debug_info=False):
    '''Return the status code'''
    if debug_info == True:
        print '[Run: ' + command + ']'

    shell_run = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    return_string = ''
    status_code = shell_run.wait()
    for line in shell_run.stdout.readlines():
        if debug_info == True:
            print line
        return_string = return_string + line
    if status_code == 0:
        if debug_info == True:
            print ok_msg
    else:
        if doRaise == True:
            if debug_info == True:
                print error_msg
            raise RuntimeError(error_msg, 'in TalkToSystem.py')
        else:
            if debug_info == True:
                print error_msg
        return False
    return return_string


class clean_up():
    '''Clean up resources'''

    def __init__(self):
        self.cmd = []

    def run(self):
        # time.sleep(1)
        if self.cmd:
            for mycmd in self.cmd:
                # print mycmd
                run_shell_cmd(mycmd)
        # print 'All the resources have been cleaned up.'

    def add_cmd(self, cmd):
        self.cmd.append(cmd)


class IpAddr():

    def __init__(self):
        self.ip_cmd_to_clear = []

    def _config_ip(self, ip_address, out_interface):
        '''Figure out the out interface and assign IP address to it.'''
        if ip_address.find(':') == -1:
            # IPv4 address
            ip_add_add_result = run_shell_cmd(
                'ip add add ' + ip_address + '/32 dev ' + out_interface, doRaise=False)
            self.ip_cmd_to_clear.append(
                'ip add del ' + ip_address + '/32 dev ' + out_interface)
        else:
            # IPv6 address
            ip_add_add_result = run_shell_cmd(
                'ip add add ' + ip_address + '/128 dev ' + out_interface, doRaise=False)
            self.ip_cmd_to_clear.append(
                'ip add del ' + ip_address + '/128 dev ' + out_interface)
        # return out_interface

    def config_ip_list(self, ip_list, dst_ip):
        ip_route_get_result = run_shell_cmd('ip route get ' + dst_ip)
        out_interface = ip_route_get_result.split('dev')[1].split()[0]
        if_src_ipv6 = False
        for i in ip_list:
            if i.find(':') != -1:
                if_src_ipv6 = True
            self._config_ip(i, out_interface)

        if if_src_ipv6 == True:
            print 'Waiting for the tentative status of new added IPv6 address over.'
            for wait in xrange(40):
                if run_shell_cmd('ip address show ' + out_interface + ' | grep inet6 | grep tentative') == '':
                    break
                time.sleep(0.1)

    def clear_current_ip(self):
        for i in self.ip_cmd_to_clear:
            run_shell_cmd(i)


#clean_up_resource = clean_up()
# atexit.register(clean_up_resource.run)
# Normal exit when killed
#signal(SIGTERM, lambda signum, stack_frame: exit(1))
