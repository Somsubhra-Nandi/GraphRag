class ContextBuilder:

    def build(self, query, graph_results, doc_results):

        #Format Graph Facts
        graph_facts = []
        for g in graph_results:
            fact = f"{g['subject']} {g['relation']} {g['object']}"

            if g.get("properties"):
                props = ", ".join([f"{k}: {v}" for k, v in g["properties"].items()])
                fact += f" ({props})"

            graph_facts.append(fact)

        #Format Documents
        documents = []
        for d in doc_results:
            documents.append(d["text"])

        #Build Structured Context
        context = f"""
You are given structured knowledge to answer a query.

=== QUERY ===
{query}

=== FACTS (Graph Knowledge) ===
{chr(10).join(graph_facts) if graph_facts else "None"}

=== EVIDENCE (Documents) ===
{chr(10).join(documents) if documents else "None"}

=== INSTRUCTIONS ===
- Use ONLY the provided information
- Prefer FACTS for relationships
- Use DOCUMENTS for explanation
- Combine both for reasoning
- If insufficient data, say "I don't know"

Answer:
"""

        return context.strip()