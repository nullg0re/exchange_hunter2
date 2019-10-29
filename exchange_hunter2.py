#!/usr/bin/python
import argparse
from ldap3 import Server, Connection, ALL
from colorama import Fore, Style
import json

def get_args():
	p = argparse.ArgumentParser(description="Exchange Hunter via LDAP")
	p.add_argument('-u','--username',type=str,help='username',required=True)
	p.add_argument('-p','--password',type=str,help='password',required=True)
	p.add_argument('-d','--domain',type=str,help='domain',required=True)
	p.add_argument('-t','--target',type=str,help='Target Domain Controller IP Address',required=True)
	p.add_argument('-hn','--hostname',type=str,help="Target Domain Contoller Hostname",required=True)

	args = p.parse_args()

	return args

def main():
	args = get_args()

	# Breakdown DC Hostname for LDAP Connection
	sub = args.hostname.split('.')[0]
	domain = args.hostname.split('.')[1]
	tld = args.hostname.split('.')[-1]

	# Confirm Hostname is FQDN
	if tld not in ['com','org','gov','edu','mil','net']:
		print(Fore.YELLOW+"[*] Top Level Domain is %s, Either adjust script, or adjust target to be FQDN instead of IP." % tld +Style.RESET_ALL)
		print(Fore.RED+"[!] Exiting Now!"+Style.RESET_ALL)

	# Create LDAP Connection
	server = Server(args.target, get_info=ALL)
	conn = Connection(server, user="%s\\%s" % (args.domain, args.username), password="%s" % args.password, authentication="NTLM", auto_bind=True)

	print(Fore.YELLOW+conn.extend.standard.who_am_i()+Style.RESET_ALL)

	# Search for Exchange Servers
	conn.search('cn=Configuration,dc=%s,dc=%s' % (domain, tld), '(objectCategory=msExchExchangeServer)', attributes = ['adminDisplayName'])

	print(Fore.GREEN+Style.BRIGHT+"[+] Exchange Servers Found:"+Style.RESET_ALL)

	for entry in conn.response:
		try:
			print(Fore.GREEN+Style.BRIGHT+entry['attributes']['adminDisplayName']+".%s.%s" % (domain,tld)+Style.RESET_ALL)
		except Exception as e:
			continue

if __name__ == "__main__":
	main()
