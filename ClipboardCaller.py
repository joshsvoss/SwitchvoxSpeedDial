

########################################
#  Z-Firm LLC Utility
#  (c) 2014 Z-Firm LLC
########################################

"""
Author: Joshua Voss, Date: 7/7/2014

This script will create a phone call from the extension
hardcoded below, to a phone number on your clipboard.  The
script takes care of getting rid of "()-+ " characters from the number.
Make sure to have a phone number on the clipboard before running.
Runs on versions 2.X and 3.X

DEPENDENCIES: You must pip install 'pyperclip', and 'requests' and 'configparser' to use this script!
Additionally, this script must have accesss to the "pyswitchvoxapi" module in order to make the api
call.  It's probably best to keep this script in the same folder as pyswitchvoxapi so it is
automatically added to the path.

CONFIG

SETUP DIRECTIONS: 
1) create a shortcut to this script on your desktop or wherever you please,
right click on the shortcut, click properties, and under "Shortcut Keys:" type
in your desired keyboard shortcut.  Keying this keyboard shortcut will now
run the script in your default version of Python.

2) Under the 'target' field of the properties of the shortcut, append the filepath of
your config file.  The config file should follow the design of "SpeedDialConfig.ini" in the
perforce workspace at: C:\develop\main\z-firm production\Misc\SwitchVox\pyswitchvoxapi\SpeedDialConfig.ini
In your own copy of the config file, change the "extension" field to
your own extension number.  For the account_id field, see below:


TO GET ACCOUNT_ID: You shouldn't need to change the account id, it seems that it
doesn't have an effect on the call logs OR on your user rules of the dial_first extension,
but if you'd like to get your account_id run 'GetAccountID.py' and input your extension
when prompted.  Change the account_id field to that number.  

"""
import sys
#print 'Python ver: ' + str(sys.version_info[0:3])
#import platform
#print platform.architecture()

import pyperclip
from pyswitchvoxapi import switchvox_api
try:
    import configparser as cp
except:
    import ConfigParser as cp

#Make sure that a command line argument filepath was provided for the config file
if len(sys.argv) < 2:
    print("ERROR: please provide config filepath as command line argument.")
    sys.exit(1)

#Read location of config file from command line argument:
configFilepath = sys.argv[1]
#print(configFilepath)


# Access and parse ConfigFile.ini
parser = cp.ConfigParser()
parser.read(configFilepath)
address = parser.get("Credentials", "ipaddress")
username = parser.get("Credentials", "username")
password = parser.get("Credentials", "password")
extension = parser.get("User", "extension")
account_id = parser.get("User", "account_id")

#Establish connection
#'local' account has limited privileges, can only use the api to create calls
switchvox = switchvox_api(
    address, username, password,
    verifycert=False, autoitemspp=200
)



#copy from clipboard
clipboardNumber = pyperclip.paste()

#output error if clipboard is empty
if clipboardNumber == None:
    print("Error: clipboard empty")
    sys.exit(1)

#Check the version of Python Interpreter being used, and based on that
#Use the correct syntax to convert the byte object to string.
#If not version 2 or 3, throw an error.
if   sys.version_info[0] == 2:
    clipboardNumber = str(clipboardNumber)
elif sys.version_info[0] == 3:
    clipboardNumber = str(clipboardNumber, 'utf-8')
else:
    print("ERROR: You must be running Python 2.X or 3.X.")
    sys.exit(1)


#make sure number is formatted correctly:
#NOTE: if running in Python 2.7, remove 'utf-8' argument.
#If 3.X, add 'utf-8' as second argument    
 #might need to change encoding based on machine 
clipboardNumber = clipboardNumber.strip()

if not clipboardNumber.isdigit(): #Get rid of all non-numbers:
    clipboardNumber = clipboardNumber.replace('-', '')
    clipboardNumber = clipboardNumber.replace('/', '')
    clipboardNumber = clipboardNumber.replace('+', '')
    clipboardNumber = clipboardNumber.replace(' ', '')
    clipboardNumber = clipboardNumber.replace('(', '')
    clipboardNumber = clipboardNumber.replace(')', '')
    clipboardNumber = clipboardNumber.replace('.', '')
if len(clipboardNumber) == 10:
    clipboardNumber = '1'+clipboardNumber


#If at this point the number still isn't numeric, exit
if not clipboardNumber.isdigit():
    print("ERROR: Clipboard doesn't contain valid phone number: " + clipboardNumber)
    sys.exit(1)


#Make sure the length of the number is valid for a phone number:
numLength = len(clipboardNumber)
if numLength <  3 or (numLength > 3 and numLength < 7) or numLength > 11:
    print("ERROR: Incorrect number of digits: " + clipboardNumber)
    sys.exit(2)



#Calls the api method.  Dials "dial_first" first then calls "dial_second"
switchvox.call_method("switchvox.call", dial_first=extension,
                      dial_second=clipboardNumber, dial_as_account_id = account_id,
                      auto_answer=1
                      )
