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
        - Standardize the verbs (e.g., use ACQUIRED, FOUNDED, DEVELOPED).
        - EXTRACT ALL DATES AND NUMBERS: If a year, date, or number is mentioned in the same sentence as the relationship, you MUST extract it into the `properties` dictionary.

        === EXAMPLE ===
        Text: SpaceX was founded by Elon Musk in 2002.
        Entities: [{{"name": "SpaceX"}}, {{"name": "Elon Musk"}}]
        Output:
        {{
         "relations":[
           {{
             "subject":"SpaceX",
             "relation":"FOUNDED",
             "object":"Elon Musk",
             "properties": {{"year": "2002"}}
           }}
         ]
        }}
        === END EXAMPLE ===

        Now, process the following:
        Entities:
        {entities}

        Return ONLY the JSON format shown in the example.

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