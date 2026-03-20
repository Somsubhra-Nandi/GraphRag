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

        Rules for relations:
        - The relation MUST be a single, uppercase string with underscores.
        - Standardize the verbs (e.g., use ACQUIRED instead of bought, FOUNDED instead of created).
        - IMPORTANT: If there is a crucial number, year, date, or amount tied to this relationship, extract it and place it in the `properties` dictionary.
        
        Entities:
        {entities}

        Return JSON format:
        {{
         "relations":[
           {{
             "subject":"entity",
             "relation":"RELATION_TYPE",
             "object":"entity",
             "properties": {{"year": "2019", "amount": "500"}} // Include this ONLY if numbers/dates exist!
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