import requests
from dotenv import load_dotenv
from .models import Thread
import os
from abc import ABC, abstractmethod
from langchain.schema import HumanMessage
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage

load_dotenv()


class LangChainModel:
    def __init__(self, thread: Thread):
        try:
            model = thread.model
            provider = thread.model.provider.name

            if provider != "ollama":
                self._chat_model = init_chat_model(
                    model.identifier,
                    model_provider=provider,
                    api_key=os.getenv(model.api_environment_variable),
                    temperature=model.temperature,
                )
            else:
                self._chat_model = init_chat_model(
                    model.identifier,
                    model_provider=provider,
                    temperature=model.temperature,
                    timeout=30
                )

            prompts = thread.prompts.all().order_by("created_at")

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
