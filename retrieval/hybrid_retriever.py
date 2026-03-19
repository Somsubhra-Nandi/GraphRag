class HybridRetriever:

    def __init__(self, graph_retriever, vector_retriever):

        self.graph = graph_retriever
        self.vector = vector_retriever

    def retrieve(self, query):

        graph_context = self.graph.retrieve(query)

        vector_context = self.vector.retrieve(query)

        return {
            "graph": graph_context,
            "documents": vector_context
        }