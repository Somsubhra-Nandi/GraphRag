from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class EntityResolver:

    def __init__(self):

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.entities = []
        self.embeddings = []

    def normalize(self, name):

        return name.strip().lower()

    def resolve(self, name):

        name = self.normalize(name)

        emb = self.model.encode([name])[0]

        if not self.embeddings:
            self.entities.append(name)
            self.embeddings.append(emb)
            return name

        sims = cosine_similarity([emb], self.embeddings)[0]

        best_idx = np.argmax(sims)

        if sims[best_idx] > 0.85:
            return self.entities[best_idx]

        self.entities.append(name)
        self.embeddings.append(emb)

        return name