import spacy
from configs.graph_schema import BASE_ENTITY_TYPES


class EntityExtractor:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract(self, text):

        doc = self.nlp(text)

        entities = []

        for ent in doc.ents:

            entity = {
                "name": ent.text,
                "type": ent.label_
            }

            entities.append(entity)

        return entities