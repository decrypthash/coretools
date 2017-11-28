#!/usr/bin/env python2.7

# Author: m8r0wn
# Script: spider.py
# Category: Recon

# Description:
# Multi threaded script to spider/crawl
# webpages looking for all links. Will search
# for admin, login, and dynamic pages in
# addition to emails. It will write all found
# links to a file.


# Disclaimer:
# This tool was designed to be used only with proper
# consent. Use at your own risk.

import urllib2
import sys
from BeautifulSoup import BeautifulSoup
from threading import Thread
import ssl
import os
sys.path.append('../resources/')
import coretools
from time import sleep


def banner():
	print """
		      Spider.py

	Multi threaded web spider looking for emails,
	login pages, admin pages, and dynamic pages. Will
	log links to output folder for review.

	-c		Max Number of pages to crawl (Default: 50)
	-t		Max Number of threads (Default: 5)

	Usage:
	python spider.py -t 4 -c 55 http://yoursite.com
	python spider.py https://yoursite.com

	"""
	sys.exit(0)

class spider():
	email_count = 0
	emails = []
	login_count = 0
	login_pages = []
	admin_count = 0
	admin_pages = []
	dynamic_count = 0
	dynamic_pages = []
	pages = []

	def __init__(self, url, max_pages, max_threads):
		#Set class variables
		self.protocol = url.split('://')[0]
		self.source = url.split('://')[1]
		self.max_pages = max_pages
		self.max_threads = max_threads
		self.dir = self.setup_logging()

		#init pages list
		self.pages.append(url)
		print "[*] Setting Thread Count: %s & Max Pages: %s" % (max_threads, max_pages)
		#start spider
		self.crawler()

	def setup_logging(self):
		try:
			if not os.path.exists('spider_output/'):
				os.mkdir('spider_output/')

			dir = "spider_output/%s/" % (self.source[0:5])
			if not os.path.exists(dir):
				os.mkdir(dir)
			else:
				print "[!] Spider of site detected..."
				req = raw_input("[*] Delete existing records? (Y/n): ")
				if req == "n" or req == "N":
					print "\n\n[*] Closing\n"
					sys.exit(0)
				coretools.remove_dir(dir)
				os.mkdir(dir)
			return dir
		except Exception, e:
			coretools.exit("[!] Setup Logging Error: %s" % (e))

	def status(self,crawl_count):
		sys.stdout.flush()
		if crawl_count != 0:
			sys.stdout.write("\x1b[A\x1b[A\x1b[A\x1b[A\x1b[A\x1b[A\x1b[A\x1b[A")
		sys.stdout.write("%-20s %s\n" % ("Pages Crawled:", crawl_count))
		sys.stdout.write("%-20s %s\n" % ("Dynamic Pages:", self.dynamic_count))
		sys.stdout.write("%-20s %s\n" % ("Emails Collected:", self.email_count))
		sys.stdout.write("%-20s %s\n" % ("Login Pages:", self.login_count))
		sys.stdout.write("%-20s %s\n" % ("Admin Pages:", self.admin_count))
		sys.stdout.write("%-20s %s\n" % ("Total Pages:", len(self.pages)))
		try:
			sys.stdout.write("\n[+] %s\n" % (self.pages[crawl_count][0:60]))
		except:
			sys.stdout.write("\n[+] %s\n" % (self.source))

	def crawler(self):
		print "[*] Initializing Scan...\n\nSpider Stats:\n","-"*35
		crawl_count = 0
		while crawl_count < self.max_pages and crawl_count != len(self.pages):
			try:
				threads = []
				self.status(crawl_count)
				for z in range(0, self.max_threads):
					if crawl_count < self.max_pages and crawl_count != len(self.pages):
						t = Thread(target=self.request_handler, args=(self.pages[crawl_count],))
						t.daemon = True
						threads.append(t)
						t.start()
						crawl_count += 1
				for t in threads:
					t.join(1)
				#Give time for first threaad to collect links
				if crawl_count == 1:
					sleep(5)
			except KeyboardInterrupt:
				coretools.exit("\n[!] Key Event Detected...\n")
			except Exception, e:
				pass
				#print "[!] Crawler Error: ", e
		self.status(crawl_count)
		sys.stdout.write("\x1b[A")
		coretools.exit(" " * 65 + "\n[*] Scan Complete\n")

	def request_handler(self, url):
		# Setup Request
		agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'
		request = urllib2.Request(url)
		request.add_header('User-Agent', agent)
		request.add_header('Referer', self.source)

		# ssl cert handling
		ctx = ssl.create_default_context()
		ctx.check_hostname = False
		ctx.verify_mode = ssl.CERT_NONE
		try:
			# Capture response
			response = urllib2.urlopen(request, timeout=2, context=ctx)
			# If page html, parsing for links
			if "html" in response.info().getheader('Content-Type') or "application" in response.info().getheader("Content-Type"):
				soup = BeautifulSoup(response)
				for link in soup.findAll('a'):
					# Convert link to string
					link = str(link.get('href'))

					#Check for dynamic pages
					if link.startswith("/"):
						link = self.protocol + "://" + self.source + link

					if self.source in link and link not in self.pages:
						self.pages.append(link)

						if "=" in link:
							link = link.split("=")[0] + "="
							if link not in self.dynamic_pages:
								self.dynamic_count += 1
								self.dynamic_pages.append(link)
								coretools.write_file("%s/%s_dynamic.txt" % (self.dir, self.source[0:5]), link)

						elif "admin" in link and link not in self.admin_pages:
							self.admin_count += 1
							self.admin_pages.append(link)
							coretools.write_file("%s/%s_admin.txt" % (self.dir, self.source[0:5]), link)

						elif "login" in link and link not in self.login_pages:
							self.login_count += 1
							self.login_pages.append(link)
							coretools.write_file("%s/%s_login.txt" % (self.dir, self.source[0:5]), link)

						else:
							coretools.write_file("%s/%s_spider.txt" % (self.dir, self.source[0:5]), link)
					#Check for Emails
					elif link.startswith("mailto:"):
						email = link.split("mailto:")[1]
						if email not in self.emails:
							self.email_count += 1
							self.emails.append(email)
							coretools.write_file("%s/%s_emails.txt" % (self.dir, self.source[0:5]), email)
			response.close()
		except Exception, e:
			#print "[!] Threading Error: ", e
			pass


def main():
	#Help banner
	if "-h" in sys.argv or len(sys.argv) == 1: banner()

	#starting url prep
	url = sys.argv[-1]
	if "://" not in url:
		print "\n\n[!] Must include http:// | https:// tag"
		print "[!] see ./spider.py --help for more\n\n"
		sys.exit(0)

	if url.endswith("/"):
		url = url.rstrip("/")

	#set max pages to spider
	if "-c" in sys.argv:
		try:
			max_pages = int(sys.argv[sys.argv.index("-c")+1])
		except:
			print "[!] Error parsing max pages, reverting to default"
			max_pages = 50
	else:
		max_pages = 50

	#set max threads
	if "-t" in sys.argv:
		try:
			max_threads = int(sys.argv[sys.argv.index("-t")+1])
		except:
			print "[!] Error parsing max pages, reverting to default"
			max_threads = 5
	else:
		max_threads = 5

	try:
		scan = spider(url, max_pages, max_threads)

	except KeyboardInterrupt:
		coretools.exit("\n[!] Key Event Detected...\n")
	except Exception, e:
		pass
		#print "\n\n[!] Main Error: ", e
		#sys.exit(1)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		coretools.exit("\n[!] Key Event Detected...\n")