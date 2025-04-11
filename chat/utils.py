import requests


class OllamaChatAI():
    def get_response(self, model: str, user_prompt: str) -> str:
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
                f"Error getting response from Ollama API. Status code: {response.status_code}, Response: {response.text}")
