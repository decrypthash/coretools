#!/user/bin/python2.7

# Author: m8r0wn
# Script: webdav_scanner.py
# Category: Recon

# Description:
# Check if webdav enabled on server using http
# response codes and the propfind method

# Disclaimer:
# This tool was designed to be used only with proper
# consent. Use at your own risk.


import socket
from threading import Thread
import sys
sys.path.append('../resources/')
import coretools

def banner():
    print """

             WebDav Scanner

    -t          Number of threads (default: 5)
    -p          Port (default: 80)
    -v          verbose output

    Usage:
        python webdav_scanner.py 10.0.0.0/24
        python webdav_scanner.py -v 192.168.2.1-20

    """
    sys.exit(0)

def main():
    # Help banner
    if "-h" in sys.argv or len(sys.argv) == 1: banner()


    targets = coretools.list_targets(sys.argv[-1])

    #verbose output
    if "-v" in sys.argv:
        v = True
    else:
        v = False

    # set max threads
    if "-t" in sys.argv:
        try:
            max_threads = int(coretools.plus_one("-t"))
        except:
            print "[!] Error parsing max pages, reverting to default"
            max_threads = 5
    else:
        max_threads = 5

    # set max threads
    if "-p" in sys.argv:
        try:
            port = int(coretools.plus_one("-p"))
        except:
            print "[!] Error parsing max pages, reverting to default"
            coretools.exit("[!] Invalid port detected\n\n")
    else:
        port = 80

    print "\n[*] Starting WebDav Scan\n"
    #start scan
    scan_count = 0

    while scan_count != len(targets):
        threads = []
        for z in range(0, max_threads):
            if scan_count != len(targets):
                x = Thread(target=scan, args=(targets[scan_count], port, v,))
                threads.append(x)
                x.daemon = True
                x.start()
                scan_count += 1
        for t in threads:
            t.join(1)
    coretools.exit("\n[!] Scan Complete\n\n")

def scan(t, port, v):
    # Setup Socket Connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    # HTTP Request Header
    data = 'PROPFIND / HTTP/1.1\n'
    data += 'Host: %s\n' % (t)
    data += 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36\n'
    data += 'Content-Type: application/xml\n'
    data += 'Content-Length: 0\n\n'

    try:
        sock.connect((t, port))
        sock.send(data)
        resp = sock.recv(2014)

        sys.stdout.flush()
        x = resp.splitlines()[0]
        # pull http code for summary
        if "200" in x or "207" in x:
            sys.stdout.write("[+] WebDav Enabled: %s (Code: %s)\n" % (t, x.split(" ")[1]))
        else:
            sys.stdout.write("[-] WebDav Disabled: %s (Code: %s)\n" % (t, x.split(" ")[1]))

        sock.close()
    except KeyboardInterrupt:
        sock.close()
        coretools.exit("\n[!] Key Event Detected...\n\n")
    except Exception as e:
        if v:
            sys.stdout.write("[-] WebDav Disabled: %s (%s)\n" % (t, e))
        sock.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        coretools.exit("\n[!] Key Event Detected...\n\n")