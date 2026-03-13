import re


class DocumentCleaner:

    def clean(self, text):

        text = re.sub(r"\s+", " ", text)

        text = text.strip()

        return text