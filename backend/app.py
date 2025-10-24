from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Configure CORS
CORS(app, origins=os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(','))

# Configure SocketIO
socketio = SocketIO(app, cors_allowed_origins=os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(','))

@app.route('/health')
def health():
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    socketio.run(app, debug=True, host='0.0.0.0', port=port)
