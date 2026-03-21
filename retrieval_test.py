from graph.graph_client import GraphClient
from retrieval.graph_retriever import GraphRetriever
from retrieval.vector_retriever import VectorRetriever
from retrieval.hybrid_retriever import HybridRetriever
from vector.vector_store import VectorStore
from configs.settings import settings
from planner.query_planner import QueryPlanner
from retrieval.reranker import Reranker
from reasoning.context_builder import ContextBuilder
from reasoning.answer_generator import AnswerGenerator

# Initialize the query planner
planner = QueryPlanner()
reranker = Reranker()
context_builder = ContextBuilder()
answer_generator = AnswerGenerator()

# 1. Initialize DB Clients
graph_client = GraphClient()
vector_store = VectorStore(384)
vector_store.load() # Loads your FAISS index from disk

# 2. Initialize Retrievers
graph_retriever = GraphRetriever(graph_client)
vector_retriever = VectorRetriever(vector_store, settings.EMBEDDING_MODEL)

# 3. Initialize Hybrid Engine
retriever = HybridRetriever(graph_retriever, vector_retriever,planner,reranker)

# 4. Test it!
query = "Which company did Dario Amodei found, and who invested in it?"
print(f"Testing Query: {query}\n")

context = retriever.retrieve(query)

print("--- Graph Results ---")
for fact in context["graph"]:
    print(fact)

print("\n--- Document Results ---")
for doc in context["documents"]:
    print(doc["text"]) # Printing just the text for readability
    
print("\n=====================================")
print("🧠 INITIATING REASONING ENGINE")
print("=====================================\n")

# Step B: Build Context String (Phase 10)
formatted_context = context_builder.build(query, context["graph"], context["documents"])

print("Data Sent to LLM s gvn below:-\n")
print(formatted_context)
print("\n------------------------\n")

# Step C: Generate Answer (Phase 11)
print("🤖 Generating Answer...\n")
final_answer = answer_generator.generate(formatted_context)

print(f"🎯 FINAL ANSWER:\n{final_answer}")