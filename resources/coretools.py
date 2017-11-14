#!/user/bin/python2.7

# Author: m8r0wn
# Script: coretools.py
# Category: Resource

# Description:
# Set of basic functions commonly used in coretools

# Disclaimer:
# This tool was designed to be used only with proper
# consent. Use at your own risk.

import datetime
import sys
import subprocess
import os
import shutil
import dns.resolver

#Remove a directory and its contents, Linux Only
def remove_dir(path):
    shutil.rmtree(path)

def remove_file(file):
    os.remove(file)

#create folder in output dir for files and get filename
def output_prep(script, ID, ext):
    try:
        #Check if PTS output folder exists
        if not os.path.exists('../output/'):
            os.mkdir('../output/')

        #Check if script logging dir exists
        if not os.path.exists('../output/%s/' % (script)):
            os.mkdir('../output/%s' % (script))

        #Check if same target has ever been scanned
        filename = "../output/%s/%s.%s" % (script, filename_prep(ID), ext)
        if os.path.exists(filename):
            print "\n\n[!] Target already exists in output folder: %s" % (filename)
            retry = raw_input("[*] Do you want to (d) delete file, (a) append file, or (e) exit [d/a/e]:: ")
            if retry == "d":
                try:
                    print "[*] File will be removed\n"
                    remove_file(filename)
                except Exception as e:
                    #print e
                    exit("[-] Error deleting data, please manually delete and try again\n\n")
            elif retry == "a":
                print "[*] File will be appended\n"
            else:
                exit("[*] Closing...\n\n")
        #will return relative file path, used with write_file
        return filename
    except Exception as e:
        exit("\n\n[!] Error creating output files: %s \n[*] Check output folder and try again..." % (e))

#Get file name based off user input as target
def filename_prep(source):
    if "://" in source:
        #avoid https://example.com
        source_temp = source.split("://")
        source = source_temp[1]
    if source.endswith((".php", ".html", ".htm", ".lst", ".xml", ".txt", ".com")):
        #avoid ~/Desktop/file/txt
        source_temp = source.split(".")
        source = source_temp[-2]
        if "/" in source:
            source_temp = source.split("/")
            source = source_temp[-1]
    if "/" in source:
        #avoid https://example.com/
        source_temp = source.split("/")
        source = source_temp[0]
    return source

#Write to File
def write_file(file, data):
    if os.path.exists(file):
        option = 'a'
    else:
        option = 'w'
    OpenFile = open(file, option)
    if option == 'w':
        OpenFile.write('%s' % (data))
    else:
        OpenFile.write('\n%s' % (data))
    OpenFile.close()

#Append a File
def write_file_option(file, data, option):
    OpenFile = open(file, option)
    OpenFile.write('%s' % (data))
    OpenFile.close()


#Line Count File
def line_count(file):
    count = len(open(file).readlines( ))
    return count

#TimeStamp: 07-12-2016 08:01
def time_stamp():
    currentTime = datetime.datetime.now().strftime('%m-%d-%Y %H:%M')
    return currentTime

def time_stamp_two():
    # used for file names
    currentTime = datetime.datetime.now().strftime('%m_%d_%H_%M')
    return currentTime

#Run shell command
def cmd(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    #proc.communicate()[0]                              #output all at once, non recursive
    for line in proc.communicate()[0].splitlines():     #recursive method
        print line

#Basic exit function
def exit(msg):
    print msg
    sys.exit(0)

#Return 0.0% for status messages
def get_percent(count, total):
    return "%.1f%%" % (((1.0 * count) / total) * 100)

#input target sys.argv[-1] and return in list
def list_targets(t_input):
    targets = []
    # pull targets from file
    if ".txt" in t_input:
        try:
            targets = [line.strip() for line in open(t_input)]
            if len(targets[0]) > 16:
                exit("\n\n[-] Line returns detected in file..")
        except:
            exit("\n[-] Error T01: Target error detected.\n[*] Check file path, or use -h for more information\n\n")
    # Targets in CIDR/24 range: 127.0.0.0/24
    elif "/24" in t_input:
        try:
            target = t_input.split("/")
            A1, A2, A3, A4 = target[0].split(".")
            for x in range(0, 256):
                target = A1 + "." + A2 + "." + A3 + "." + `x`
                targets.append(target)
        except:
            exit("\n[-] Error T02: Target error detected..\n[*] Use -h for more information\n\n")
    # DNS name resolution
    elif t_input.endswith(('.com', '.org', '.net', '.gov', '.us', '.ninja', 'local')):
        #multiple domain names yahoo.com,google.com
        if "," in t_input:
            try:
                dom_split = t_input.split(",")
                #print dom_split
                for d in dom_split:
                    dns_query = dns.resolver.query(d, 'A')
                    dns_query.nameservers = ['8.8.8.8', '8.8.4.4']
                    for name in dns_query:
                        targets.append(name)
            except:
                exit("\n[-] Error T001: Error in DNS name resolution\n[*] Ensure proper input is provided, use -h for more\n\n")
        else:
            #single domain name yahoo.com
            try:
                dns_query = dns.resolver.query(t_input, 'A')
                dns_query.nameservers = ['8.8.8.8', '8.8.4.4']
                for name in dns_query:
                    targets.append(name)
            except:
                exit(
                    "\n[-] Error T002: Error in DNS name resolution\n[*] Ensure proper input is provided, use -h for more\n\n")
    # Targets in CIDR/16 range: 127.0.0.0/16
    elif "/16" in t_input:
        try:
            target = t_input.split("/")
            A1, A2, A3, A4 = target[0].split(".")
            for x in range(0, 256):
                for y in range(0,256):
                    target = A1 + "." + A2 + "." + `x` + "." + `y`
                    targets.append(target)
        except:
            exit("\n[-] Error T03: Target error detected..\n[*] Use -h for more information\n\n")
    # Targets in CIDR/8 range: 127.0.0.0/8
    elif "/8" in t_input:
        try:
            target = t_input.split("/")
            A1, A2, A3, A4 = target[0].split(".")
            for x in range(0, 256):
                for y in range(0, 256):
                    for z in range(0, 256):
                        target = A1 + "." + `x` + "." + `y` + "." + `z`
                        targets.append(target)
        except:
            exit("\n[-] Error T04: Target error detected..\n[*] Use -h for more information\n\n")
    # targets in range 127.0.0.1-255
    elif "-" in t_input:
        try:
            A, B = t_input.split("-")
            A1, A2, A3, A4 = A.split(".")
            for x in range(int(A4), int(B) + 1):
                target = A1 + "." + A2 + "." + A3 + "." + `x`
                targets.append(target)
        except:
            exit("\n[-] Error T05: Target error detected..\n[*] Use -h for more information\n\n")
    #Multiiple targets give 127.0.01,127.0.0.1
    elif "," in t_input:
        try:
            for t in t_input.split(","):
                targets.append(t)
        except:
            exit("[-] Error T06: Target error detected..\n[*] Use -h for more information\n\n")
    #Single ip give 127.0.0.1
    elif "." not in t_input or len(t_input) < 7 or "/" in t_input:
        exit("\n[-] Error T07: Target error detected..\n[*] Use -h for more information\n\n")
    else:
        targets.append(t_input)
    return targets

#Give sys arg and return its value -p "password1"
def plus_one(arg_val):
    return sys.argv[sys.argv.index(arg_val)+1]
