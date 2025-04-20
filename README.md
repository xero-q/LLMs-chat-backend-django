### LLMs - Simulator Backend

LLMs - Simulator is a project that allows to define the info for any amount of LLMs both online and offline (using Ollama) and give them prompts and receive their response. Online LLMs can be OpenAI compatible or not.

The frontend for this project is this: [Angular frontend](https://github.com/xero-q/LLMs-chat-frontend-angular)

For defining a model you can access the [admin](http://localhost:8000/admin). Key fields: `identifier`, `provider`, `api_environment variable`,`temperature`, `api_environment variable` is used to define the environment variable for the api key for the model.
