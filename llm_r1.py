import llm
from llm.default_plugins.openai_models import Chat

class DeepSeekR1(Chat):
    """
    A Chat model that appears as short name 'r1' to users,
    but internally calls the 'deepseek-ai/DeepSeek-R1' model
    via an OpenAI-compatible endpoint.
    """

    # Store key under alias "r1" or environment variable "NEBIUS_API_KEY"
    needs_key = "r1"
    key_env_var = "NEBIUS_API_KEY"

    def __init__(self):
        # The first argument is the actual 'model_name', used in the request
        # The second is the user-visible 'model_id' that LLM uses for logs, -m r1, etc.
        super().__init__(
            model_name="deepseek-ai/DeepSeek-R1",  # The real model for the request
            model_id="r1",                         # The short name recognized by LLM
            api_base="https://api.studio.nebius.ai/v1/",
            # can_stream=True if the Nebius endpoint supports streaming
            can_stream=False
        )

    def __str__(self):
        # Display name in logs, etc.
        return f"DeepSeek R1 alias: {self.model_id}"


@llm.hookimpl
def register_models(register):
    """
    Hook function that tells LLM this plugin provides a 'r1' model.
    """
    # If no key is set, skip registering to avoid "no key found" errors
    key = llm.get_key("", "r1", "NEBIUS_API_KEY")
    if not key:
        return

    register(DeepSeekR1())