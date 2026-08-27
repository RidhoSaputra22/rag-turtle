

from pydantic import (
    ValidationError
)

from config import (
    SKILL_PATH,
    MAX_RETRIES
)

from rag.retriever import (
    Retriever
)

from llm.ollama_provider import (
    OllamaProvider
)

from scene.models import (
    Scene
)

# debug
from config import DEBUG_MODE

from utils.debug_mode import Debug
debug = Debug(DEBUG_MODE)


class TurtlePipeline:
    def __init__(self):
        self.llm = (
            OllamaProvider()
        )

        self.retriever = (
            Retriever()
        )

        self.skill = (
            SKILL_PATH.read_text(
                encoding="utf-8"
            )
        )


    def _build_context(
        self,
        hits
    ):
        if not hits:
            return (
                "No relevant draving"
                "Knowledge Found"
            )


        context = []
        
        for index, hit in enumerate(
            hits,
            start=1
        ):
            context.append(
                f"""
RECIPE {index}:
{hit["context"]}
"""
            )

        return "\n".join(
            context
        )

    def _clean_json(
        self,
        text
    ):
        text = text.strip()

        # fallback in case model 
        # add markdown

        if text.startswith(
            "```"
        ):

            lines = (
                text.splitlines()
            )

            lines = lines[1:]

            if (
                lines
                and
                lines[-1].startswith(
                    "```"
                )
            ):
                lines = lines[:-1]
            
            text = "\n".join(
                lines
            )

        # Extract Json object

        start = text.find("{")
        end = text.rfind("}")

        if (
            start != -1
            and end != -1
        ):
            text = text[
                start:end + 1
            ]
        
        return text
    
    def generate_scene(
        self,
        user_request
    ):

        # RAG

        hits = (
            self.retriever.search(
                user_request
            )
        )

        context = (
            self._build_context(
                hits
            )
        )

        # Initial Prompt

        prompt = f"""
DRAWING KNOWLEDGE

{context}


USER REQUEST


{user_request}



Create a valid scene JSON

Remember:

- User instructions override recipe defaults.
- Use recipes as guidance.
- Return JSON only.
"""

        raw_json, response = (
            self.llm.generate_json(
                self.skill,
                prompt
            )
        )

        debug.save_on_file(
            message=f"""
#skill

{self.skill}

# prompt

{prompt}

# response

{response}

# raw json

{raw_json}

# cleaned json

{
    (
        self._clean_json(
                    raw_json
                )
    )
}
"""
        )


        # Validate + Repair LOOP

        for attempt in range (
            MAX_RETRIES + 1
        ):

            cleaned = (
                self._clean_json(
                    raw_json
                )
            )

            try:
                
                scene = (
                    Scene.model_validate_json(
                        cleaned
                    )
                )

                return (
                    scene,
                    hits,
                    response
                )

            except ValidationError as error:

                if (
                    attempt
                    >= MAX_RETRIES
                ):

                    raise RuntimeError(
                        "LLM failed to"
                        "produce valid scene"
                    ) from error

                repair_prompt = f"""
Your previous scene JSON was invalid.

USER REQUEST:

{user_request}


DRAWING KNOWLEDGE:

{context}


INVALID JSON:

{cleaned}


VALIDATION ERROR:

{error}


Fix the JSON.

Return JSON only.
"""
                raw_json, response = (
                    self.llm.generate_json(
                        self.skill,
                        repair_prompt
                    )
                )
        raise RuntimeError(
            "Unexpected pipeline error."
        )