class TripleBuilder:

    def build(self, extraction_result):

        triples = []

        for relation in extraction_result["relations"]:

            triples.append({
                "subject": relation["subject"],
                "relation": relation["relation"],
                "object": relation["object"]
            })

        return triples