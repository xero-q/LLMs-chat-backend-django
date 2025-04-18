import requests
from dotenv import load_dotenv
from .models import Model
import os
from abc import ABC, abstractmethod
from langchain.schema import HumanMessage
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

load_dotenv()


class AIChat(ABC):
    @abstractmethod
    def get_response(self, model: Model, user_prompt: str) -> str:
        pass
        """ Get response from AI model.
        This method gets the response for the corresponding user's prompt using the data of the model
        Each descendant implementes the method of a different kind of model
        Args:
            user_prompt (str): The user's input prompt.

        Returns:
            str: The AI's response.
        """


class LangChainModel():
    def __init__(self, model: Model, provider_name: str):
        try:
            self._model = init_chat_model(model.name,
                                          model_provider=provider_name, api_key=os.getenv(model.api_environment_variable), temperature=model.temperature)
        except Exception as e:
            raise Exception(f"Error creating LangChain model\n{e}")

    def get_response(self, user_prompt: str) -> str:
        try:
            response = self._model.invoke([HumanMessage(content=user_prompt)])

            return response.content
        except Exception as e:
            raise Exception(f"Error getting response from AI API.\n{e}")


class AIChatCreator(ABC):
    @abstractmethod
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


class AnthropicAIChatCreator(AIChatCreator):
    def create_ai_chat(self):
        return AnthropicAIChat()


class DeepSeekAIChatCreator(AIChatCreator):
    def create_ai_chat(self):
        return DeepSeekAIChat()


class MistralAIChatCreator(AIChatCreator):
    def create_ai_chat(self):
        return MistralAIChat()


class HuggingFaceAIChat(AIChat):
    def get_response(self, model: Model, user_prompt: str) -> str:
        model = LangChainModel(model, "huggingface")
        return model.get_response(user_prompt)


class OpenAIChat(AIChat):
    def get_response(self, model: Model, user_prompt: str) -> str:
        model = LangChainModel(model, "openai")
        return model.get_response(user_prompt)


class DeepSeekAIChat(AIChat):
    def get_response(self, model: Model, user_prompt: str) -> str:
        model = LangChainModel(model, "deepseek")
        return model.get_response(user_prompt)


class AnthropicAIChat(AIChat):
    def get_response(self, model: Model, user_prompt: str) -> str:
        model = LangChainModel(model, "anthropic")
        return model.get_response(user_prompt)


class MistralAIChat(AIChat):
    def get_response(self, model: Model, user_prompt: str) -> str:
        model = LangChainModel(model, "mistralai")
        return model.get_response(user_prompt)


class GeminiAIChat(AIChat):
    def get_response(self, model: Model, user_prompt: str) -> str:
        model = LangChainModel(model, "google_genai")
        return model.get_response(user_prompt)


class OllamaAIChat(AIChat):
    def get_response(self, model: Model, user_prompt: str) -> str:
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
