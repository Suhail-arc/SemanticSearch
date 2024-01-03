import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    
from flask import Flask, render_template, request
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
import pymongo
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__, template_folder='/Users/suhailahmed/SemanticSearch/env/templates')

# MongoDB connection string
connection_string = "mongodb+srv://kaicorpwatch:iFgY5yvBDS7AJ7yJ@serverlessinstance0.81nzwlp.mongodb.net/?retryWrites=true&w=majority"
password = "iFgY5yvBDS7AJ7yJ"

# Hugging Face model details
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

# Load the Sentence Transformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Load JSON data
json_file = '/Users/suhailahmed/SemanticSearch/GenerativeAIJSON.json'
with open(json_file) as file:
    data = json.load(file)

# Process JSON data and add plot_embeddings
for item in data:
    plot = item.get('Plot')
    if plot:
        plot_embedding = model.encode(plot)
        item['plot_embeddings'] = plot_embedding.tolist()

# MongoDB client
client = pymongo.MongoClient(connection_string.format(password))
db = client.GenerativeAIBuild  # Replace 'your_database_name' with your database name
collection = db.your_collection_name  # Replace 'your_collection_name' with your collection name

# Function to perform search based on query
def perform_search(query_embedding, collection, threshold=0.4):
    try:
        results = {}
        documents = collection.find({'plot_embeddings': {'$exists': True}})
        for doc in documents:
            Genre = doc.get('Genre')  # Retrieve 'Genre' field as string
            if isinstance(Genre, str):  # Check if 'Genre' is a string
                plot_embedding = np.array(doc.get('plot_embeddings', []))
                similarity_score = cosine_similarity([query_embedding], [plot_embedding])[0][0]
            
                if similarity_score > threshold:
                    Genre = doc['Genre']
                    if Genre not in results:
                        results[Genre] = {
                            'Plot': doc.get('Plot', ''),
                            'Similarity Score': similarity_score
                        }
        return results
    except Exception as e:
        print(f"Error in perform_search: {e}")
        return {}


# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_query = request.form['user_query']
    query_embedding = model.encode(user_query)
    query_results = perform_search(query_embedding, collection, threshold=0.4)

    if query_results:
        combined_data = {
        'query': user_query,
        'results': query_results
        }
        return render_template('results.html', data=combined_data)
    else:
        return render_template('no_results.html')

if __name__ == '__main__':
    app.run(debug=True)
