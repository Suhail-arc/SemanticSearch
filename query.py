import pymongo
import requests

# MongoDB connection string
connection_string = "mongodb+srv://kaicorpwatch:iFgY5yvBDS7AJ7yJ@serverlessinstance0.81nzwlp.mongodb.net/?retryWrites=true&w=majority"
password = "iFgY5yvBDS7AJ7yJ"

# MongoDB client
client = pymongo.MongoClient(connection_string.format(password))
db = client.GenerativeAIBuild  # Replace 'your_database_name' with your database name
collection = db.your_collection_name  # Replace 'your_collection_name' with your collection name

hf_token = "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"
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

def generate_embedding(text: str) -> list[float]:

  response = requests.post(
    embedding_url,
    headers={"Authorization": f"Bearer {hf_token}"},
    json={"inputs": text})

  if response.status_code != 200:
    raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")

  return response.json()

for doc in collection.find({'plot':{"$exists": True}}).limit(50):
 doc['plot_embedding_hf'] = generate_embedding(doc['plot'])
 collection.replace_one({'_id': doc['_id']}, doc)

query = "technical documentation"

results = collection.aggregate([
  {"$vectorSearch": {
    "queryVector": generate_embedding(query),
    "path": "plot_embedding_hf",
    "numCandidates": 100,
    "limit": 4,
    "index": "PlotSemanticSearch",
      }}
]);

for document in results:
    print(f'title: {document["title"]},\nPlot: {document["plot"]}\n')