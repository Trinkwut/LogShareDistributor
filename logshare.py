#! /usr/bin/env python
import os
import shutil
import urllib2
from samba import smb
from smb.SMBHandler import SMBHandler
from time import sleep
import hmac
import hashlib

if not os.path.exists('/localshare/'):
	os.makedirs('/localshare/')

if os.listdir('/localshare/') != []:
	shutil.rmtree('/localshare/')
	os.makedirs('/localshare/')




#MACs

auth_fh_withoutMAC = []

#HMAC_prep = hmac.new('12345678', '', hashlib.sha256)



k = 0
pastMac = '0'
MAC = 'help'

with open('/home/fabian/Desktop/test.txt','r') as auth_fh:
	for line in auth_fh:
		MAC_identifier = line
		auth_fh_withoutMAC.append(line)
		if not('MAC Wert:'in MAC_identifier):
			HMAC_prep = hmac.new('12345678', '', hashlib.sha256)			
			MAC = auth_fh_withoutMAC[k]
			print MAC.rstrip()
			#auth_fh_withoutMAC[k] = auth_fh_withoutMAC[k] + 'Mac vorheriger Eintrag: ' + pastMac
			HMAC_prep.update(MAC.rstrip().encode('utf-8'))
			print HMAC_prep.hexdigest()
			#pastMac = HMAC_prep.hexdigest()
			#print pastMac
			auth_fh_withoutMAC[k] = auth_fh_withoutMAC[k] +  ' MAC Wert: ' + HMAC_prep.hexdigest()
		k+=1	

file=open('/home/fabian/Desktop/test.txt', 'w')

for i in auth_fh_withoutMAC:
    file.write(i + '\n')

file.close()


#liste leeren
auth_fh_withoutMAC[:] = []

#Shares erstellen

os.system("sudo gfsplit '/var/log/auth.log' '/localshare/ubuntu2'")


#Shares verteilen
ip_list = ['192.168.137.91','192.168.137.93','192.168.137.94','192.168.137.95','192.168.137.91']
filenames = os.listdir('/localshare/')

i = 0

for filenames in filenames:
	file_fh = open('/localshare/'+filenames, 'r')
	director = urllib2.build_opener(SMBHandler)
	url = 'smb://'+ip_list[i]+'/shares/'+filenames
	#print(url)
	#sleep(20.10)
	fh = director.open(url, data = file_fh)
	#sleep(10.10)
	fh.close()
	i+=1

