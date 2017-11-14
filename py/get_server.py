#!/usr/bin/env python2.7

# Author: m8r0wn
# Script: get_server.py
# Category: Recon

# Description:
# Fingerprint systems/service/version using
# 'Server:' HTTP Response header

# Disclaimer:
# This tool was designed to be used only with proper
# consent. Use at your own risk.

import urllib2
import ssl
import sys
from threading import Thread
sys.path.append('../resources/')
import coretools

def banner():
    print """
                        Get_Server

    This script will connect to the target machine(s) and return
    the HTTP response "Server" header. Used for recon and
    fingerprinting target machines.

    Method:
    -m [http/https]         Default will be both http & https
    -v                      Verbose output (show failed attempts)
    -t                      Number of threads (default: 5)

    Targets:
    *) python get_server.py -m http scope.txt
    *) python get_server.py 10.0.0.1
    *) python get_server.py 10.0.0.1-5
    *) python get_server.py 10.0.0.1,10.0.0.3
    *) python get_server.py 10.0.0.0/24

    """
    coretools.exit("\n")

def status_report(methods, target_count):
    print "\n[*] Targets acquired: %s (IP count: %s)" %  (sys.argv[-1], target_count)
    print "[*] Using Method(s): ",
    for method in methods: print method,

def scan(target, methods, verbose):
    #flush output
    sys.stdout.flush()
    #Start scan
    output = []
    for method in methods:
        url = str(method)+str(target)
        try:
            # ssl cert handling (bypass)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            #HTTP Header Setup
            request = urllib2.Request(url)
            request.add_header('User-agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36')
            request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
            request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')
            request.add_header('Accept-Encoding', 'gzip,deflate,sdch')
            request.add_header('Accept-Language', 'en-US,en;q=0.8,fr;q=0.6')
            request.add_header('Connection', 'keep-alive')

            # Capture response
            response = urllib2.urlopen(request, timeout=2, context=ctx)
            server_info = response.info().getheader('Server')
            if server_info not in output and "None" not in str(server_info):
                sys.stdout.write("[+] %-32s  Server: %s\n" % (url, server_info))
                output.append(server_info)
            else:
                if verbose:
                    sys.stdout.write("[-] %-32s  Server: N/A\n" % (url))
            response.close()
        except urllib2.HTTPError as e:
            server_info = e.info().getheader('Server')
            if server_info not in output and "None" not in str(server_info):
                sys.stdout.write("[+] %-32s  Server: %s\n" % (url, server_info))
                output.append(server_info)
            else:
                if verbose:
                    sys.stdout.write("[-] %-32s  Server: N/A\n" % (url))

        except Exception as e:
            if verbose:
                sys.stdout.write("[-] %-32s  Server: %s\n" % (url,e))

def main():
    #help check
    if "-h" in sys.argv or len(sys.argv) == 1: banner()

    #Choose Scan methods
    if "-m" in sys.argv and coretools.plus_one("-m") == "http": methods = ['http://']
    elif "-m" in sys.argv and coretools.plus_one("-m") == "https": methods = ['https://']
    else: methods = ['http://', 'https://']

    #verbose = show failed attempts
    if "-v" in sys.argv:
        verbose = True
    else:
        verbose = False

    # set max threads
    if "-t" in sys.argv:
        try:
            max_threads = int(coretools.plus_one("-t"))
        except:
            print "[!] Error parsing max pages, reverting to default"
            max_threads = 5
    else:
        max_threads = 5

    #Start program
    targets = coretools.list_targets(sys.argv[-1])
    status_report(methods, len(targets))

    print "\n[*] Starting Scan...\n"
    scan_count = 0

    while scan_count != len(targets):
        threads = []
        #Start Threads
        for x in range(0, max_threads):
            if scan_count != len(targets):
                t = Thread(target=scan, args=(targets[scan_count], methods, verbose,))
                t.daemon = True
                threads.append(t)
                t.start()
                scan_count += 1
        for t in threads:
            t.join(1)
    coretools.exit("\n[!] Scan Complete\n\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        coretools.exit("\n[!] Keyboard Interrupt Caught...\n\n")
