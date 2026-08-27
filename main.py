

from agent.pipeline import (
    TurtlePipeline
)

from scene.normalizer import (
    normalize_scene
)

from renderer.renderer import (
    render_scene
)


class ConsoleReporter:
    def __init__(self):
        self.streaming = False
        self.stream_label = None

    def status(
        self,
        message
    ):

        self.finish_stream()

        print(
            f"[SYSTEM] {message}",
            flush=True
        )

    def chunk(
        self,
        label,
        content
    ):

        if (
            not self.streaming
            or self.stream_label != label
        ):
            self.finish_stream()

            print(
                f"\n[MODEL {label}]",
                flush=True
            )

            self.streaming = True
            self.stream_label = label

        print(
            content,
            end="",
            flush=True
        )

    def finish_stream(self):

        if self.streaming:
            print(
                "",
                flush=True
            )

            self.streaming = False
            self.stream_label = None


def print_plan(
    plan
):

    print(
        "\nScenery plan:"
    )

    print(
        plan.model_dump_json(
            indent=2
        )
    )


def print_retrieval(
    hits
):

    print(
        "\nRetrieved knowledge:"
    )

    for hit in hits:

        metadata = hit[
            "metadata"
        ]

        distance = hit[
            "distance"
        ]

        print(
            f"- "
            f"{metadata['source']} "
            f"(distance="
            f"{distance:.4f})"
        )


def print_model_usage(
    responses
):

    print(
        "\nModel usage:"
    )

    total_prompt = 0
    total_output = 0

    for label, response in responses:

        prompt_tokens = (
            response.prompt_eval_count
            or 0
        )

        output_tokens = (
            response.eval_count
            or 0
        )

        eval_duration = (
            response.eval_duration
            or 0
        )

        seconds = (
            eval_duration
            / 1_000_000_000
        )

        token_per_second = (
            output_tokens / seconds
            if seconds > 0
            else 0
        )

        total_prompt += prompt_tokens
        total_output += output_tokens

        print(
            f"{label:<12}: "
            f"model={response.model}, "
            f"prompt={prompt_tokens}, "
            f"output={output_tokens}, "
            f"token/sec={token_per_second:.2f}"
        )

    print(
        f"Total       : "
        f"prompt={total_prompt}, "
        f"output={total_output}"
    )


def main():

    pipeline = (
        TurtlePipeline()
    )

    reporter = (
        ConsoleReporter()
    )

    print(
        "\n"
        "=============================="
    )

    request = input(
        "Describe image: "
    ).strip()

  

   

    try:

        # ==================
        # GENERATION
        # ==================

        reporter.status(
            "Memulai generate scene..."
        )

        (
            result
        ) = pipeline.generate_scene(
            request,
            on_status=reporter.status,
            on_chunk=reporter.chunk
        )

        reporter.finish_stream()

        # ==================
        # DEBUG
        # ==================

        

        print_plan(
            result.plan
        )

        print_retrieval(
            result.hits
        )

        print_model_usage(
            [
                (
                    "Plan",
                    result.plan_response
                ),
                (
                    "Scene",
                    result.scene_response
                )
            ]
        )

        print(
            "\nGenerated scene:"
        )

        print(
            result.scene.model_dump_json(
                indent=2
            )
        )

        # ==================
        # NORMALIZE
        # ==================

        normalized = (
            normalize_scene(
                result.scene
            )
        )

        reporter.status(
            "Normalisasi scene selesai."
        )

        # ==================
        # RENDER
        # ==================

        reporter.status(
            "Membuka jendela render Turtle..."
        )

        render_scene(
            normalized
        )

    except Exception as error:

        reporter.finish_stream()

        print(
            f"\nERROR: {error}"
        )

        


if __name__ == "__main__":
    main()
