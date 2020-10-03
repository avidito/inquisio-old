import sys
from api import app, socketio

if __name__ == '__main__':
	sys.path.append('.')
	socketio.run(app, port=5000, debug=True)