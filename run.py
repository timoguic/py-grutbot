import sys


if __name__ == "__main__":
    if len(sys.argv) > 1:
        opt = sys.argv[1]
        if opt == 'socket':
            from flask_socketio import SocketIO
            from grutpy import socket
            from grutpy.socket import socketio
        elif opt == 'txt':
            from grutpy.text import app
            app.run()
        else:
            print("Sorry, not sorry.")

    else:
        from grutpy.web import app
        app.run(debug=True)