from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        # 🔥 Switch to a model specifically trained to score Query-Document relevance
        self.model = CrossEncoder(model_name)

    def rerank(self, query, graph_results, doc_results, top_k=5):
        items = []
        pairs = []

        # ---- Prepare graph results ----
        for g in graph_results:
            text = f"{g['subject']} {g['relation']} {g['object']}"
            pairs.append([query, text])
            items.append({"type": "graph", "data": g})

        # ---- Prepare document results ----
        for d in doc_results:
            text = d["text"]
            pairs.append([query, text])
            items.append({"type": "document", "data": d})

        if not pairs:
            return {"graph": [], "documents": [], "scored": []}

        # ---- Score all pairs at once using the Cross-Encoder ----
        scores = self.model.predict(pairs)

        # ---- Attach scores and sort ----
        for i, score in enumerate(scores):
            items[i]["score"] = float(score)

        items.sort(key=lambda x: x["score"], reverse=True)
        top_items = items[:top_k]

        # ---- Split back ----
        final_graph = [item["data"] for item in top_items if item["type"] == "graph"]
        final_docs = [item["data"] for item in top_items if item["type"] == "document"]

        return {
            "graph": final_graph,
            "documents": final_docs,
            "scored": top_items
        }