from openai import OpenAI
from configs.settings import settings


class AnswerGenerator:

    def __init__(self):
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=settings.OPENAI_API_KEY
        )

    def generate(self, context):

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise reasoning assistant."},
                {"role": "user", "content": context}
            ]
        )

        return response.choices[0].message.content