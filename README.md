# exchange_hunter2
Hunting for Microsoft Exchange the LDAP Way.

This script uses a valid credential, a DC IP and Hostname to log into the DC over LDAP and query the LDAP server for the wherabouts of the Microsoft Exchange servers in the environment.

# Help Menu:
```
./exchange_hunter2.py -h
usage: exchange_hunter2.py [-h] -u USERNAME -p PASSWORD -d DOMAIN -t TARGET

Exchange Hunter via LDAP

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        username
  -p PASSWORD, --password PASSWORD
                        password
  -d DOMAIN, --domain DOMAIN
                        domain.com
  -t TARGET, --target TARGET
                        Target Domain Controller
```
# Example Usage:
```
./exchange_hunter2.py -u testuser1 -p Summer2019 -d tgore.com -t 192.168.204.139
u:TGORE\testuser1
[+] Exchange Servers Found:
EXCHANGE.tgore.com
```
