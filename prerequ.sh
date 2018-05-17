#!/bin/bash
#Variablen

#einfach Auskommentieren was man nicht braucht

#Installationsquellen Updaten
sudo apt-get update -y
sudo apt-get upgrade -y

#python pip installer
sudo apt-get install python -y
sudo apt-get install python-pip -y

#python Bibliothken installieren
sudo yes | pip install pysmb
sudo yes | pip install hashlib


#edit /etc/samab/smb.conf
sudo apt-get install samba -y
sudo mkdir -p /shares
sudo chmod 777 /shares
#hier die Config in /etc/samab/smb.conf bearbeiten
sudo echo "[shares]" >> /etc/samba/smb.conf
sudo echo "comment = Shares for Log Files" >> /etc/samba/smb.conf
sudo echo "path = /shares" >> /etc/samba/smb.conf
sudo echo "browesable = yes" >> /etc/samba/smb.conf
sudo echo "read only = no" >> /etc/samba/smb.conf
sudo echo "guest ok = yes" >> /etc/samba/smb.conf
sudo echo "test" >> /etc/samba/smbconf

sudo service smbd restart

#sss Programm:
sudo apt-get install libgfshare-bin -y




