class HybridRetriever:

    def __init__(self, graph_retriever, vector_retriever, planner):
        self.graph = graph_retriever
        self.vector = vector_retriever
        self.planner = planner

    def retrieve(self, query):

        plan = self.planner.plan(query)
        print("\n Query Plan:")
        print(plan)

        strategy = plan.get("strategy", "hybrid")

        results = {
            "plan": plan,
            "graph": [],
            "documents": []
        }

        if strategy == "graph":
            results["graph"] = self.graph.retrieve(query)

        elif strategy == "vector":
            results["documents"] = self.vector.retrieve(query)

        else:  # hybrid
            results["graph"] = self.graph.retrieve(query)
            results["documents"] = self.vector.retrieve(query)

        return results