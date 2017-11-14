#!/usr/bin/env python2.7

# Author: m8r0wn
# Script: dns_fun.py
# Category: Recon

# Description:
# + Checks all NS servers for zone transfer
# + Uses DNS to brute force sub-domains
# + Perform DNS queries

# Disclaimer:
# This tool was designed to be used only with proper
# consent. Use at your own risk.

import socket
import sys
import subprocess
import dns.resolver
import dns.zone
sys.path.append('../resources/')
import coretools

def banner():
    print '''
                    DnS_FuN.pY
         -----------------------------------

    DNS Lookup:
        -t [type]           DNS lookup types:
                            [NS, A, AAAA, MX, TXT, CNAME, HINFO, ISDN, PTR, SOA]

        -t all              Lookup all DNS types

    DNS Zone Transfer:
        -z                  Perform DNS Zone Transfer

    Sub-Domain Brute Force:
        -s                  Subdomain Brute force
        -w [file.txt]       custom word list

    Example usage:
        python dns_fun.py -t MX google.com
        python dns_fun.py -z zonetransfer.me
        python dns_fun.py -s yahoo.com'''
    coretools.exit("\n")

class dns_fun():
    def lookup(self, target, type):
        all_types = ['NS', 'A', 'AAAA', 'MX', 'TXT', 'CNAME', 'HINFO', 'ISDN', 'PTR', 'SOA']
        if 'all' in type or 'ALL' in type:
            for type in all_types:
                try:
                    dns_query = dns.resolver.query(target, type)
                    dns_query.nameservers = ['8.8.8.8', '8.8.4.4']
                    if len(dns_query) != 0:
                        # Output
                        print "\n[*] %s records for %s (Count: %s)" % (type, target, len(dns_query))
                        for name in dns_query:
                            print '   ', name
                except Exception as e:
                    print "\n[-] Error in DNS name resolution: %s" % (e)
        else:
            try:
                #DNS Query
                dns_query = dns.resolver.query(target, type)
                dns_query.nameservers = ['8.8.8.8', '8.8.4.4']

                #Display and Log Header
                print "\n[*] %s records for %s (Count: %s)" % (type, target, len(dns_query))

                #Display and Log Data
                for name in dns_query:
                    print '   ', name
            except Exception as e:
                print "\n[-] Error in DNS name resolution: %s" % (e)

    def subdomain_enum(self, target):
        print '\n[*] Sub-Domain Enumeration for: %s'  % (target)
        print '-'*40
        #Get word list
        if "-w" in sys.argv:
            try:
                subs = [x.strip() for x in open(coretools.plus_one('-w'))]
            except:
                print "[!] Error parsing custom word list, reverting to default..."
                subs = [x.strip() for x in open('../resources/subdomain_list.txt')]
        else:
            subs = [x.strip() for x in open('../resources/subdomain_list.txt')]

        for s in subs:
            query = s+'.'+target
            try:
                 #resp = socket.gethostbyname(str(query))
                 # DNS Query
                 resolver = dns.resolver.Resolver()
                 resolver.timeout = 3
                 resolver.lifetime = 3
                 dns_query = resolver.query(query, 'A')
                 dns_query.nameservers = ['8.8.8.8', '8.8.4.4']
                 for resp in dns_query:
                     # Output
                     space_num = len(sys.argv[-1]) + 10
                     print '+ %-*s--> %s' % (space_num, query, resp)
                     #dynamically make output length
                     if dns_fun.logging:
                         coretools.write_file(dns_fun.filename, '%-*s %s' % (space_num,query, resp))

            except Exception as e:
                pass
        coretools.exit("\n")

    def zone_transfer(self, target):
        print '\n[*] DNS Zone Transfer for: %s' % (target)
        print '-' * 40
        #Get Name Servers:
        dns_query = dns.resolver.query(target, "NS")
        dns_query.nameservers = ['8.8.8.8', '8.8.4.4']

        for ns_name in dns_query:
            try:
                z = dns.zone.from_xfr(dns.query.xfr(str(ns_name), target, lifetime=5))
                names = z.nodes.keys()
                names.sort()
                for n in names:
                    #Output
                    print "[+] %s \n" % (z[n].to_text(n))
            except Exception as e:
                print "[!] Error: ",e

def main():
    try:
        #help banner
        if "-h" in sys.argv or len(sys.argv) == 1: banner()

        #quick target input validation
        target = sys.argv[-1]
        if "://" in target or "." * 2 in target:
            coretools.exit("\n[!] DNS_fun Target Error, use -h for more\n\n")

        #new class
        dns_scan = dns_fun()
        if "-t" in sys.argv:
            dns_scan.lookup(target, coretools.plus_one("-t"))
        elif "-z" in sys.argv:
            dns_scan.zone_transfer(target)
        elif "-s" in sys.argv:
            dns_scan.subdomain_enum(target)
        else:
            coretools.exit("\n[-] No options selected, use -h for more information\n\n")
    except Exception as e:
        coretools.exit("[!] Error parsing initial options: %s" % (e))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        coretools.exit("\n[!] Key Event Detected...\n\n")