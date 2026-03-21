#  GraphRAG Knowledge Engine: Agentic, Multi-Hop Retrieval System

##  Overview

Most modern AI applications rely on standard **Vector RAG (Retrieval-Augmented Generation)**. While fast, standard RAG suffers from the **"Disconnected Multi-Hop" problem**: it fails completely when answering complex questions that require connecting disparate pieces of information across thousands of documents.

To solve this, I architected a custom, deterministic **GraphRAG Knowledge Engine** from scratch.

Instead of relying on bloated, black-box frameworks, this system utilizes a custom orchestration layer that combines **Agentic Query Planning**, **Semantic Vector Search**, **Deterministic Graph Traversal**, and **Cross-Encoder Reranking**. It thinks before it searches, ruthlessly filters noise, and provides zero-hallucination, multi-hop reasoning.

---

##  System Architecture

The pipeline is split into two distinct workflows: **Asynchronous Ingestion** and **Agentic Retrieval**.

### 1. The Dual-Ingestion Pipeline

Text is processed through two isolated streams to optimize for both compute cost and API rate limits:

- **Vector Stream (Micro-Chunks):** Documents are sliced into strict 400-character chunks and embedded locally using `all-MiniLM-L6-v2`. Stored in **FAISS** for lightning-fast semantic similarity searches.

- **Graph Stream (Macro-Blocks):** Documents are combined into massive 4,000-character blocks. An LLM performs batch extraction of entities and relationships (dynamically typing nodes and extracting properties like dates and amounts). Triples are stored deterministically in **Neo4j**.

### 2. The Agentic Retrieval Pipeline (The "Brain")

When a user asks a question, the system executes a **5-phase cognitive loop**:

```
Query
  │
  ▼
[Phase a]   Query Planner (LLM)   ──  Evaluates intent. Routes to Graph, Vector, or Hybrid strategy.
  │
  ▼
[Phase b]   Hybrid Retriever       ──  Executes Cypher 2-hop traversals AND/OR FAISS semantic search.
  │
  ▼
[Phase c]   The Judge (Reranker)  ──  Uses a Cross-Encoder to score all text/edges against the query.
  │
  ▼
[Phase d]  Context Builder        ──  Formats surviving data into strict [FACTS] and [EVIDENCE] blocks.
  │
  ▼
[Phase e]  Reasoning Engine       ──  Synthesizes the structured context into a final, factual answer.
```

---

##  Key Engineering Decisions

### 1. Batching LLM Extractions (Rate Limit Optimization)

Extracting graph triples via LLM APIs is notoriously expensive and prone to rate-limiting (HTTP 429). By building an `ExtractionBlockBuilder`, the system concatenates micro-chunks into macro-blocks. This **reduced API requests by over 90%** during ingestion, allowing for the processing of dense documents without hitting quota walls or requiring expensive token rotation hacks.

### 2. Bi-Encoders for Retrieval, Cross-Encoders for Reranking

Retrieving documents using cosine similarity (Bi-Encoders) is fast but dumb — it misses deep contextual relevance. This system implements a **Two-Stage Retrieval** architecture. FAISS pulls the top 20 possible matches, but a `ms-marco-MiniLM-L-6-v2` Cross-Encoder reranks them by feeding the Query and Document through the transformer together, scoring true relevance before passing the context to the final LLM.

### 3. Agentic Query Routing

Not all queries require a graph search. Instead of blindly firing at both databases and mashing results together, the `QueryPlanner` acts as an intelligent traffic cop:

- **Conceptual questions** (e.g., *"How do EV batteries work?"*) → routed to the **Vector DB**
- **Relational questions** (e.g., *"Who invested in Anthropic?"*) → executes a precise **Neo4j Cypher traversal**

This saves compute and reduces LLM context noise.

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| **Core Language** | Python |
| **Graph Database** | Neo4j |
| **Vector Database** | FAISS |
| **Embeddings** | `sentence-transformers` — `all-MiniLM-L6-v2` |
| **Reranker** | `sentence-transformers` — `ms-marco-MiniLM-L-6-v2` |
| **LLM** | `gpt-4o-mini` via GitHub Models / Azure Inference API |
| **Algorithms** | Louvain & Leiden (Community Detection / GDS) |

---

## ⚡ Quick Start

### Prerequisites

- Python 3.10+
- Neo4j Desktop or Docker container running locally (`bolt://localhost:7687`)
- GitHub Personal Access Token (for Azure Models endpoint)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/graph-rag-system.git
   cd graph-rag-system
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file in the root directory:**
   ```env
   OPENAI_API_KEY=your_github_pat_here
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_password
   ```

### Running the Engine

1. Drop your `.txt` files into `data/documents/`.

2. Run the dual-ingestion pipeline to build the Graph and Vector indices:
   ```bash
   python pipeline.py
   ```

3. Interrogate the knowledge base:
   ```bash
   python retrieval_test.py
   ```

---

## 🔮 Future Roadmap (V1)

- **Multi-Step ReAct Agent:** Upgrading the Query Planner into a looping execution agent that can dynamically explore the graph based on intermediate findings (e.g., *"Hop 1 found X, now I must search for Y"*).

- **Asynchronous Processing:** Implementing `asyncio` in the ingestion pipeline for parallel extraction block processing.

- **FastAPI Integration:** Wrapping the backend in a REST API for seamless frontend chat UI integration.