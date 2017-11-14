#!/usr/bin/env bash

#Check if Script run as root
if [[ $(id -u) != 0 ]]; then
	echo -e "\n[!] Setup script needs to run as root\n\n"
	exit 0
fi

echo -e "\n[*] Starting coretools setup script"

echo -e "[*] Checking for Python 2.7"
if [[ $(python2.7 -V 2>&1) == *"not found"* ]]
then
    echo -e "[*] Installing Python 2.7"
    apt-get install python2.7 -y
else
    echo "[+] Python 2.7 installed"
fi

echo -e "[*] Checking for modules outside standard libraries"

if [[ $(python2.7 -c "import BeautifulSoup" 2>&1) == *"No module"* ]]
then
    echo -e "[*] Installing python-beautifulsoup"
    apt-get install python-beautifulsoup -y
else
    echo "[+] BeautifulSoup installed"
fi

if [[ $(python2.7 -c "import dns.resolver" 2>&1) == *"No module"* ]]
then
    echo -e "[*] Installing python-dnspython"
    apt-get install python-dnspython -y
else
    echo "[+] dnspython installed"
fi

echo -e "\n[*] coretools setup complete\n\n"