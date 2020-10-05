# Modul Flask
from flask import Flask
from flask_socketio import SocketIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a119efed50647b71e3f02ae52408e996'
app.config['JSON_SORT_KEYS'] = False
socketio = SocketIO(app, logger=True)


# Modul Projek
from . import routes