#!/user/bin/python2.7

# Author: m8r0wn
# Script: coretools_web.py
# Category: Resource

# Description:
# Set of functions pertaining to web functionality for coretools

# Disclaimer:
# This tool was designed to be used only with proper
# consent. Use at your own risk.

import urllib2
import ssl
import sys
sys.path.append('../resources/')
from coretools import exit

def get_domain(source):
    if "://" in source:
        source_temp = source.split("://")
        source = source_temp[1]
    if source.endswith("/"):
        source_temp = source.split("/")
        source = source_temp[0]
    return source

def https_default(target):
    #Prep target domain for scanning, will return https://target.com/
    #Check if target has domain extension
    if "." not in target:
        exit("\n[!] Error Invalid target, try again...\n\n")

    #check for Protocol Identifier
    try:
        if "://" not in target:
            # modify for url
            print "\n[!] http:// or https:// not privided...\n[*] Defaulting to: https://"
            target = str("https://" + target)

    #if target ends with /
        if target.endswith("/"):
            return target
        else:
            return str(target + "/")
    except Exception as E:
        # print E
        exit("[!] Error prepairing target for scan...")

def get_server(url):
    #Will return HTTP response header Server field
    try:
        # ssl cert handling (bypass)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        # HTTP Header Setup
        request = urllib2.Request(url)
        # request.add_header('Host', target)
        request.add_header('User-agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36')
        request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')
        request.add_header('Accept-Encoding', 'gzip,deflate,sdch')
        request.add_header('Accept-Language', 'en-US,en;q=0.8,fr;q=0.6')
        request.add_header('Connection', 'keep-alive')

        # Capture response
        response = urllib2.urlopen(request, timeout=2, context=ctx)
        server_info = response.info().getheader('Server')
        response.close()
    except urllib2.HTTPError as e:
        server_info = e.info().getheader('Server')
    except Exception as i:
        server_info = "[-] Error %s: %s" % (url, i)
    return server_info

def get_header(url):
    #Will return HTTP response header
    try:
        # ssl cert handling (bypass)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        # HTTP Header Setup
        request = urllib2.Request(url)
        # request.add_header('Host', target)
        request.add_header('User-agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36')
        request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')
        request.add_header('Accept-Encoding', 'gzip,deflate,sdch')
        request.add_header('Accept-Language', 'en-US,en;q=0.8,fr;q=0.6')
        request.add_header('Connection', 'keep-alive')

        # Capture response
        response = urllib2.urlopen(request, timeout=2, context=ctx)
        server_info = response.info()
        response.close()
    except urllib2.HTTPError as e:
        server_info = e.info()
    except Exception as i:
        server_info = "[-] Error %s: %s" % (url, i)
    return server_info