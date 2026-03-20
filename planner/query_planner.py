from openai import OpenAI
from configs.settings import settings
import json


class QueryPlanner:

    def __init__(self):
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=settings.OPENAI_API_KEY
        )

    def plan(self, query: str):

        prompt = f"""
You are a Query Planning Agent for a GraphRAG system.

Your job is to analyze the user query and decide the BEST retrieval strategy.

Available strategies:
1. graph → for factual, relationship-based queries
2. vector → for conceptual, explanatory queries
3. hybrid → for complex queries requiring both

Rules:
- Use graph when query involves relationships, dates, or specific facts
- Use vector when query asks "why", "how", "explain"
- Use hybrid when both reasoning + facts are needed
- Extract important entities from the query
- Generate step-by-step retrieval plan

Return ONLY valid JSON in this format:
{{
  "strategy": "graph | vector | hybrid",
  "entities": ["..."],
  "steps": ["...", "..."],
  "reasoning": "short explanation"
}}

Query:
{query}
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except Exception:
            return {
                "strategy": "hybrid",
                "entities": [],
                "steps": ["fallback retrieval"],
                "reasoning": "failed to parse planner output"
            }