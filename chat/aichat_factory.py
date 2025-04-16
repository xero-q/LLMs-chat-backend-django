import requests
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv
from .models import Model
import os
from abc import ABC

load_dotenv()


class AIChat(ABC):
    def get_response(self, model: Model, user_prompt: str) -> str:
        pass


class AIChatCreator(ABC):
    def create_ai_chat() -> AIChat:
        pass


class OllamaChatCreator(AIChatCreator):
    def create_ai_chat(self):
        return OllamaAIChat()


class OpenAIChatCreator(AIChatCreator):
    def create_ai_chat(self):
        return OpenAIChat()


class GeminiAIChatCreator(AIChatCreator):
    def create_ai_chat(self):
        return GeminiAIChat()


class HuggingFaceAIChatCreator(AIChatCreator):
    def create_ai_chat(self):
        return HuggingFaceAIChat()


class HuggingFaceAIChat(AIChat):
    def get_response(self, model: Model, user_prompt: str) -> str:
        api_key = os.getenv(model.api_environment_variable)
        base_url = model.base_url
        headers = {"Authorization": f"Bearer {api_key}"}

        data = {
            "inputs": user_prompt,
        }

        response = requests.post(base_url, headers=headers, json=data)

        if response.status_code == 200:
            data = response.json()
            return data[0]['generated_text']
        else:
            raise Exception(
                f"Error getting response from AI API.\nResponse status: {response.status_code}\nMessage: {response.text}")


class OpenAIChat(AIChat):
    def get_response(self, model: Model, user_prompt: str) -> str:
        try:
            api_key = os.getenv(model.api_environment_variable)
            client = OpenAI(api_key=api_key, base_url=model.base_url)
        except Exception as e:
            raise Exception(f"Error creating OpenAI client.\n{e}")

        try:
            response = client.chat.completions.create(
                model=model.name,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            # Devuelve el contenido del mensaje de respuesta
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error getting response from AI API.\n{e}")


class OllamaAIChat(AIChat):
    def get_response(self, model: Model, user_prompt: str) -> str:
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
            "model": model.name,
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


class GeminiAIChat(AIChat):
    def get_response(self, model: Model, user_prompt: str) -> str:
        """ Get response from Gemini model.
        This method sends a request to the Gemini API with the user's prompt
        and retrieves the generated response.
        It uses the Mistral model for generating responses.
        """
        try:
            api_key = os.getenv(model.api_environment_variable)
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model.name)
        except Exception as e:
            raise Exception(f"Error creating Gemini client.\n{e}")

        try:
            chat = model.start_chat()

            chat_response = chat.send_message(user_prompt)
            return chat_response.text

        except Exception as e:
            raise Exception(f"Error getting response from AI API.\n{e}")
