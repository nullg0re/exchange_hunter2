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

	# 0xZDH Magic Right here...
	dcstring = ','.join(['dc=%s' % i for i in args.domain.split('.')])

	server = Server(args.target, get_info=ALL)
	conn = Connection(server, user="%s\\%s" % (args.domain, args.username), password="%s" % args.password, authentication="NTLM", auto_bind=True)


	conn.search('cn=Configuration,%s' % dcstring,'(objectCategory=msExchExchangeServer)', attributes = ['adminDisplayName'])

	print(Fore.GREEN+Style.BRIGHT+"[+] Exchange Servers Found:"+Style.RESET_ALL)

	for entry in conn.response:
		try:
			print(Fore.GREEN+"%s.%s" % (entry['attributes']['adminDisplayName'],args.domain) + Style.RESET_ALL)
		except Exception as e:
			continue

if __name__ == "__main__":
	main()
