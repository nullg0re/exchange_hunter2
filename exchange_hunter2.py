#!/usr/bin/python
import argparse
from ldap3 import Server, Connection, ALL
from colorama import Fore, Style

def get_args():
	p = argparse.ArgumentParser(description="Exchange Hunter via LDAP")
	p.add_argument('-u','--username',type=str,help='username',required=True)
	p.add_argument('-p','--password',type=str,help='password',required=True)
	p.add_argument('-d','--domain',type=str,help='domain.com',required=True)
	p.add_argument('-t','--target',type=str,help='Target Domain Controller',required=True)

	args = p.parse_args()

	return args

def main():
	args = get_args()

	if args.domain.split('.')[2]:
		sub = args.domain.split('.')[0]
		domain = args.domain.split('.')[1]
		tld = args.domain.split('.')[2]
	else:
		domain = args.domain.split('.')[0]
		tld = args.domain.split('.')[1]

	# Create LDAP Connection
	server = Server(args.target, get_info=ALL)
	conn = Connection(server, user="%s\\%s" % (args.domain, args.username), password="%s" % args.password, authentication="NTLM", auto_bind=True)

	# Search for Exchange Servers
	if sub:
		conn.search('cn=Configuration,dc=%s,dc=%s,dc=%s' % (sub,domain,tld), '(objectCategory=msExchExchangeServer)', attributes = ['adminDisplayName'])

		print(Fore.GREEN+Style.BRIGHT+"[+] Exchange Servers Found:"+Style.RESET_ALL)

		for entry in conn.response:
			try:
				print(Fore.GREEN+Style.BRIGHT+entry['attributes']['adminDisplayName']+".%s.%s.%s" % (sub,domain,tld) +Style.RESET_ALL)
			except Exception as e:
				continue
	else:
		conn.search('cn=Configuration,dc=%s,dc=%s' % (domain, tld), '(objectCategory=msExchExchangeServer)', attributes = ['adminDisplayName'])

		print(Fore.GREEN+Style.BRIGHT+"[+] Exchange Servers Found:"+Style.RESET_ALL)

		for entry in conn.response:
			try:
				print(Fore.GREEN+Style.BRIGHT+entry['attributes']['adminDisplayName']+".%s.%s" % (domain,tld)+Style.RESET_ALL)
			except Exception as e:
				continue

if __name__ == "__main__":
	main()

