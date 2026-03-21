class HybridRetriever:

    def __init__(self, graph_retriever, vector_retriever, planner, reranker):
        self.graph = graph_retriever
        self.vector = vector_retriever
        self.planner = planner
        self.reranker = reranker

    def retrieve(self, query):

        plan = self.planner.plan(query)

        print("\n Query Plan:")
        print(plan)

        strategy = plan.get("strategy", "hybrid")

        graph_results = []
        doc_results = []

        if strategy == "graph":
            graph_results = self.graph.retrieve(query)

        elif strategy == "vector":
            doc_results = self.vector.retrieve(query)

        else:
            graph_results = self.graph.retrieve(query)
            doc_results = self.vector.retrieve(query)

        # NEW: Reranking
        reranked = self.reranker.rerank(
            query,
            graph_results,
            doc_results
        )

        return {
            "plan": plan,
            "graph": reranked["graph"],
            "documents": reranked["documents"],
            "debug": reranked["scored"]
        }