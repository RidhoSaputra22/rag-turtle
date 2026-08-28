import ollama

from config import LLM_MODEL


class OllamaProvider:

    def __init__(
        self,
        model=LLM_MODEL
    ):

        self.model = model

    def generate_json(
        self,
        system_prompt,
        user_prompt,
        on_chunk=None,
        schema=None,
    ):

        stream = ollama.chat(

            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": (
                        system_prompt
                    )
                },
                {
                    "role": "user",
                    "content": (
                        user_prompt
                    )
                }
            ],

            # Ollama accepts a JSON Schema here. Supplying the Pydantic schema
            # makes a small model follow the contract much more reliably than
            # the generic `format="json"` mode alone.
            format=schema or "json",

            stream=True,

            # Qwen3 doesn't need
            # thinking for this task
            think=False,

            # Keep model loaded
            keep_alive=-1,

            options={
                "temperature": 0.2,
                "num_ctx": 4096,
                "num_predict": 600
            }
        )

        chunks = []
        final_response = None

        for response in stream:

            final_response = response

            content = (
                response.message.content
                or ""
            )

            if content:
                chunks.append(
                    content
                )

                if on_chunk:
                    on_chunk(
                        content
                    )

        if final_response is None:
            raise RuntimeError(
                "Ollama returned no response."
            )

        return (
            "".join(chunks),
            final_response
        )
