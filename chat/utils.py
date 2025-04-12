import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class OnlineAIChat():
    def get_response(self, model: str, user_prompt: str):
        try:
            client = OpenAI(base_url="https://api.deepinfra.com/v1/openai")
        except Exception as e:
            raise Exception("Error creating OpenAI client")

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            # Devuelve el contenido del mensaje de respuesta
            return response.choices[0].message.content
        except Exception as e:
            print(e)
            raise Exception("Error getting response from AI API")


class OfflineAIChat():
    def get_response(self, model: str, user_prompt: str):
        """ Get response from Ollama model.
        This method sends a request to the Ollama API with the user's prompt
        and retrieves the generated response.
        It uses the Mistral model for generating responses.

        Args:
            user_prompt (str): The user's input prompt.

        Returns:
            str: The AI's response.
        """
        url = "http://localhost:11434/api/generate"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": model,
            "prompt": user_prompt,
            "stream": False
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data.get("response")
        else:
            raise Exception(
                f"Error getting response from AI API.\nResponse status: {response.status_code}\nMessage: {response.text}")
