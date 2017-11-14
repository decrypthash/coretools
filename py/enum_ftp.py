#!/usr/bin/env python2.7

# Author: m8r0wn
# Script: enum_ftp.py
# Category: Recon

# Description:
# Check for anonymous FTP logins and enumerate root directory

# Disclaimer:
# This tool was designed to be used only with proper
# consent. Use at your own risk.

import ftplib
import sys
sys.path.append('../resources/')
import coretools

def banner():
    print """
                    Enum FTP

    Script to enumerate the home directory of
    FTP servers. If no username and password are
    provided an anonymous login will be attempted.

    Options:
        -u      Username   (optional)
        -p      Password   (optional)
        -t      Timeout    (default 10)

    Usage:
        python anon_ftp.py 10.0.0.0/24
        python anon_ftp.py 10.0.0.1-10
        python anon_ftp.py 10.0.0.5
    """
    coretools.exit("\n")

def anon_check(targets, username, password,time_out):
    #Attempt FTP login
    for t in targets:
        try:
            # try login
            ftp = ftplib.FTP(t, username, password, timeout=time_out)
            data = []
            #if successful print home dir
            print "[+] %s:%s@%s Connection established" % (username,password,t)
            print "[*] Enumerating root directory..."
            ftp.dir(data.append)
            for dir in data:
                print "    %s " % (dir)
            ftp.quit()
        except ftplib.all_errors as e:
            print "[-] %s:%s@%s Login Failed: %s" % (username,password,t,e)

        except KeyboardInterrupt:
            coretools.exit("\n[!] Keyboard Interrupt Caught...\n\n")
    print "\n"

def main():
    targets = coretools.list_targets(sys.argv[-1])

    #get username
    if "-u" in sys.argv:
        username = coretools.plus_one("-u")
    else: username = "anonymous"

    #get password
    if "-p" in sys.argv:
        password = coretools.plus_one("-p")
    else: password = "nimda@gmail.com"

    if "-t" in sys.argv:
        try:
            timeout = int(coretools.plus_one("-t"))
        except:
            print "\n[-] Invalid timeout, reverting to default..."
            timeout = 2
    else:
        timeout = 2

    anon_check(targets, username, password,timeout)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        coretools.exit("\n[!] Keyboard Interrupt Caught...\n\n")

