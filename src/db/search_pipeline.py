from typing import List, Dict, Any
from src.utils.helper import text_to_vector

# Example pipeline to search for similar text
'''pipeline = [
  {
    '$vectorSearch': {
      'index': 'vector_index', 
      'path': 'vector', 
      'queryVector': text_to_vector('What the sigma???'), 
      'numCandidates': 200, 
      'limit': 10
    } 
  }, {
    '$project': {
      '_id': 0, 
      'text': 1,
      'vector': 0,
      'score': {
        '$meta': 'vectorSearchScore'
      }
    }
  }
]'''

class SearchPipelineBuilder:
    """
    A builder class for constructing MongoDB aggregation pipelines for vector search.
    """

    __VECTOR_SEARCH = '$vectorSearch'
    __PROJECT = '$project'
    __search_pipeline = [{__VECTOR_SEARCH: {}}, {__PROJECT: {}}]
    
    def set_index(self, index: str) -> 'SearchPipelineBuilder':
        """
        Set the index for the vector search stage.

        Args:
            index (str): The name of the index.

        Returns:
            SearchPipelineBuilder: The builder instance.
        """
        self.__search_pipeline[0][self.__VECTOR_SEARCH]['index'] = index
        return self

    def set_path(self, path: str) -> 'SearchPipelineBuilder':
        """
        Set the path for the vector search stage.

        Args:
            path (str): The path to the vector field.

        Returns:
            SearchPipelineBuilder: The builder instance.
        """
        self.__search_pipeline[0][self.__VECTOR_SEARCH]['path'] = path
        return self

    def set_query(self, query: str) -> 'SearchPipelineBuilder':
        """
        Set the query vector for the vector search stage.

        Args:
            query (str): The query text to be converted to a vector.

        Returns:
            SearchPipelineBuilder: The builder instance.
        """
        self.__search_pipeline[0][self.__VECTOR_SEARCH]['queryVector'] = text_to_vector(query)
        return self

    def set_num_candidates(self, num_candidates: int) -> 'SearchPipelineBuilder':
        """
        Set the number of candidates for the vector search stage.

        Args:
            num_candidates (int): The number of candidates to consider.

        Returns:
            SearchPipelineBuilder: The builder instance.
        """
        self.__search_pipeline[0][self.__VECTOR_SEARCH]['numCandidates'] = num_candidates
        return self

    def set_limit(self, limit: int) -> 'SearchPipelineBuilder':
        """
        Set the limit for the vector search stage.

        Args:
            limit (int): The maximum number of results to return.

        Returns:
            SearchPipelineBuilder: The builder instance.
        """
        self.__search_pipeline[0][self.__VECTOR_SEARCH]['limit'] = limit
        return self

    def set_project(self, fields_to_get: Dict[str, Any]) -> 'SearchPipelineBuilder':
        """
        Set the fields to project in the results.

        Args:
            fields_to_get (Dict[str, Any]): The fields to include or exclude in the results.

        Returns:
            SearchPipelineBuilder: The builder instance.
        """
        for key, value in fields_to_get.items():
            self.__search_pipeline[1][self.__PROJECT][key] = value
        return self

    def build(self) -> List[Dict[str, Any]]:
        """
        Build the search pipeline.

        Returns:
            List[Dict[str, Any]]: The constructed search pipeline.
        """
        return self.__search_pipeline


