import os
import shutil
import urllib2
from samba import smb
from smb.SMBHandler import SMBHandler
from time import sleep
import hmac
import hashlib
import socket

if not os.path.exists('/localshare/'):
	os.makedirs('/localshare/')

if os.listdir('/localshare/') != []:
	shutil.rmtree('/localshare/')
	os.makedirs('/localshare/')



####
#MACs

MACHelper = []

#HMAC Password
HMAC_Password = 'ae6fc580d933300587894716f8'

#Unique String to identifiy MACs:
MAC_identifier = '  MACapplied:  '

k = 0
#alter with current pre MAC, if run Programm multiple times
pastMac = 'd8c7fae915f0a5e8ff49ebfe96'

#liste leeren
MACHelper[:] = []


with open('/var/log/auth.log','r') as auth_fh:
	MACHelper = auth_fh.readlines()
	MACHelper.reverse()
	
	for i in MACHelper:
		#MACHelper.append(line) 

		
		#Only append MACs to those Strings where no MAC is already added
		if  not (MAC_identifier in MACHelper[k]):
			#remove (\n) will after text, will be added later
			temp = MACHelper[k]
			temp = temp.rstrip()
			HMAC_prep = hmac.new(HMAC_Password, '', hashlib.sha256)			
			MAC = temp + pastMac
			HMAC_prep.update(MAC)
			pastMac = HMAC_prep.hexdigest()
			#Overwrite the current list Element with the List Element the MAC Identifier and the hexed MAC
			MACHelper[k] =	temp.rstrip() +  MAC_identifier + pastMac + '\n'
		k+=1	

MACHelper.reverse()

#Write modified log file with added MACs, this will overwrite the current file!

ModifieddLogFile=open('/var/log/auth.log', 'w')

for i in MACHelper:
    ModifieddLogFile.write(i)

ModifieddLogFile.close()

#liste leeren
MACHelper[:] = []


#################
#Shares erstellen

hostname = socket.gethostname()

#uses standad values n = 5 and k = 3
sssCommand = "sudo gfsplit " + '/var/log/auth.log /localshare/auth-log-' + hostname
os.system(sssCommand)

#################
#Shares verteilen

#pySMB only works with ip Adresses
# for documentation see: pySMB SMbHandlerClass
ip_list = ['192.168.137.91','192.168.137.93','192.168.137.94','192.168.137.95','192.168.137.92']
#create an Array for all the files to share
filenames = os.listdir('/localshare/')

i = 0

for filenames in filenames:
	file_fh = open('/localshare/'+filenames, 'r')
	director = urllib2.build_opener(SMBHandler)
	#if you have mor shares then available servers to store them, we start from the beginning
	if i > len(filenames):
		i = 0
	url = 'smb://'+ip_list[i]+'/shares/'+filenames
	#print(url)
	#sleep(20.10)
	fh = director.open(url, data = file_fh)
	#sleep(10.10)
	fh.close()
	i+=1

