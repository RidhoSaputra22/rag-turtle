

from agent.pipeline import (
    TurtlePipeline
)

from scene.normalizer import (
    normalize_scene
)

from renderer.renderer import (
    render_scene
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
    response
):

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

    print(
        "\nModel usage:"
    )

    print(
        f"Model        : "
        f"{response.model}"
    )

    print(
        f"Prompt token : "
        f"{prompt_tokens}"
    )

    print(
        f"Output token : "
        f"{output_tokens}"
    )

    print(
        f"Token/sec    : "
        f"{token_per_second:.2f}"
    )


def main():

    pipeline = (
        TurtlePipeline()
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

        (
            scene,
            hits,
            response
        ) = pipeline.generate_scene(
            request
        )

        # ==================
        # DEBUG
        # ==================

        

        print_retrieval(
            hits
        )

        print_model_usage(
            response
        )

        print(
            "\nGenerated scene:"
        )

        print(
            scene.model_dump_json(
                indent=2
            )
        )

        # ==================
        # NORMALIZE
        # ==================

        normalized = (
            normalize_scene(
                scene
            )
        )

        # ==================
        # RENDER
        # ==================

        render_scene(
            normalized
        )

    except Exception as error:

        print(
            f"\nERROR: {error}"
        )

        


if __name__ == "__main__":
    main()