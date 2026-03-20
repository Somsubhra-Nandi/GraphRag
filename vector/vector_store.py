import faiss
import numpy as np
import pickle
import os

class VectorStore:
    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)
        self.texts = []
        
        # ---> The dedicated storage directory <---
        self.storage_dir = os.path.join("data", "vector_store")
        os.makedirs(self.storage_dir, exist_ok=True)

    def add(self, embeddings, chunks):
        self.index.add(np.array(embeddings).astype('float32'))
        self.texts.extend(chunks)

    def search(self, query_embedding, k=5):
        # Added a safety check in case the index is empty
        if self.index.ntotal == 0:
            return []
            
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), k)
        return [self.texts[i] for i in indices[0]]

    def save(self, index_name="vector.index", chunks_name="vector_chunks.pkl"):
        # Route the files directly into the dedicated folder
        index_path = os.path.join(self.storage_dir, index_name)
        texts_path = os.path.join(self.storage_dir, chunks_name)
        
        faiss.write_index(self.index, index_path)
        with open(texts_path, "wb") as f:
            pickle.dump(self.texts, f)

    def load(self, index_name="vector.index", chunks_name="vector_chunks.pkl"):
        # Load the files directly from the dedicated folder
        index_path = os.path.join(self.storage_dir, index_name)
        texts_path = os.path.join(self.storage_dir, chunks_name)
        
        if os.path.exists(index_path) and os.path.exists(texts_path):
            self.index = faiss.read_index(index_path)
            with open(texts_path, "rb") as f:
                self.texts = pickle.load(f)
        else:
            print(f"Warning: No vector files found in {self.storage_dir}")