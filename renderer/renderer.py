import turtle

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)

from renderer.objects import (
    draw_house,
    draw_tree,
    draw_sun,
    draw_cloud,
    draw_basic_object
)


def render_scene(
    scene,
    save_as=None
):

    screen = turtle.Screen()

    screen.setup(
        SCREEN_WIDTH,
        SCREEN_HEIGHT
    )

    screen.title(
        "Tiny LLM Turtle AI"
    )

    screen.bgcolor(
        scene.get(
            "background",
            "white"
        )
    )

    # Disable animation
    # while drawing
    screen.tracer(
        0,
        0
    )

    pen = turtle.Turtle()

    pen.hideturtle()

    pen.speed(0)

    for obj in scene[
        "objects"
    ]:

        obj_type = obj["type"]

        if obj_type == "house":

            draw_house(
                pen,
                obj
            )

        elif obj_type == "tree":

            draw_tree(
                pen,
                obj
            )

        elif obj_type == "sun":

            draw_sun(
                pen,
                obj
            )

        elif obj_type == "cloud":

            draw_cloud(
                pen,
                obj
            )

        else:

            draw_basic_object(
                pen,
                obj
            )

    # Draw everything at once
    screen.update()

    # Optional export
    if save_as:

        canvas = (
            screen.getcanvas()
        )

        canvas.postscript(
            file=save_as
        )

    screen.mainloop()