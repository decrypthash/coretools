#!/user/bin/python2.7

# Author: m8r0wn
# Script: paste_passwords.py
# Category: Info Gathering

# Description:
# Script to parse Pastebin's trendings pastes and
# return all email and password combinations

# Disclaimer:
# This tool was designed to be used only with proper
# consent. Use at your own risk.

import re
import sys
import urllib2
import urllib

def list_trending(api_key):
    #list Trending Pastes:

    data = {'api_dev_key': api_key,
            'api_option': 'trends'}
    req = urllib2.urlopen('https://pastebin.com/api/api_post.php', urllib.urlencode(data).encode('utf-8'), timeout=7)
    return req.read()

def show_paste(paste_key):
    # Print Raw paste
    req = urllib2.urlopen('https://pastebin.com/raw/' + paste_key, timeout=7)
    return req.read()

def get_txt(data):
    #Get text from inside XML tags
    try:
        temp = data.split("</")
        temp2 = temp[0].split(">")
        return temp2[1]
    except:
        return False

def main():
    #API Key Here:
    api_key = ''
    pwd_format = re.compile('[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+:[a-zA-Z0-9._-]+')
    paste_keys = []

    if api_key == '':
        print "\n[!] Please insert your Pastebin account's API Key to continue\n\n"
        sys.exit(0)

    #pull all keys from trending Pastes
    for line in list_trending(api_key).splitlines():
        if '<paste_key>' in line:
            try:
                paste_keys.append(get_txt(line))
            except:
                pass

    #get content for each paste_key
    for key in paste_keys:
        for line in show_paste(key).splitlines():
            #print line
            #search email@domain:password format
            if pwd_format.match(line):
                # split email from password
                tmp = line.split(":")
                #check for errors via blank password
                #print tmp[1]
                if not tmp[1]: break
                # check for spaces after password
                if " " in tmp[1]:
                    passwd = tmp[1].split(" ")
                    print "Email: %-32s Password: %s" % (tmp[0].strip(), passwd[0].strip())
                else:
                    print "Email: %-32s Password: %s" % (tmp[0].strip(), tmp[1].strip())

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\n[!] Keyboard Interrupt Caught...\n\n")