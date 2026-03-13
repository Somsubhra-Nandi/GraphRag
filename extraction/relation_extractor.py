from openai import OpenAI
from configs.settings import settings
import json


class RelationExtractor:

    def __init__(self):

        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=settings.OPENAI_API_KEY
        )

    def extract(self, text, entities):

        prompt = f"""
Extract relationships between the provided entities.

Entities:
{entities}

Return JSON format:

{{
 "relations":[
   {{
     "subject":"entity",
     "relation":"RELATION_TYPE",
     "object":"entity"
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

        return json.loads(content)