#!/usr/bin/env python

import os
import datetime

from flask import Flask, render_template
from flask_socketio import SocketIO

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
#async_mode = None
async_mode = 'eventlet'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
sio = SocketIO(app, async_mode=async_mode)

# For IRC Messages
CHANNEL = '#test-channel'

# Keep a message counter number
# Store for each channel
MSG_COUNT = dict()
MSG_COUNT[CHANNEL] = dict()

# Store chat log history
# used to populate the chat html page on reload
# Store for each channel
CHAT_LOG = dict()
CHAT_LOG[CHANNEL] = list()

# -----------------------------------------------------------
# Chat Window Callback Buttons / Fields
# ----------------------------------------------------------

class TheChatForm(FlaskForm):
    def __init__(self):
        super().__init__()

    # Send Message Text Input
    chat_message_data = TextAreaField('Message', validators=[InputRequired(), Length(max=500)])

    # Send Message Button
    chat_send = SubmitField('Send')


# ----------------------------------------------------------
# Event Callbacks
# ----------------------------------------------------------


# IRC Chat Callbacks
# ..................
def get_chat_send_message_count(target, nickname):
    ''' Keep track of the send message count for nickname '''

    # Increment the message count
    if nickname not in MSG_COUNT[target].keys():
       MSG_COUNT[target][nickname] = 1;
    else :
       MSG_COUNT[target][nickname] += 1;

    return MSG_COUNT[target][nickname]


def record_chat_send_message(message):
    ''' Record message for chat log history html view
        The message should be a dictionary with keys:
         'data', 'target', 'nickname', 'tstamp'
    '''

    # Record the chat log history
    # Note: use a list, as deque not json compatible
    CHAT_LOG[message['target']].insert(0, dict(message))


@sio.on('send_chat_message', namespace='/chat')
def on_send_chat_message(message):
    ''' Received a send chat message from web client, forward to Python Client '''

    # Cleanup message
    message['message'] = message['message'].strip()

    # relay message to irc bot client
    sio.emit('send_chat_message', message, namespace='/chat')

    # DEBUG Send message to all connected web clients
    tstamp = datetime.datetime.utcnow().strftime("%H:%M:%S")
    msg = {'data': message['message'], 
           'target': message['target'],
           'nickname': message['nickname'],
           'tstamp': tstamp }
    sio.emit('recv_chat_message', msg, namespace='/chat')

    # record the message to the chat log
    record_chat_send_message(msg)


@sio.on('recv_chat_message', namespace='/chat')
def on_recv_chat_message(message):
    ''' Received a message from Python Client, forward to web client '''
    sio.emit('recv_chat_message', message, namespace='/chat')


# ----------------------------------------------------------
# HTML Routes
# ----------------------------------------------------------

@app.route('/')
@app.route('/chat')
def html_chat():
    '''  Chat Page '''
    chat_form = TheChatForm()

    # Configuration Parameters
    nickname = 'TestNick'
    channel = '#test-channel'

    return render_template('chat.html', chat_form=chat_form, channel=channel, nickname=nickname, chat_log=CHAT_LOG[channel])


# ----------------------------------------------------------
# MAIN STARTUP
# ----------------------------------------------------------
if __name__ == '__main__':

    # Run the FLASK-SOCKETIO APP
    sio.run(app, debug=True)
    # For binding on all interfaces
    #sio.run(app, host='0.0.0.0', debug=True)