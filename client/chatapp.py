#!/usr/bin/env python3

''' Read and write IRC channel messages to socketio '''

import asyncio
import os
import datetime

from flask_socketio import socketio

# ASYNCIO Event loop
LOOP = asyncio.get_event_loop()

# SocketIO Client
sio = socketio.AsyncClient(logger=True, engineio_logger=True)

# ----------------------------------------------------- 
# Socketio
# ----------------------------------------------------- 

@sio.on('send_message', namespace='/chat')
def on_send_chat_message(message):
    ''' Callback action for sending a chat message from socketio '''
    print(message)

async def start_sio_server():
    await sio.connect('http://127.0.0.1:5000')

# ----------------------------------------------------- 
def main():

    # Start the SocketIO Client ASYNCIO
    LOOP.run_until_complete(start_sio_server())
    
    # Run the asyncio event loop forever
    LOOP.run_forever()

    # Cleanup
    sio.disconnect()

if __name__ == '__main__':
   main()
