#!/usr/bin/env python2.7

# Author: m8r0wn
# Script: get_header.py
# Category: Recon

# Description:
# Pull back whole HTTP Response header

# Disclaimer:
# This tool was designed to be used only with proper
# consent. Use at your own risk.

import urllib2
import ssl
import sys
sys.path.append('../resources/')
import coretools
from coretools_web import get_header

def banner():
    print """
                        Get_Header

    This script will connect to the target machine(s) and return
    the full HTTP response header. This will test both http and
    https unless otherwise noted in the command line arguments.
    Used for recon and fingerprinting target machines.

    Method:
    -m [http/https]         Default will be both http & https
    -v                      Verbose output (show failed attempts)

    Targets:
    *) python get_header.py -m http scope.txt
    *) python get_header.py 10.0.0.1
    *) python get_header.py -nw 10.0.0.0/24
    *) python get_header.py 10.0.0.1, 10.0.0.3
    *) python get_header.py 10.0.0.1-50
    """
    coretools.exit("\n")

def status_report(methods, target_count):
    print "\n[*] Targets acquired: %s (IP count: %s)" % (sys.argv[-1], target_count)
    print "[*] Using Method(s): ",
    for method in methods: print method,

def start_scan(targets, methods):
    print "\n[*] Starting Scan...\n\n"

    #verbose = show failed attempts
    if "-v" in sys.argv:
        verbose = True
    else:
        verbose = False

    num_count=0
    for target in targets:
        #progress counter triggers every 20 targest that are scanned
        if num_count != 0 and num_count%20 == 0:
            print "[*] get_header.py Status: ", coretools.get_percent(num_count,len(targets))
        #Start scan
        output = []
        for method in methods:
            try:
                #Create URL
                url = str(method) + str(target)
                # Get Header
                response = get_header(url)
                print "\n[+] Target: %s" % (url)
                print response
            except KeyboardInterrupt:
                coretools.exit("\n[!] Keyboard Interrupt Caught...\n\n")
            except Exception as e:
                if verbose:
                    print "\n[-] Target: %s" % (url)
                    print e
        num_count += 1
    coretools.exit("\n[!] Scan Complete\n\n")

def main():
    #help check
    if "-h" in sys.argv or len(sys.argv) == 1: banner()

    #Choose Scan methods
    if "-m" in sys.argv and coretools.plus_one("-m") == "http": methods = ['http://']
    elif "-m" in sys.argv and coretools.plus_one("-m") == "https": methods = ['https://']
    else: methods = ['http://', 'https://']
    #Start Scan
    targets = coretools.list_targets(sys.argv[-1])
    status_report(methods, len(targets))
    start_scan(targets, methods)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        coretools.exit("\n[!] Keyboard Interrupt Caught...\n\n")