from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = '54a54e15c2c5f036bc0a574d02684db7'
socketio = SocketIO(app, logger=True)

from . import routes