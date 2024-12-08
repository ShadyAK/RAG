from sentence_transformers import SentenceTransformer

class SingletonSentenceTransformer:
    _instance = None

    @staticmethod
    def get_instance():
        if SingletonSentenceTransformer._instance is None:
            SingletonSentenceTransformer._instance = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        return SingletonSentenceTransformer._instance

def text_to_vector(text):
    model = SingletonSentenceTransformer.get_instance()
    embedding = model.encode(text)
    return embedding[:50].tolist()  # Ensure the vector length is 50


