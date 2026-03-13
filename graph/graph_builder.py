from graph.graph_client import GraphClient


class GraphBuilder:

    def __init__(self):

        self.client = GraphClient()

    def add_triple(self, subject, relation, obj):

        query = """
        MERGE (a:Entity {name:$subject})
        MERGE (b:Entity {name:$object})
        MERGE (a)-[r:`%s`]->(b)
        """ % relation

        params = {
            "subject": subject,
            "object": obj
        }

        self.client.run_query(query, params)