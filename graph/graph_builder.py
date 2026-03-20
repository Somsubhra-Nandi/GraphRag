import time
from graph.graph_client import GraphClient
from graph.entity_resolution import EntityResolver


class GraphBuilder:

    def __init__(self):

        self.client = GraphClient()
        self.resolver = EntityResolver()

    def add_triple(
        self, subject, relation, obj, properties=None,
        subject_type="Entity", object_type="Entity",
        source=None, chunk_id=None, confidence=0.9
    ):
        if str(obj).strip().isdigit() or str(subject).strip().isdigit():
            return  # Skip triples where subject or object is just a pure number

        subject = self.resolver.resolve(subject)
        obj = self.resolver.resolve(obj)
        
        if properties is None:
            properties = {}

        # Combine your standard metadata with the LLM's extracted properties
        edge_props = {
            "source": source,
            "chunk_id": chunk_id,
            "confidence": confidence,
            "timestamp": int(time.time())
        }
        edge_props.update(properties) # This merges 'year', 'amount', etc. into the database!

        # Use SET r += to dynamically attach all properties to the relationship
        query = f"""
        MERGE (a:{subject_type} {{name:$subject}})
        MERGE (b:{object_type} {{name:$object}})
        MERGE (a)-[r:`{relation}`]->(b)
        SET r += $edge_props
        """

        params = {
            "subject": subject,
            "object": obj,
            "edge_props": edge_props
        }

        self.client.run_query(query, params)