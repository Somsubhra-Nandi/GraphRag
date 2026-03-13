from sentence_transformers import SentenceTransformer
print("ok")

class EmbeddingGenerator:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)
    def generate(self, texts):
        embeddings = self.model.encode(texts)
        return embeddings