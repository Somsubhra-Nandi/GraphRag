from ingestion.document_loader import DocumentLoader
from ingestion.cleaner import DocumentCleaner
from ingestion.chunker import DocumentChunker

from extraction.relation_extractor import RelationExtractor
from extraction.triple_builder import TripleBuilder
from graph.graph_builder import GraphBuilder

from vector.embedding_generator import EmbeddingGenerator
from vector.vector_store import VectorStore

from configs.settings import settings
from extraction.entity_extractor import EntityExtractor

loader = DocumentLoader()
cleaner = DocumentCleaner()
chunker = DocumentChunker()

relation_extractor = RelationExtractor()
triple_builder = TripleBuilder()
graph_builder = GraphBuilder()
entity_extractor = EntityExtractor()

docs = loader.load_documents()
chunks = []

for doc in docs:

    doc["text"] = cleaner.clean(doc["text"])

    chunks.extend(chunker.chunk(doc))


# ---------- Embedding pipeline ----------

texts = [c["text"] for c in chunks]

embedder = EmbeddingGenerator(settings.EMBEDDING_MODEL)

embeddings = embedder.generate(texts)

store = VectorStore(len(embeddings[0]))

store.add(embeddings, chunks)

print("Vector store ready")


# ---------- Graph extraction ----------

for chunk in chunks:

    text = chunk["text"]

    entities = entity_extractor.extract(text)

    result = relation_extractor.extract(text, entities)

    triples = triple_builder.build(result)

    for t in triples:

        graph_builder.add_triple(
            t["subject"],
            t["relation"],
            t["object"],
            "Entity",
            "Entity"
        )

print("Graph construction complete")