import requests
from dotenv import load_dotenv
from .models import Model, Thread
import os
from abc import ABC, abstractmethod
from langchain.schema import HumanMessage
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage

load_dotenv()


class LangChainModel():
    def __init__(self, model: Model, provider_name: str, thread_id):
        try:
            self._chat_model = init_chat_model(model.name,
                                               model_provider=provider_name, api_key=os.getenv(model.api_environment_variable), temperature=model.temperature)

            thread = Thread.objects.get(pk=thread_id)
            prompts = thread.prompts.all().order_by('created_at')

            self._messages = []
            for prompt in prompts:
                self._messages.append(HumanMessage(content=prompt.prompt))
                self._messages.append(AIMessage(content=prompt.response))

        except Exception as e:
            raise Exception(f"Error creating LangChain model\n{e}")

    def get_response(self, user_prompt: str) -> str:
        try:
            self._messages.append(HumanMessage(content=user_prompt))
            response = self._chat_model.invoke(self._messages)
            return response.content

        except Exception as e:
            raise Exception(f"Error getting response from AI API.\n{e}")


class AIChat():
    def __init__(self, model: Model, provider: str, thread_id: int):
        self._llm_model = LangChainModel(model, provider, thread_id)

    def get_response(self, user_prompt: str) -> str:
        return self._llm_model.get_response(user_prompt)


class AIChatCreator(ABC):
    @abstractmethod
    def create_ai_chat(self, model: Model, thread_id: int) -> AIChat:
        pass


class OllamaChatCreator(AIChatCreator):
    def create_ai_chat(self, model: Model, thread_id: int) -> AIChat:
        return OllamaAIChat(model, thread_id)


class OpenAIChatCreator(AIChatCreator):
    def create_ai_chat(self, model: Model, thread_id: int) -> AIChat:
        return AIChat(model, "openai", thread_id)


class GeminiAIChatCreator(AIChatCreator):
    def create_ai_chat(self, model: Model, thread_id: int) -> AIChat:
        return AIChat(model, "google_genai", thread_id)


class HuggingFaceAIChatCreator(AIChatCreator):
    def create_ai_chat(self, model: Model, thread_id: int) -> AIChat:
        return AIChat(model, "huggingface", thread_id)


class AnthropicAIChatCreator(AIChatCreator):
    def create_ai_chat(self, model: Model, thread_id: int) -> AIChat:
        return AIChat(model, "anthropic", thread_id)


class DeepSeekAIChatCreator(AIChatCreator):
    def create_ai_chat(self, model: Model, thread_id: int) -> AIChat:
        return AIChat(model, "deepseek", thread_id)


class MistralAIChatCreator(AIChatCreator):
    def create_ai_chat(self, model: Model, thread_id: int) -> AIChat:
        return AIChat(model, "mistralai", thread_id)


class OllamaAIChat(AIChat):
    def __init__(self, model: Model):
        self._model = model

    def get_response(self, user_prompt: str) -> str:
        url = "http://localhost:11434/api/generate"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": self._model.name,
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
