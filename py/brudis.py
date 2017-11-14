#!/usr/bin/env python2.7

# Author: m8r0wn
# Script: brudis.py
# Category: Recon

# Description:
# Brute force HTTP Directories to find
# hidden pages and resources. Based on
# HTTP response codes.

# Disclaimer:
# This tool was designed to be used only with proper
# consent. Use at your own risk.

import urllib2
import ssl
import sys
sys.path.append('../resources/')
import coretools
import coretools_web
from threading import Thread

def banner():
    print """

                    brudis.py

    Multi threaded script to brute-force HTTP directories
    and find hidden resources on a web server.

    Options:
      -t #              Number of threads (default 25, max 50)
      -d #              Dir depth (default 3, max 8)
      -v                Verbose, show response of all requests
      -w [file]         Custom word list

    Usage:
      python brudis.py example.com
      python brudis -d 5 -t 8 http://192.168.1.7

"""
    sys.exit(0)

class brudis():

    depth = [[],[],[],[],[],[],[],[]]

    def __init__(self):
        t_input = sys.argv[-1]
        brudis.depth[0] = brudis.wordlist_prep(self)
        brudis.base_url = coretools_web.https_default(t_input)
        if "-v" in sys.argv:
            brudis.verbose = True
        else:
            brudis.verbose = False
        if "-vv" in sys.argv:
            brudis.debug = True
        else:
            brudis.debug = False

    def wordlist_prep(self):
        # if -w not in sys args use custom list
        if "-w" in sys.argv:
            try:
                list = [x.strip() for x in open(coretools.plus_one('-w'))]
            except:
                # On except revert to default dir list
                print "[!] Error parsing custom word list, reverting to default..."
                list = [x.strip() for x in open('../resources/brudis_dirs.txt')]
        else:
            # Use default list
            list = [x.strip() for x in open('../resources/brudis_dirs.txt')]
        return list

    def start_it(self):
        try:
            #Set Max Threads
            try:
                if "-t" in sys.argv and int(coretools.plus_one("-t")) <= 50:
                    max_threads = int(coretools.plus_one("-t"))
                else:
                    print "[*] Using default thread count..."
                    max_threads = 25
            except:
                print "[!] Error parsing thread input, reverting to default..."
                max_threads = 25
            #Set scan depth
            try:
                if "-d" in sys.argv and int(coretools.plus_one("-d")) <= 8:
                    max_depth = int(coretools.plus_one("-d"))
                else:
                    print "[*] Using default depth..."
                    max_depth = 3
            except:
                print "[!] Error parsing depth input, reverting to default..."
                max_depth = 3

            #start scan
            print "[*] Using max depth: %s, and max threads: %s" % (max_depth, max_threads)
            print "[*] Starting Dir brute force for: %s\n\n" % (brudis.base_url)
            for x in range(0, max_depth):
                if x == 0:
                    temp_url = []
                    # Put urls in temp list
                    for y in brudis.depth[0]:
                        temp_url.append(str(brudis.base_url + y))
                else:
                    temp_url = []
                    # Put urls temp list
                    for a in brudis.depth[x]:
                        for b in brudis.depth[0]:
                            temp_url.append(str(a+b))
                # Setup threading
                url_count = 0
                while url_count != len(temp_url):
                    threads = []
                    for z in range(0, max_threads):
                        #if statement prevents threading from continuing after list is done
                        if url_count != len(temp_url):
                            if brudis.debug:
                                print "[!!] SENDING %s --> thread #%s" % (temp_url[url_count], z)
                            t = Thread(target=brudis.send_it, args=(self, temp_url[url_count], x+1))
                            t.daemon = True
                            threads.append(t)
                            t.start()
                            url_count += 1
                    for t in threads:
                        t.join(1)
        except KeyboardInterrupt:
            coretools.exit("\n[!] Keyboard Interrupt Caught\n")
        except Exception as e:
            if brudis.bedug:
                coretools.exit("\n[!!] Error start_it: %s" % (e))
            else:
                pass

    def send_it(self, url, levelup):
        # ssl cert handling
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        # HTTP Header Setup
        agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'
        request = urllib2.Request(url)
        request.add_header('User-agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36')
        request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')
        request.add_header('Accept-Encoding', 'gzip,deflate,sdch')
        request.add_header('Accept-Language', 'en-US,en;q=0.8,fr;q=0.6')
        request.add_header('Connection', 'keep-alive')
        try:
            # Send it!
            response = urllib2.urlopen(request, timeout=1, context=ctx)
            # Print Response
            sys.stdout.write("[+] %s (Code:%s)\n" % (url, response.getcode()))
            if url.endswith((".php" ,".html", "html", "asp", "aspx", "xml", ".txt")):
                pass
            else:
                brudis.depth[levelup].append(url+"/")
            response.close()
        except urllib2.HTTPError as e:
            if e.code != 404:
                sys.stdout.write("[*] %s (Interesting Response: %s)\n" % (url,e.code))
            elif brudis.verbose:  # debugging
                sys.stdout.write("[-] %s (Error: %s)\n" % (url, e.code))
            else:
                pass
        except Exception as e:
            pass

def main():
    if "-h" in sys.argv or len(sys.argv) == 1: banner()
    dir_scan = brudis()
    dir_scan.start_it()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        coretools.exit("\n[!] Keyboard Interrupt Caught...\n\n")