from openai import OpenAI 
import llm
from llm.default_plugins.openai_models import Chat
class R1Chat(Chat):
    """
    A plugin that uses Nebius R1 (deepseek-ai/DeepSeek-R1) via an
    OpenAI-compatible endpoint, including streaming support.
    """

    # The short user-facing alias for -m r1
    model_id = "r1"

    # Key alias or environment var to look for:
    needs_key = "r1"
    key_env_var = "NEBIUS_API_KEY"

    # Whether it can stream
    can_stream = True

    # If you want to define model-level options, you could do so:
    class Options(Chat.Options):
        # For example, override or add custom fields
        pass

    def __init__(self):
        """
        The 'model_name' is the real name for the request:
          'deepseek-ai/DeepSeek-R1'
        'model_id' is how logs refer to it.
        """
        super().__init__(
            model_name="deepseek-ai/DeepSeek-R1",  # Actual remote model name
            model_id="r1",
            api_base="https://api.studio.nebius.ai/v1/",  # Nebius endpoint
            can_stream=True,
        )

    def execute(self, prompt, stream, response, conversation=None):
        """
        Called when LLM runs a sync prompt. If stream=True, yield partial tokens.
        If stream=False, yield entire text at once.
        """

        # 1. Build a client. This is an OpenAI() from python-openai but pointed at Nebius
        client = OpenAI(
            base_url=self.api_base,
            # See self.get_key() to retrieve from keys or env:
            api_key=self.get_key(),
        )

        # 2. Prepare messages
        #   If you want to replicate conversation logic (pull from conversation.responses),
        #   do so here or just rely on super().build_messages() from Chat class.
        messages = self.build_messages(prompt, conversation)

        # 3. Fire off the request
        kwargs = dict(
            model=self.model_name or self.model_id,  # "deepseek-ai/DeepSeek-R1"
            messages=messages,
            # You can parse your prompt.options.* if you want max_tokens, etc.
            max_tokens=prompt.options.max_tokens or 1024,
            temperature=prompt.options.temperature or 0.7,
            stream=stream,  # crucial
        )

        usage = None
        if stream:
            # We gather partial chunks as they come from .create(..., stream=True).
            completion = client.chat.completions.create(**kwargs)
            chunks = []
            for chunk in completion:
                chunks.append(chunk)
                if chunk.usage:
                    usage = chunk.usage.model_dump()
                # Extract partial text from chunk
                try:
                    content = chunk.choices[0].delta.content
                except IndexError:
                    content = None
                if content is not None:
                    # yield partial content to the console
                    yield content
            # Once done, we can store the final combined text or JSON
            # We replicate openai_models.py combine_chunks() if desired.
            # Minimal approach:
            response.response_json = {"chunks": [c.model_dump() for c in chunks]}
        else:
            # Non-streaming
            completion = client.chat.completions.create(**kwargs)
            # Typically there's just one chunk with final text
            usage = completion.usage.model_dump() if completion.usage else None
            # Just yield the entire text
            yield completion.choices[0].message.content
            response.response_json = completion.model_dump()

        # 4. Log usage tokens, if any
        if usage:
            # usage might have {"prompt_tokens": 123, "completion_tokens": 456, ...}
            # You can rename them to input=..., output=..., details=...
            input_tokens = usage.get("prompt_tokens")
            output_tokens = usage.get("completion_tokens")
            response.set_usage(input=input_tokens, output=output_tokens, details=usage)


@llm.hookimpl
def register_models(register):
    """
    The plugin hook that registers our r1 model with LLM.
    """
    # If there's no key found, skip
    key = llm.get_key(None, "r1", "NEBIUS_API_KEY")
    if not key:
        return

    # Register it:
    register(R1Chat())