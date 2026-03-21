from openai import OpenAI
from configs.settings import settings
import json


class CombinedExtractor:

    def __init__(self):
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=settings.OPENAI_API_KEY
        )

    def extract(self, text):

        prompt = f"""
You are an information extraction system for a knowledge graph.

Extract BOTH:
1. Entities
2. Relationships

Rules:
- Entity types should be dynamic (Company, Person, Technology, Concept, etc.)
- Do NOT extract standalone numbers/dates as entities
- Relations must be UPPERCASE_WITH_UNDERSCORES
- Extract ALL numbers/dates into relation properties

Return ONLY JSON:

{{
  "entities": [
    {{"name": "Entity", "type": "Type"}}
  ],
  "relations": [
    {{
      "subject": "Entity1",
      "relation": "RELATION_TYPE",
      "object": "Entity2",
      "properties": {{"year": "2020"}}
    }}
  ]
}}

Text:
{text}
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content

        # try:
        #     return json.loads(content)
        # except Exception:
        #     return {"entities": [], "relations": []}
        return json.loads(content)