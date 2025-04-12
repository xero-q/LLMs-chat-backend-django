import requests


class OpenAIChat():
    def __init__(self, openai_instance):
        self.client = openai_instance

    def get_response(self, model: str, user_prompt: str):
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            # Devuelve el contenido del mensaje de respuesta
            return response.choices[0].message.content
        except Exception as e:
            raise Exception("Error getting response from AI API")
