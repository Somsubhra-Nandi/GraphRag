from graph.graph_client import GraphClient
from retrieval.graph_retriever import GraphRetriever
from retrieval.vector_retriever import VectorRetriever
from retrieval.hybrid_retriever import HybridRetriever
from vector.vector_store import VectorStore
from configs.settings import settings

# 1. Initialize DB Clients
graph_client = GraphClient()
vector_store = VectorStore(384)
vector_store.load() # Loads your FAISS index from disk

# 2. Initialize Retrievers
graph_retriever = GraphRetriever(graph_client)
vector_retriever = VectorRetriever(vector_store, settings.EMBEDDING_MODEL)

# 3. Initialize Hybrid Engine
retriever = HybridRetriever(graph_retriever, vector_retriever)

# 4. Test it!
query = "How did Tesla improve battery technology?"
print(f"Testing Query: {query}\n")

context = retriever.retrieve(query)

print("--- Graph Results ---")
for fact in context["graph"]:
    print(fact)

print("\n--- Document Results ---")
for doc in context["documents"]:
    print(doc["text"]) # Printing just the text for readability