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
    draw_mountain,
    draw_hill,
    draw_river,
    draw_bush,
    draw_flower,
    draw_moon,
    draw_star,
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

        elif obj_type == "mountain":

            draw_mountain(
                pen,
                obj
            )

        elif obj_type == "hill":

            draw_hill(
                pen,
                obj
            )

        elif obj_type == "river":

            draw_river(
                pen,
                obj
            )

        elif obj_type == "bush":

            draw_bush(
                pen,
                obj
            )

        elif obj_type == "flower":

            draw_flower(
                pen,
                obj
            )

        elif obj_type == "moon":

            draw_moon(
                pen,
                obj
            )

        elif obj_type == "star":

            draw_star(
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
