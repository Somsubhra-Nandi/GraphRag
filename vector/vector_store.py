import faiss
import numpy as np
import pickle


class VectorStore:

    def __init__(self, dimension):

        self.index = faiss.IndexFlatL2(dimension)
        self.texts = []

    def add(self, embeddings, chunks):

        self.index.add(np.array(embeddings))
        self.texts.extend(chunks)

    def search(self, query_embedding, k=5):

        distances, indices = self.index.search(query_embedding, k)
        return [self.texts[i] for i in indices[0]]

    def save(self, path="vector.index"):

        faiss.write_index(self.index, path)

        with open("vector_chunks.pkl", "wb") as f:
            pickle.dump(self.texts, f)

    def load(self, path="vector.index"):

        self.index = faiss.read_index(path)

        with open("vector_chunks.pkl", "rb") as f:
            self.texts = pickle.load(f)