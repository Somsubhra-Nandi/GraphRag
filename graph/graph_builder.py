import time
from graph.graph_client import GraphClient
from graph.entity_resolution import EntityResolver


class GraphBuilder:

    def __init__(self):

        self.client = GraphClient()
        self.resolver = EntityResolver()

    def add_triple(
        self,
        subject,
        relation,
        obj,
        subject_type="Entity",
        object_type="Entity",
        source=None,
        chunk_id=None,
        confidence=0.9
    ):

        subject = self.resolver.resolve(subject)
        obj = self.resolver.resolve(obj)

        query = f"""
        MERGE (a:{subject_type} {{name:$subject}})
        MERGE (b:{object_type} {{name:$object}})
        MERGE (a)-[r:`{relation}` {{
            source:$source,
            chunk_id:$chunk_id,
            confidence:$confidence,
            timestamp:$timestamp
        }}]->(b)
        """

        params = {
            "subject": subject,
            "object": obj,
            "source": source,
            "chunk_id": chunk_id,
            "confidence": confidence,
            "timestamp": int(time.time())
        }

        self.client.run_query(query, params)