from renderer.primitives import (
    rectangle,
    polygon,
    circle,
    line
)


def draw_house(
    t,
    obj
):

    x = obj["x"]
    y = obj["y"]

    scale = obj["scale"]

    color = obj["color"]

    roof_color = (
        obj.get(
            "secondary_color"
        )
        or "darkred"
    )

    props = obj.get(
        "properties",
        {}
    )

    style = props.get(
        "style",
        "basic"
    )

    windows = int(
        props.get(
            "windows",
            2
        )
    )

    windows = max(
        1,
        min(
            windows,
            6
        )
    )

    chimney = props.get(
        "chimney",
        False
    )

    # -------------------------
    # HOUSE SIZE
    # -------------------------

    body_width = (
        220 * scale
    )

    body_height = (
        150 * scale
    )

    roof_height = (
        90 * scale
    )

    # -------------------------
    # BODY
    # -------------------------

    rectangle(
        t,
        x,
        y,
        body_width,
        body_height,
        fill=color
    )

    # -------------------------
    # ROOF
    # -------------------------

    roof_bottom = (
        y + body_height / 2
    )

    roof_points = [

        (
            x - body_width / 2 - 10,
            roof_bottom
        ),

        (
            x,
            roof_bottom
            + roof_height
        ),

        (
            x + body_width / 2 + 10,
            roof_bottom
        )
    ]

    polygon(
        t,
        roof_points,
        fill=roof_color
    )

    # -------------------------
    # DOOR
    # -------------------------

    door_width = (
        38 * scale
    )

    door_height = (
        70 * scale
    )

    rectangle(
        t,
        x,
        (
            y
            - body_height / 2
            + door_height / 2
        ),
        door_width,
        door_height,
        fill="saddlebrown"
    )

    # -------------------------
    # WINDOWS
    # -------------------------

    window_width = (
        30 * scale
    )

    window_height = (
        38 * scale
    )

    spacing = (
        body_width
        / (windows + 1)
    )

    for i in range(windows):

        wx = (
            x
            - body_width / 2
            + spacing * (i + 1)
        )

        # avoid placing a window
        # directly on the door

        if abs(wx - x) < (
            door_width
        ):
            continue

        rectangle(
            t,
            wx,
            y + 18 * scale,
            window_width,
            window_height,
            fill="lightblue"
        )

    # -------------------------
    # CHIMNEY
    # -------------------------

    if chimney:

        rectangle(
            t,
            (
                x
                + body_width * 0.28
            ),
            (
                roof_bottom
                + roof_height * 0.55
            ),
            25 * scale,
            70 * scale,
            fill="firebrick"
        )

    # -------------------------
    # VICTORIAN DETAIL
    # -------------------------

    if style == "victorian":

        # attic window

        circle(
            t,
            x,
            (
                roof_bottom
                + roof_height * 0.42
            ),
            14 * scale,
            fill="lightyellow"
        )

        # decorative horizontal trim

        line(
            t,
            (
                x
                - body_width / 2
            ),
            (
                y
                + body_height * 0.25
            ),
            body_width,
            color="brown",
            width=2
        )


def draw_tree(
    t,
    obj
):

    x = obj["x"]
    y = obj["y"]

    scale = obj["scale"]

    leaf_color = (
        obj["color"]
        if obj["color"] != "black"
        else "forestgreen"
    )

    trunk_height = (
        100 * scale
    )

    rectangle(
        t,
        x,
        y,
        28 * scale,
        trunk_height,
        fill="saddlebrown"
    )

    canopy_y = (
        y
        + trunk_height * 0.75
    )

    radius = (
        55 * scale
    )

    circle(
        t,
        x,
        canopy_y,
        radius,
        fill=leaf_color
    )

    circle(
        t,
        x - 35 * scale,
        canopy_y - 10 * scale,
        radius * 0.75,
        fill=leaf_color
    )

    circle(
        t,
        x + 35 * scale,
        canopy_y - 10 * scale,
        radius * 0.75,
        fill=leaf_color
    )


def draw_sun(
    t,
    obj
):

    x = obj["x"]
    y = obj["y"]

    scale = obj["scale"]

    radius = (
        40 * scale
    )

    color = (
        obj["color"]
        if obj["color"] != "black"
        else "gold"
    )

    circle(
        t,
        x,
        y,
        radius,
        fill=color
    )

    for angle in range(
        0,
        360,
        45
    ):

        line(
            t,
            x,
            y,
            70 * scale,
            angle,
            color=color,
            width=2
        )


def draw_cloud(
    t,
    obj
):

    x = obj["x"]
    y = obj["y"]

    scale = obj["scale"]

    color = (
        obj["color"]
        if obj["color"] != "black"
        else "white"
    )

    circle(
        t,
        x,
        y,
        35 * scale,
        fill=color
    )

    circle(
        t,
        x - 35 * scale,
        y - 5 * scale,
        28 * scale,
        fill=color
    )

    circle(
        t,
        x + 35 * scale,
        y - 5 * scale,
        28 * scale,
        fill=color
    )


def draw_basic_object(
    t,
    obj
):

    obj_type = obj["type"]

    x = obj["x"]
    y = obj["y"]

    scale = obj["scale"]

    color = obj["color"]

    if obj_type == "rectangle":

        rectangle(
            t,
            x,
            y,
            120 * scale,
            80 * scale,
            fill=color
        )

    elif obj_type == "circle":

        circle(
            t,
            x,
            y,
            50 * scale,
            fill=color
        )

    elif obj_type == "triangle":

        size = (
            100 * scale
        )

        polygon(
            t,
            [
                (
                    x,
                    y + size / 2
                ),
                (
                    x - size / 2,
                    y - size / 2
                ),
                (
                    x + size / 2,
                    y - size / 2
                )
            ],
            fill=color
        )

    elif obj_type == "line":

        line(
            t,
            x,
            y,
            120 * scale,
            color=color
        )