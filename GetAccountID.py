""" Enter your extension number when prompted and the script prints out
your account_id number.

Author: Joshua Voss
Date: 7/7/2014
"""

from pyswitchvoxapi import switchvox_api
import json

#Establish connection
#'api_admin' account has limited privileges, can only use the api to create calls
switchvox = switchvox_api(
    '<IP ADRESS HERE>', '<USERNAME HERE>', '<PASSWORD HERE>',
    verifycert=False, autoitemspp=200
)

#Get extension number from user
extension = input("What is your extension? >>> ")



extensionInfo = switchvox.call_method(
"switchvox.extensions.getInfo",
extensions=[extension]
)


id = extensionInfo[u'response'][u'result'][u'extensions'][u'extension'][u'account_id']
print("You're account_id is: " + id)


