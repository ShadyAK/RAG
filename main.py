from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from src.utils.helper import text_to_vector
from src.db.atlas_connector import MongoDBAtlasConnector
import logging
from typing import List, Dict, Any
from src.db.search_pipeline import SearchPipelineBuilder  # Import the SearchPipeLineBuilder class

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize the MongoDB connector
db_connector = MongoDBAtlasConnector()


# Add flask endpoints to access the db
@app.route('/add', methods=['POST'])
def add() -> Any:
    data = request.json
    inserted_id = db_connector.insert_one('test', data)
    return jsonify({"inserted_id": str(inserted_id)})

@app.route('/get/<table_name>', methods=['GET'])
def get(table_name: str) -> Any:
    data = db_connector.find(table_name)
    return jsonify(data)

# get all tables inside the db
@app.route('/tables', methods=['GET'])
def get_tables() -> Any:
    tables = db_connector.list_collection_names()
    return jsonify(tables)

@app.route('/add_vector', methods=['POST'])
def add_vector() -> Any:
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({"error": "Text is required"}), 400
    
    vector = text_to_vector(text)
    inserted_id = db_connector.insert_one('vector_search', {"text": text, "vector": vector})
    return jsonify({"inserted_id": str(inserted_id), "text": text, "vector": vector})

@app.route('/get_similar_text', methods=['POST'])
def get_similar_text() -> Any:
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({"error": "Text is required"}), 400
    
    vector = text_to_vector(text)
    all_vectors = db_connector.find('vector_search', {}, {"_id": 0, "text": 1, "vector": 1})
    
    if not all_vectors:
        return jsonify({"error": "No vectors found in the database"}), 404
    
    vectors = [item['vector'] for item in all_vectors]
    similarities = cosine_similarity([vector], vectors)
    most_similar_index = similarities.argmax()
    most_similar_text = all_vectors[most_similar_index]['text']
    
    return jsonify({"text": most_similar_text, "similarity": similarities[0][most_similar_index]})

if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    # app.run(debug=True)
    pipeline_builder = SearchPipelineBuilder()
    pipeline_builder.set_index('vector_index') \
                    .set_limit(10) \
                    .set_num_candidates(200) \
                    .set_path('vector') \
                    .set_project({'text': 1}) \
                    .set_query('what the sigma?')
    
    db_connector.get_similar_text('vector_search', pipeline_builder)
