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
        user_prompt
    ):

        response = ollama.chat(

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

            # Force JSON output
            format="json",

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

        return (
            response.message.content,
            response
        )