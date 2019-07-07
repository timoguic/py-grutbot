from flask_socketio import SocketIO
from . import app
from .utils import Parser
from .utils import Search

socketio = SocketIO(app)

@socketio.on('query')
def handle_my_custom_event(query):
	parsed = Parser(query)
	result = Search(parsed)

	print(parsed, result)
	socketio.emit('more_data', {'data': 'maxiLOL'})