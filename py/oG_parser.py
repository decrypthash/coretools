#!/user/bin/python2.7

# Author: m8r0wn
# Script: oG_parser.py
# Category: Recon

# Description
# Parse: nmap -sP -oG file.txt -T5 10.0.0.0/8
# OR
# Parse: masscan -p ANYPORTS -oG file.txt --rate 100000 10.0.0.0/8
# Will create a .txt list of IP's for input into a vuln scanner

# Disclaimer:
# This tool was designed to be used only with proper
# consent. Use at your own risk.

import sys
import os
sys.path.append('../resources/')
import coretools

def banner():
    print """
                  oG_parser.py
    Takes the output of nmap and masscan -oG option
    and turns it into a .txt list of targets. This can
    be used to further fingerprint or upload to a vuln
    scanning program.

    Usage:
        oG_parse.py nmap_output.txt
        oG_parse.py ~/Desktop/out_file.txt

    """
    coretools.exit("\n")

def main():
    #Display help banner
    if "-h" in sys.argv or len(sys.argv) == 1: banner()

    #Start logic to read/parse input file
    dups = []
    count = 0
    file = sys.argv[-1]
    if not os.path.exists(file):
        print "\n[!] File not found, please try again\n\n"
        sys.exit(0)
    openSesame = open(file)
    for line in openSesame.readlines():
        if "Host:" in line:
            puller = line.split(" ")
            #check for duplicates
            if puller[1] not in dups:
                count += 1
                print puller[1]
                dups.append(puller[1])
    openSesame.close()
    coretools.exit("[+] oG_parser Complete!\n[+] %s unique targets found!\n\n" % (count))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        coretools.exit("\n[!] Key Event Detected...\n\n")
