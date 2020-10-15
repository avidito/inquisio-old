from api import app, socketio
import sys
sys.path.append(".")

if __name__ == '__main__':	
	socketio.run(app, port=5000, debug=True)