import math

from renderer.primitives import (
    rectangle,
    polygon,
    circle,
    line
)


def _property(
    obj,
    name,
    default=None
):

    return obj.get(
        "properties",
        {}
    ).get(
        name,
        default
    )


def _number_property(
    obj,
    name,
    default
):

    value = _property(
        obj,
        name,
        default
    )

    try:
        return float(value)
    except (
        TypeError,
        ValueError
    ):
        return default


def _int_property(
    obj,
    name,
    default,
    minimum,
    maximum
):

    value = _property(
        obj,
        name,
        default
    )

    try:
        value = int(value)
    except (
        TypeError,
        ValueError
    ):
        value = default

    return max(
        minimum,
        min(
            value,
            maximum
        )
    )


def _bool_property(
    obj,
    name,
    default=False
):

    value = _property(
        obj,
        name,
        default
    )

    if isinstance(
        value,
        bool
    ):
        return value

    if isinstance(
        value,
        str
    ):
        return value.strip().lower() in {
            "true",
            "1",
            "yes"
        }

    return bool(value)


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

    body_width = (
        220 * scale
    )

    body_height = (
        150 * scale
    )

    roof_height = (
        90 * scale
    )

    rectangle(
        t,
        x,
        y,
        body_width,
        body_height,
        fill=color
    )

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

    for index in range(
        windows
    ):

        wx = (
            x
            - body_width / 2
            + spacing * (index + 1)
        )

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

    if style == "victorian":

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


def draw_mountain(
    t,
    obj
):

    x = obj["x"]
    y = obj["y"]

    scale = obj["scale"]

    width_scale = _number_property(
        obj,
        "width_scale",
        1.0
    )

    height_scale = _number_property(
        obj,
        "height_scale",
        1.0
    )

    width = (
        220 * scale * width_scale
    )

    height = (
        170 * scale * height_scale
    )

    color = (
        obj["color"]
        if obj["color"] != "black"
        else "lightslategray"
    )

    snow_color = (
        obj.get(
            "secondary_color"
        )
        or "white"
    )

    points = [
        (
            x - width / 2,
            y - height / 2
        ),
        (
            x - width * 0.22,
            y + height * 0.03
        ),
        (
            x - width * 0.08,
            y + height * 0.23
        ),
        (
            x,
            y + height / 2
        ),
        (
            x + width * 0.12,
            y + height * 0.18
        ),
        (
            x + width * 0.24,
            y + height * 0.02
        ),
        (
            x + width / 2,
            y - height / 2
        )
    ]

    polygon(
        t,
        points,
        fill=color,
        outline=color
    )

    if _bool_property(
        obj,
        "snow_cap",
        scale >= 1
    ):

        snow_points = [
            (
                x - width * 0.14,
                y + height * 0.18
            ),
            (
                x,
                y + height / 2
            ),
            (
                x + width * 0.14,
                y + height * 0.17
            ),
            (
                x + width * 0.06,
                y + height * 0.15
            ),
            (
                x - width * 0.05,
                y + height * 0.14
            )
        ]

        polygon(
            t,
            snow_points,
            fill=snow_color,
            outline=snow_color
        )


def draw_hill(
    t,
    obj
):

    x = obj["x"]
    y = obj["y"]

    scale = obj["scale"]

    width = (
        260
        * scale
        * _number_property(
            obj,
            "width_scale",
            1.0
        )
    )

    height = (
        115
        * scale
        * _number_property(
            obj,
            "height_scale",
            1.0
        )
    )

    color = (
        obj["color"]
        if obj["color"] != "black"
        else "#7fb069"
    )

    points = [
        (
            x - width / 2,
            y - height / 2
        ),
        (
            x - width * 0.34,
            y + height * 0.05
        ),
        (
            x - width * 0.16,
            y + height * 0.28
        ),
        (
            x,
            y + height / 2
        ),
        (
            x + width * 0.18,
            y + height * 0.24
        ),
        (
            x + width * 0.34,
            y + height * 0.06
        ),
        (
            x + width / 2,
            y - height / 2
        )
    ]

    polygon(
        t,
        points,
        fill=color,
        outline=color
    )


