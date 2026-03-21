import time
from tqdm import tqdm

from ingestion.document_loader import DocumentLoader
from ingestion.cleaner import DocumentCleaner
from ingestion.chunker import DocumentChunker
from ingestion.extraction_block_builder import ExtractionBlockBuilder

from extraction.combined_extractor import CombinedExtractor
from extraction.triple_builder import TripleBuilder

from graph.graph_builder import GraphBuilder
from graph.community_detection import CommunityDetector

from vector.embedding_generator import EmbeddingGenerator
from vector.vector_store import VectorStore

from configs.settings import settings


# ---------- INIT ----------

loader = DocumentLoader()
cleaner = DocumentCleaner()
chunker = DocumentChunker()
block_builder = ExtractionBlockBuilder()

extractor = CombinedExtractor()
triple_builder = TripleBuilder()
graph_builder = GraphBuilder()


# ---------- LOAD + CLEAN ----------

docs = loader.load_documents()

for doc in docs:
    doc["text"] = cleaner.clean(doc["text"])


# =========================================================
# VECTOR PIPELINE (SMALL CHUNKS)
# =========================================================

chunks = []

for doc in docs:
    chunks.extend(chunker.chunk(doc))

texts = [c["text"] for c in chunks]

embedder = EmbeddingGenerator(settings.EMBEDDING_MODEL)
embeddings = embedder.generate(texts)

store = VectorStore(len(embeddings[0]))
store.add(embeddings, chunks)
store.save()

print("✅ Vector store ready")


# =========================================================
# GRAPH PIPELINE (LARGE BLOCKS)
# =========================================================

blocks = block_builder.build_blocks(docs)

print(f" Processing {len(blocks)} extraction blocks...")

for block in tqdm(blocks, desc="Graph Extraction"):

    text = block["text"]

    # ---- Retry logic ----
    result = None
    for attempt in range(3):
        try:
            result = extractor.extract(text)
            break
        except Exception as e:
            print(f"[Retry {attempt+1}] Error: {e}")
            time.sleep(5)

    if not result:
        continue

    triples = triple_builder.build(result)

    for t in triples:
        graph_builder.add_triple(
            t["subject"],
            t["relation"],
            t["object"],
            properties=t["properties"],
            source=block["source"],
            chunk_id=block["block_id"]
        )

    # ---- Rate limiting (15 RPM) ----
    time.sleep(4)


# ---------- COMMUNITY DETECTION ----------

detector = CommunityDetector(graph_builder.client)
detector.detect()

print(" Graph construction complete")