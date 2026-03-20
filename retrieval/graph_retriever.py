from extraction.entity_extractor import EntityExtractor
import json

class GraphRetriever:

    def __init__(self, graph_client, max_hops=2):

        self.client = graph_client
        self.entity_extractor = EntityExtractor()
        self.max_hops = max_hops

    def retrieve(self, query):

        entities = self.entity_extractor.extract(query)
        print(f"--> [DEBUG] extracted entities: {entities}")
        if not entities:
            return []

        results = []

        for ent in entities:

            name = ent["name"]

            cypher = f"""
            MATCH (source)-[r*1..{self.max_hops}]-(target)
            WHERE toLower(source.name) CONTAINS toLower($name)
            UNWIND r AS rel
            RETURN DISTINCT
                startNode(rel).name AS subject,
                type(rel) AS relation,
                endNode(rel).name AS object,
                properties(rel) AS properties
            LIMIT 20
            """

            data = self.client.run_query(cypher, {"name": name})

            results.extend(data)

        # deduplicate
        unique = []
        seen = set()
        for d in results:
            # Convert dict to a string to safely check for duplicates
            d_str = json.dumps(d, sort_keys=True)
            if d_str not in seen:
                seen.add(d_str)
                unique.append(d)

        return unique