def draw_river(
    t,
    obj
):

    x = obj["x"]
    y = obj["y"]

    scale = obj["scale"]

    bend = str(
        _property(
            obj,
            "bend",
            "right"
        )
    ).lower()

    if bend == "left":
        curve = -70 * scale
    elif bend == "center":
        curve = 0
    else:
        curve = 70 * scale

    width_scale = _number_property(
        obj,
        "width_scale",
        1.0
    )

    length_scale = _number_property(
        obj,
        "length_scale",
        1.0
    )

    length = (
        260 * scale * length_scale
    )

    top_y = (
        y + length / 2
    )

    upper_y = (
        y + length * 0.12
    )

    lower_y = (
        y - length * 0.16
    )

    bottom_y = (
        y - length / 2
    )

    top_x = (
        x - curve * 0.35
    )

    upper_x = (
        x + curve * 0.08
    )

    lower_x = (
        x + curve * 0.48
    )

    bottom_x = (
        x + curve * 0.82
    )

    top_half = (
        18 * scale * width_scale
    )

    upper_half = (
        28 * scale * width_scale
    )

    lower_half = (
        42 * scale * width_scale
    )

    bottom_half = (
        58 * scale * width_scale
    )

    left_bank = [
        (
            top_x - top_half,
            top_y
        ),
        (
            upper_x - upper_half,
            upper_y
        ),
        (
            lower_x - lower_half,
            lower_y
        ),
        (
            bottom_x - bottom_half,
            bottom_y
        )
    ]

    right_bank = [
        (
            bottom_x + bottom_half,
            bottom_y
        ),
        (
            lower_x + lower_half,
            lower_y
        ),
        (
            upper_x + upper_half,
            upper_y
        ),
        (
            top_x + top_half,
            top_y
        )
    ]

    water_color = (
        obj["color"]
        if obj["color"] != "black"
        else "dodgerblue"
    )

    highlight_color = (
        obj.get(
            "secondary_color"
        )
        or "lightblue"
    )

    polygon(
        t,
        left_bank + right_bank,
        fill=water_color,
        outline=water_color
    )

    inner_left = [
        (
            top_x - top_half * 0.45,
            top_y
        ),
        (
            upper_x - upper_half * 0.42,
            upper_y
        ),
        (
            lower_x - lower_half * 0.35,
            lower_y
        ),
        (
            bottom_x - bottom_half * 0.28,
            bottom_y
        )
    ]

    inner_right = [
        (
            bottom_x + bottom_half * 0.1,
            bottom_y
        ),
        (
            lower_x + lower_half * 0.12,
            lower_y
        ),
        (
            upper_x + upper_half * 0.18,
            upper_y
        ),
        (
            top_x + top_half * 0.2,
            top_y
        )
    ]

    polygon(
        t,
        inner_left + inner_right,
        fill=highlight_color,
        outline=highlight_color
    )


def draw_bush(
    t,
    obj
):

    x = obj["x"]
    y = obj["y"]

    scale = obj["scale"]

    color = (
        obj["color"]
        if obj["color"] != "black"
        else "forestgreen"
    )

    puff_count = _int_property(
        obj,
        "puffs",
        3,
        3,
        6
    )

    spread = (
        26 * scale
    )

    base_radius = (
        20 * scale
    )

    start = (
        -(puff_count - 1) / 2
    )

    for index in range(
        puff_count
    ):

        offset = (
            start + index
        ) * spread

        radius = (
            base_radius
            * (1 + (index % 2) * 0.18)
        )

        circle(
            t,
            x + offset,
            y + (
                4 * scale
                if index % 2
                else -4 * scale
            ),
            radius,
            fill=color,
            outline=color
        )


def draw_flower(
    t,
    obj
):

    x = obj["x"]
    y = obj["y"]

    scale = obj["scale"]

    petal_color = (
        obj["color"]
        if obj["color"] != "black"
        else "deeppink"
    )

    center_color = (
        obj.get(
            "secondary_color"
        )
        or "gold"
    )

    count = _int_property(
        obj,
        "count",
        5,
        1,
        8
    )

    spacing = (
        26 * scale
    )

    petal_radius = (
        3.5 * scale
    )

    start = (
        -(count - 1) / 2
    )

    for index in range(
        count
    ):

        fx = (
            x
            + (start + index) * spacing
        )

        stem_base_y = (
            y
            + (
                -5 * scale
                if index % 2
                else 4 * scale
            )
        )

        line(
            t,
            fx,
            stem_base_y,
            18 * scale,
            90,
            color="forestgreen",
            width=2
        )

        bloom_y = (
            stem_base_y
            + 18 * scale
        )

        for dx, dy in [
            (-4, 0),
            (4, 0),
            (0, -4),
            (0, 4)
        ]:

            circle(
                t,
                fx + dx * scale,
                bloom_y + dy * scale,
                petal_radius,
                fill=petal_color,
                outline=petal_color
            )

        circle(
            t,
            fx,
            bloom_y,
            2.3 * scale,
            fill=center_color,
            outline=center_color
        )


def draw_moon(
    t,
    obj
):

    x = obj["x"]
    y = obj["y"]

    scale = obj["scale"]

    radius = (
        32 * scale
    )

    moon_color = (
        obj["color"]
        if obj["color"] != "black"
        else "ivory"
    )

    circle(
        t,
        x,
        y,
        radius,
        fill=moon_color,
        outline=moon_color
    )

    cutout = obj.get(
        "secondary_color"
    )

    if cutout:

        circle(
            t,
            x + 12 * scale,
            y + 2 * scale,
            radius * 0.84,
            fill=cutout,
            outline=cutout
        )


def draw_star(
    t,
    obj
):

    x = obj["x"]
    y = obj["y"]

    scale = obj["scale"]

    color = (
        obj["color"]
        if obj["color"] != "black"
        else "lightyellow"
    )

    outer_radius = (
        14 * scale
    )

    inner_radius = (
        outer_radius * 0.45
    )

    points = []

    for index in range(10):

        radius = (
            outer_radius
            if index % 2 == 0
            else inner_radius
        )

        angle = math.radians(
            90 + index * 36
        )

        points.append(
            (
                x + math.cos(angle) * radius,
                y + math.sin(angle) * radius
            )
        )

    polygon(
        t,
        points,
        fill=color,
        outline=color
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
