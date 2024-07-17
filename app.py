from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message'].lower()
    
    try:
        response = requests.post('http://localhost:8001/additive', json={'additive': user_message})
        return response.json()
    except requests.exceptions.ConnectionError:
        return jsonify({'message': "Error: Unable to connect to the data server. Make sure it's running."})

if __name__ == '__main__':
    app.run(port=8000, debug=True)