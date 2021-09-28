# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 19:09:19 2021

@author: Vamsi
"""

# importing the sync module from Telethon library 
from telethon import TelegramClient
from telethon.tl.types import PeerChannel
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.errors import SessionPasswordNeededError
from datetime import datetime
import json
import asyncio 
import nest_asyncio
nest_asyncio.apply()
import configparser
    
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o,datetime): return o.isoformat()
        if isinstance(o,bytes): return list(o)
        return json.JSONEncoder.default(self,o)
    
# Instantiating client object using the credentials generated
api_id = 8460666
api_hash = '38320a09aea6b2f008569025df512030'
phone = '+14809559623'
client = TelegramClient(phone, api_id, api_hash)
client.connect()


async def main(phone):
    async with TelegramClient(phone, api_id, api_hash) as client:
        await client.start()
        if await client.is_user_authorized() == False:
            await client.send_code_request(phone)
            try:
                await client.sign_in(phone, input('Enter the code: '))
            except: 
                await client.sign_in(password = input('Enter password: '))
        
        user = await client.get_me()
        
        user_input_channel = "OANNTV"
        if user_input_channel.isdigit(): 
            entity = PeerChannel(int(user_input_channel))
    
        my_channel = await client.get_entity(user_input_channel)
        
        offset_id, limit, all_messages, total_messages, total_count_limit = 0, 2000, [], 0, 1000000
        while True:
            history = await client(GetHistoryRequest(peer = my_channel, offset_id = offset_id, offset_date = None, add_offset = 0, limit = limit, max_id = 0, min_id = 0, hash = 0))
            if not history.messages: break
            for message in history.messages:
                all_messages.append(message.to_dict())
            offset_id = history.messages[-1].id
            total_messages = len(all_messages)
            if total_count_limit !=0 and total_messages >= total_count_limit: 
                break 
            
        with open('messages.json','w') as outfile:
            json.dump(all_messages, outfile, cls = DateTimeEncoder)
        
asyncio.run(main(phone))