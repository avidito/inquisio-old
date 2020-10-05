# Modul Sistem
import sys
sys.path.append('.')

# Modul Projek
from api import app, socketio


if __name__ == '__main__':
	socketio.run(app, port=5050, debug=True)