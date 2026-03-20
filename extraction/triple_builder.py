class TripleBuilder:
    def build(self, extraction_result):
        triples = []
        #get the relations list
        for rel in extraction_result.get("relations", []):
            triples.append({
                "subject": rel["subject"],
                "relation": rel["relation"],
                "object": rel["object"],
                #grab properties, or default to an empty dictionary
                "properties": rel.get("properties", {}) 
            })
        return triples