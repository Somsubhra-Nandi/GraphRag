import os
from configs.settings import settings


class DocumentLoader:

    def load_documents(self):

        documents = []

        for file in os.listdir(settings.DATA_PATH):

            path = os.path.join(settings.DATA_PATH, file)

            with open(path, "r", encoding="utf-8") as f:

                text = f.read()

                documents.append({
                    "doc_id": file,
                    "text": text
                })

        return documents