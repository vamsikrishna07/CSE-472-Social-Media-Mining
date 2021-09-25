# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 19:09:19 2021

@author: Vamsi
"""

# importing the sync module from Telethon library 
from telethon.sync import TelegramClient

# Instantiating client object using the credentials generated
api_id = 8460666
api_hash = '38320a09aea6b2f008569025df512030'
phone = '+14809559623'
client = TelegramClient(phone, api_id, api_hash)

# Connecting to telegram and check if the user is authorized, Else send an OTP
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code'))

# 
