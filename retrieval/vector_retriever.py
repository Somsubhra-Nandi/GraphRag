import numpy as np
from vector.embedding_generator import EmbeddingGenerator


class VectorRetriever:

    def __init__(self, vector_store, embedding_model):

        self.store = vector_store
        self.embedder = EmbeddingGenerator(embedding_model)

    def retrieve(self, query, k=5):

        emb = self.embedder.generate([query])

        results = self.store.search(np.array(emb), k)

        return results