import requests
from dotenv import load_dotenv
from .models import Model
import os
from abc import ABC
from langchain.schema import HumanMessage
from langchain.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.llms import HuggingFaceHub
from langchain_anthropic import ChatAnthropic
from langchain_deepseek import ChatDeepSeek

load_dotenv()


class AIChat(ABC):
    def get_response(self, model: Model, user_prompt: str) -> str:
        pass


class LangChainModel():
    def __init__(self, provider):
        self._provider = provider

    def get_response(self, user_prompt) -> str:
        messages = [HumanMessage(content=user_prompt)]
        response = self._provider(messages)

        return response.content if hasattr(response, 'content') else response


class LangChainModelSimple():
    def __init__(self, provider):
        self._provider = provider

    def get_response(self, user_prompt) -> str:
        return self._provider.invoke(user_prompt)


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


class AnthropicAIChatCreator(AIChatCreator):
    def create_ai_chat(self):
        return AnthropicAIChat()


class DeepSeekAIChatCreator(AIChatCreator):
    def create_ai_chat(self):
        return DeepSeekAIChat()


class HuggingFaceAIChat(AIChat):
    def get_response(self, model: Model, user_prompt: str) -> str:
        try:
            provider = HuggingFaceHub(repo_id=model.name, model_kwargs={"temperature": model.temperature},
                                      huggingfacehub_api_token=os.getenv(model.api_environment_variable))
            model = LangChainModelSimple(provider)
        except Exception as e:
            raise Exception(f"Error creating OpenAI client.\n{e}")

        try:
            return model.get_response(user_prompt)
        except Exception as e:
            raise Exception(f"Error getting response from AI API.\n{e}")


class OpenAIChat(AIChat):
    def get_response(self, model: Model, user_prompt: str) -> str:
        try:
            provider = ChatOpenAI(model_name=model.name,
                                  temperature=model.temperature, openai_api_key=os.getenv(model.api_environment_variable))
            model = LangChainModel(provider)
        except Exception as e:
            raise Exception(f"Error creating OpenAI client.\n{e}")

        try:
            return model.get_response(user_prompt)
        except Exception as e:
            raise Exception(f"Error getting response from AI API.\n{e}")


class DeepSeekAIChat(AIChat):
    def get_response(self, model: Model, user_prompt: str) -> str:
        try:
            provider = ChatDeepSeek(model=model.name,
                                    temperature=model.temperature,
                                    api_base=model.base_url,
                                    api_key=os.getenv(model.api_environment_variable))
            model = LangChainModelSimple(provider)
        except Exception as e:
            raise Exception(f"Error creating OpenAI client.\n{e}")

        try:
            return model.get_response(user_prompt)
        except Exception as e:
            raise Exception(f"Error getting response from AI API.\n{e}")


class AnthropicAIChat(AIChat):
    def get_response(self, model: Model, user_prompt: str) -> str:
        try:
            provider = ChatAnthropic(model=model.name,
                                     temperature=model.temperature, anthropic_api_key=os.getenv(model.api_environment_variable))
            model = LangChainModelSimple(provider)
        except Exception as e:
            raise Exception(f"Error creating OpenAI client.\n{e}")

        try:
            return model.get_response(user_prompt)
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
            provider = ChatGoogleGenerativeAI(model=model.name,
                                              temperature=model.temperature,
                                              google_api_key=os.getenv(
                                                  model.api_environment_variable),
                                              convert_system_message_to_human=True
                                              )
            model = LangChainModel(provider)
        except Exception as e:
            raise Exception(f"Error creating Gemini client.\n{e}")

        try:
            return model.get_response(user_prompt)
        except Exception as e:
            raise Exception(f"Error getting response from AI API.\n{e}")
