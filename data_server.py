#server code

import http.server
import socketserver
import json
import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, 'FoodAdditives.csv')

try:
    df = pd.read_csv(csv_path)
    print(f"Successfully loaded {csv_path}")
except FileNotFoundError:
    print(f"Error: {csv_path} not found.")
    print("Please make sure the CSV file is in the same directory as this script.")
    exit(1)

class DataHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        if self.path == '/additive':
            response = self.get_additive_info(data['additive'])
        else:
            response = {'error': 'Invalid endpoint'}

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def get_additive_info(self, additive):
        result = df[df['Food Additive'].str.lower() == additive.lower()]
        
        if not result.empty:
            additive_info = result.iloc[0]
            response = f"Food Additive: {additive_info['Food Additive']}\n"
            response += f"Type: {additive_info['Type']}\n"
            response += f"Pros: {additive_info['Pros']}\n"
            response += f"Cons: {additive_info['Cons']}"
        else:
            response = f"Sorry, I couldn't find information about {additive}. Please try another food additive."
        
        return {'message': response}

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Data server is running")
        else:
            super().do_GET()

if __name__ == "__main__":
    PORT = 8001
    with socketserver.TCPServer(("", PORT), DataHandler) as httpd:
        print(f"Serving data at http://localhost:{PORT}")
        httpd.serve_forever()

 # To Install required packages Open a terminal in your project folder and run
 #  pip install requests beautifulsoup4
 #  Run the server:
 #  python server.py