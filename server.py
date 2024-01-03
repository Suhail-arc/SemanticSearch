from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from urllib.parse import parse_qs
import pymongo
import requests
import logging


# ... Your existing server setup code ...

class RequestHandler(BaseHTTPRequestHandler):
	
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('templates/index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path.startswith('/search'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Here, you would handle the POST request for the search functionality

            with open('templates/results.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')
            
connection_string = "mongodb+srv://kaicorpwatch:iFgY5yvBDS7AJ7yJ@serverlessinstance0.81nzwlp.mongodb.net/?retryWrites=true&w=majority"
password = "iFgY5yvBDS7AJ7yJ"

def do_POST(self):
        # This part would handle the POST request when the user submits the form
        
		# Code for generating embeddings and performing search
        
        client = pymongo.MongoClient(connection_string.format(password))
        db = client.GenerativeAIBuild  # Replace 'your_database_name' with your database name
        collection = db.your_collection_name  # Replace 'your_collection_name' with your collection name
        
def render_template(self, template_name, context=None):
        templates_dir = 'templates'  # Directory where your templates are stored
        env = Environment(
            loader=FileSystemLoader(os.path.abspath(templates_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template(template_name)
        return template.render(context or {})

        hf_token = "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"
        embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

def generate_embedding(text: str) -> list[float]:
            # Code to generate embeddings...

         def perform_search(query_embedding, threshold=0.6):
            # Code to perform search...

          if self.path == '/search':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)

            user_query = params['user_query'][0] if 'user_query' in params else ''
            query_embedding = generate_embedding(user_query)
            query_results = perform_search(query_embedding)

            if query_results:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Customize this part to generate the response based on the query results
                # Read the 'results.html' file and send it back to the user
                with open('templates/results.html', 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Send 'no_results.html' if no results are found
                with open('templates/no_results.html', 'rb') as file:
                    self.wfile.write(file.read())
                    

def log_message(self, format, *args):
        # This method is called for every HTTP request
        print("%s - - [%s] %s" %
              (self.client_address[0], self.log_date_time_string(), format % args))

# Change the port number here
PORT = 8080  # For example, change 8000 to 8080 or any other available port

# The run method starts the server
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {PORT}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()


hf_token = "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"
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

def generate_embedding(text: str) -> list[float]:
    response = requests.post(
        embedding_url,
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": text}
    )

    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")

    return response.json()

def perform_search(query_embedding, threshold=0.6):
    results = []

    query_results = collection.aggregate([
        {"$vectorSearch": {
            "queryVector": query_embedding,
            "path": "plot_embedding_hf",
            "numCandidates": 100,
            "limit": 4,
            "index": "PlotSemanticSearch"
        }}
    ])

    for document in query_results:
        results.append({
            "title": document["title"],
            "plot": document["plot"]
        })

    return results

# Modify do_POST method to perform search
def do_POST(self):
    try:
            if self.path == '/search':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                params = parse_qs(post_data)

                user_query = params['user_query'][0] if 'user_query' in params else ''

                if user_query:
                    query_embedding = generate_embedding(user_query)
                    query_results = perform_search(query_embedding)

                    if query_results:
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()

                        with open('templates/results.html', 'rb') as file:
                            self.wfile.write(file.read())
                    else:
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()

                        with open('templates/no_results.html', 'rb') as file:
                            self.wfile.write(file.read())
                else:
                    self.send_response(400)  # Bad Request status code
                    self.end_headers()
                    self.wfile.write(b'Missing or empty user_query parameter')

            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'404 Not Found')

    except KeyError as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(f"KeyError: {e}".encode('utf-8'))

    except ValueError as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"ValueError: {e}".encode('utf-8'))

    except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Unexpected error: {e}".encode('utf-8'))

                
                
		
