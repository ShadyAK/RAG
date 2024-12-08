from typing import List, Dict, Any
import os
import logging
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from src.utils.helper import text_to_vector
from src.db.search_pipeline import SearchPipelineBuilder

class MongoDBAtlasConnector:
    """
    A class to handle MongoDB Atlas database access with read and write operations.
    """

    __COLLECTION_NAME = 'RAG_SEARCH'
  
    def __init__(self):
        """
        Initialize the MongoDBAtlasConnector, load environment variables, and test the connection.
        """
        load_dotenv()
        self.mongo_uri = os.getenv('MONGO_URI', 'your_mongodb_connection_string')
        self.client = MongoClient(self.mongo_uri, server_api=ServerApi('1'))
        self.db = self.client[self.__COLLECTION_NAME]
        self._test_connection()

    def _test_connection(self) -> None:
        """
        Test the connection to the MongoDB server.
        """
        try:
            self.client.admin.command('ping')
            logging.info("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            logging.error(e)

    def insert_one(self, collection_name: str, data: Dict[str, Any]) -> str:
        """
        Insert a single document into a collection.

        Args:
            collection_name (str): The name of the collection.
            data (Dict[str, Any]): The data to insert.

        Returns:
            str: The ID of the inserted document.
        """
        collection = self.db[collection_name]
        result = collection.insert_one(data)
        return str(result.inserted_id)

    def find(self, collection_name: str, query: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Find documents in a collection.

        Args:
            collection_name (str): The name of the collection.
            query (Dict[str, Any], optional): The query to filter documents. Defaults to None.

        Returns:
            List[Dict[str, Any]]: The list of found documents.
        """
        collection = self.db[collection_name]
        if query is None:
            query = {}
        return list(collection.find(query))

    def list_collection_names(self) -> List[str]:
        """
        List all collection names in the database.

        Returns:
            List[str]: The list of collection names.
        """
        return self.db.list_collection_names()

    def add_vector(self, collection: str, text_to_add: str) -> str:
        """
        Add a text and its vector embedding to a collection.

        Args:
            collection (str): The name of the collection.
            text_to_add (str): The text to add.

        Returns:
            str: The ID of the inserted document.
        """
        vector = text_to_vector(text_to_add)
        inserted_id = self.insert_one('vector_search', {"text": text_to_add, "vector": vector})
        return inserted_id
 
    def get_similar_text(self, collection_name: str, search_pipeline: SearchPipelineBuilder) -> List[Dict[str, Any]]:
        """
        Get similar text based on the search pipeline.

        Args:
            collection_name (str): The name of the collection.
            search_pipeline (SearchPipelineBuilder): The search pipeline builder.

        Returns:
            List[Dict[str, Any]]: The list of similar texts.
        """
        result = self.db[collection_name].aggregate(search_pipeline.build())
        return list(result)
  
# test the connection below 
if __name__ == "__main__":
    db_connector = MongoDBAtlasConnector()
    print(db_connector.list_collection_names())
