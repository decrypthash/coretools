#!/user/bin/python2.7

# Author: m8r0wn
# Script: verb_tamper.py
# Category: Recon

# Description:
# script to test HTTP options on web server

# Disclaimer:
# This tool was designed to be used only with proper
# consent. Use at your own risk.

import socket
import sys
import ssl
sys.path.append('../resources/')
import coretools

def banner():
    print '''

    -------------------------------
        Verb Tamper script:
    -------------------------------

    options:
        -ssl        For ssl encryption
        -p [port]   port to send data

    Usage:
    python http_opt.py -p port [server/IP]
    python http_opt.py -p 443 -ssl google.com
    python http_opt.py -p 80 127.0.0.1
    '''
    coretools.exit('\n')

class tamper():
    verbs = ['HEAD', 'GET', 'OPTIONS', 'TRACE', 'PROPFIND', 'TRACK', 'JUNK', 'HELP', 'DEBUG', 123, 'PUT', 'PWD', 'TYPE', 'LIST', 'PASV', 'PWD']
    summary = []

    def __init__(self, target, port, secure):
        self.target = target
        self. port = port
        self.secure = secure

    def add_headers(self, verb):
        #basic http request header
        data = '%s / HTTP/1.1\n' % (verb)
        data += 'Host: %s\n' % (self.target)
        data += 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36\n'
        data += 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\n'
        data += 'Accept-Language: en-US,en;q=0.8,fr;q=0.6\n'
        data += 'Accept-Encoding: gzip,deflate,sdch\n'
        data += 'Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3\n'
        data += 'Connection: keep-alive\n'

        #verb specific headers
        if verb == 'TRACE' or verb == 'TRACK':
            data += 'Data: <script>alert("Cross Site Trace Proof);</script>\n\n'
        elif verb == 'DEBUG':
            data += 'Command: stop-debug\n\n'
        else:
            data += '\n'

        #print request header
        print "\n\n-------------->\nRequest Header\n-------------->"
        print data[:-1]
        return data


    def scan(self, header):
        try:
            #setup connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((self.target, self.port))
            #incorporate ssl TLSv1_1
            if self.secure:
                sock = ssl.wrap_socket(sock, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
            sock.sendall(header)
            #read response
            resp = sock.recv(4096)

            # Add HTTP code to summary report
            self.summary.append(resp.splitlines()[0][9:])
            # Print response header
            print "<--------------\nResponse Header\n<--------------"
            for line in resp.splitlines():
                print line
            sock.close()
        except KeyboardInterrupt:
            coretools.exit("\n[!] Key Event Detected...\n\n")
        except Exception as e:
            print "[-] HTTP Response: ", e
            self.summary.append(e)

    def results(self):
        # summarize findings
        print "---------------\nSummary of Results\n---------------"
        if not self.summary:
            coretools.exit("[!] No Summary Provided\n[*] Check input and try again")
        print "\nTarget: %s    Port: %-5s    SSL: %s \n" % (self.target, self.port, self.secure)
        verbcount = 0
        for s in self.summary:
            print '[*] Verb: %-8s Status:' % (self.verbs[verbcount]), s
            verbcount += 1
        coretools.exit("\n[+] Scan Complete\n")

def main():
    #Help banner
    if "-h" in sys.argv or len(sys.argv) <= 1: banner()

    #Setup info
    target = sys.argv[-1]
    if "://" in target:
        print "\n[!] http / https:// not required, stripping from target..."
        temp = target.split("://")
        target = temp[1]

    #Check if SSL enabled
    if "-ssl" in sys.argv:
        ssl = True
    else:
        ssl = False

    #Get port information
    try:
        port = int(coretools.plus_one("-p"))
    except:
        coretools.exit("\n[-] Error parsing port, see -h for more\n\n")

    try:
        #Start verb tamper
        scan = tamper(target, port, ssl)
        for verb in scan.verbs:
                scan.scan(scan.add_headers(verb))
        #Get Results:
        scan.results()
    except Exception, e:
        coretools.exit("\n Main Error: %s" % (e))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        coretools.exit("\n[!] Key Event Detected...\n\n")