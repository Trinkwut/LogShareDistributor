import hmac
import hashlib

HMAC_Password = 'ae6fc580d933300587894716f8'


LogToCopmpare = input('Geben Sie den zu pruefenden Log Eintrag in Anfuerhungszeichen ein: ')
PastMac = input('Geben Sie den vorherigen MAC Wert in Anfuerhungszeichen ein (sollte dies der erste Eintrag im Log sein, bitte den vorher verinebarten Initial MAC eingeben: ')

HMAC = hmac.new(HMAC_Password, '', hashlib.sha256)			
#remove unnecassary charakters
LogToCopmpare.rstrip()
PastMac.rstrip()

MAC = LogToCopmpare + PastMac
HMAC.update(MAC)

print ("Der MAC Wert zu ihrem Log Eintrag lautet wie folgt: ")
print HMAC.hexdigest()

