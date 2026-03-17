# import spacy
# from configs.graph_schema import BASE_ENTITY_TYPES


# class EntityExtractor:

#     def __init__(self):
#         self.nlp = spacy.load("en_core_web_sm")

#     def extract(self, text):

#         doc = self.nlp(text)

#         entities = []

#         for ent in doc.ents:

#             entity = {
#                 "name": ent.text,
#                 "type": ent.label_
#             }

#             entities.append(entity)

#         return entities

from openai import OpenAI
from configs.settings import settings
import json

class EntityExtractor:
    def __init__(self):
        # Pointing to the free GitHub Models endpoint!
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=settings.OPENAI_API_KEY
        )

    def extract(self, text):
        prompt = f"""
        Extract the core entities (like companies, people, technologies, locations) from the text.
        
        Text:
        {text}

        Return exactly this JSON format:
        {{
            "entities": [
                {{"name": "EntityName", "type": "EntityType"}}
            ]
        }}
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content
        return json.loads(content).get("entities", [])