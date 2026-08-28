import math

from renderer.primitives import (
    circle,
    line,
    polygon,
    rectangle,
)


def _property(
    obj,
    name,
    default=None,
):
    return obj.get("properties", {}).get(name, default)


def _number_property(
    obj,
    name,
    default,
):
    try:
        return float(_property(obj, name, default))
    except (TypeError, ValueError):
        return default


def _int_property(
    obj,
    name,
    default,
    minimum,
    maximum,
):
    try:
        value = int(_property(obj, name, default))
    except (TypeError, ValueError):
        value = default

    return max(minimum, min(value, maximum))


def _bool_property(
    obj,
    name,
    default=False,
):
    value = _property(obj, name, default)

    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}

    return bool(value)


def _color(
    obj,
    fallback,
):
    return obj.get("color") or fallback


def draw_house(
    t,
    obj,
):
    x = obj["x"]
    y = obj["y"]
    scale = obj["scale"]
    wall_color = _color(obj, "beige")
    roof_color = obj.get("secondary_color") or "firebrick"
    style = _property(obj, "style", "basic")
    windows = _int_property(obj, "windows", 2, 1, 6)

    body_width = 205 * scale
    body_height = 138 * scale
    roof_height = (108 if style == "victorian" else 84) * scale
    roof_bottom = y + body_height / 2

    rectangle(t, x, y, body_width, body_height, fill=wall_color)
    polygon(
        t,
        [
            (x - body_width / 2 - 9 * scale, roof_bottom),
            (x, roof_bottom + roof_height),
            (x + body_width / 2 + 9 * scale, roof_bottom),
        ],
        fill=roof_color,
    )

    door_width = 36 * scale
    door_height = 67 * scale
    door_y = y - body_height / 2 + door_height / 2
    rectangle(t, x, door_y, door_width, door_height, fill="saddlebrown")
    circle(
        t,
        x + door_width * 0.28,
        door_y,
        2.2 * scale,
        fill="gold",
    )

    spacing = body_width / (windows + 1)
    for index in range(windows):
        window_x = x - body_width / 2 + spacing * (index + 1)

        if abs(window_x - x) < door_width * 0.95:
            continue

        window_width = 29 * scale
        window_height = 35 * scale
        window_y = y + 16 * scale
        rectangle(
            t,
            window_x,
            window_y,
            window_width,
            window_height,
            fill="lightblue",
        )
        line(
            t,
            window_x,
            window_y - window_height / 2,
            window_height,
            90,
            color="white",
            width=1,
        )
        line(
            t,
            window_x - window_width / 2,
            window_y,
            window_width,
            color="white",
            width=1,
        )

    if _bool_property(obj, "chimney", False):
        rectangle(
            t,
            x + body_width * 0.29,
            roof_bottom + roof_height * 0.52,
            23 * scale,
            62 * scale,
            fill="firebrick",
        )

    if style == "victorian":
        circle(
            t,
            x,
            roof_bottom + roof_height * 0.39,
            13 * scale,
            fill="lightyellow",
        )
        line(
            t,
            x - body_width / 2,
            y + body_height * 0.24,
            body_width,
            color="peru",
            width=2,
        )


def draw_tree(
    t,
    obj,
):
    x = obj["x"]
    y = obj["y"]
    scale = obj["scale"]
    leaf_color = _color(obj, "forestgreen")
    highlight_color = obj.get("secondary_color") or "#5fae5d"
    trunk_color = _property(obj, "trunk_color", "saddlebrown")
    trunk_height = 98 * scale
    canopy_y = y + trunk_height * 0.77
    radius = 51 * scale

    # Fine branches keep the trunk connected to the foliage instead of looking
    # like a plain rectangle beneath three circles.
    line(
        t,
        x,
        y + trunk_height * 0.28,
        43 * scale,
        118,
        color=trunk_color,
        width=max(2, int(5 * scale)),
    )
    line(
        t,
        x,
        y + trunk_height * 0.38,
        40 * scale,
        58,
        color=trunk_color,
        width=max(2, int(4 * scale)),
    )
    rectangle(t, x, y, 27 * scale, trunk_height, fill=trunk_color)

    for cx, cy, radius_multiplier in [
        (x, canopy_y + 8 * scale, 1.0),
        (x - 34 * scale, canopy_y - 5 * scale, 0.78),
        (x + 36 * scale, canopy_y - 6 * scale, 0.76),
        (x - 4 * scale, canopy_y + 35 * scale, 0.66),
    ]:
        circle(
            t,
            cx,
            cy,
            radius * radius_multiplier,
            fill=leaf_color,
        )

    circle(
        t,
        x - 16 * scale,
        canopy_y + 25 * scale,
        radius * 0.3,
        fill=highlight_color,
    )


def draw_sun(
    t,
    obj,
):
    x = obj["x"]
    y = obj["y"]
    scale = obj["scale"]
    color = _color(obj, "gold")
    radius = 38 * scale

    for angle in range(0, 360, 30):
        line(
            t,
            x,
            y,
            66 * scale,
            angle,
            color=color,
            width=max(1, int(2 * scale)),
        )

    circle(t, x, y, radius, fill=color)
    circle(t, x - 10 * scale, y + 11 * scale, radius * 0.24, fill="#fff1a8")


def draw_cloud(
    t,
    obj,
):
    x = obj["x"]
    y = obj["y"]
    scale = obj["scale"]
    color = _color(obj, "white")
    shade = obj.get("secondary_color") or "#d9edf5"

    for cx, cy, radius in [
        (x, y - 4 * scale, 34 * scale),
        (x - 34 * scale, y - 10 * scale, 26 * scale),
        (x + 35 * scale, y - 11 * scale, 27 * scale),
    ]:
        circle(t, cx, cy - 5 * scale, radius, fill=shade)

    for cx, cy, radius in [
        (x, y + 3 * scale, 34 * scale),
        (x - 34 * scale, y - 4 * scale, 26 * scale),
        (x + 35 * scale, y - 5 * scale, 27 * scale),
    ]:
        circle(t, cx, cy, radius, fill=color)


def draw_mountain(
    t,
    obj,
):
    x = obj["x"]
    y = obj["y"]
    scale = obj["scale"]
    width = 220 * scale * _number_property(obj, "width_scale", 1.0)
    height = 170 * scale * _number_property(obj, "height_scale", 1.0)
    color = _color(obj, "slategray")
    snow_color = obj.get("secondary_color") or "white"
    shadow_color = _property(obj, "shadow_color", "#637989")

    peak = (x, y + height / 2)
    left_base = (x - width / 2, y - height / 2)
    right_base = (x + width / 2, y - height / 2)
    polygon(
        t,
        [
            left_base,
            (x - width * 0.23, y + height * 0.02),
            (x - width * 0.09, y + height * 0.22),
            peak,
            (x + width * 0.13, y + height * 0.17),
            (x + width * 0.25, y + height * 0.01),
            right_base,
        ],
        fill=color,
    )
    polygon(
        t,
        [
            peak,
            (x + width * 0.13, y + height * 0.17),
            (x + width * 0.25, y + height * 0.01),
            right_base,
            (x + width * 0.06, y - height * 0.16),
        ],
        fill=shadow_color,
    )

    if _bool_property(obj, "snow_cap", scale >= 1):
        polygon(
            t,
            [
                (x - width * 0.14, y + height * 0.18),
                peak,
                (x + width * 0.14, y + height * 0.17),
                (x + width * 0.06, y + height * 0.13),
                (x - width * 0.04, y + height * 0.14),
            ],
            fill=snow_color,
        )


def draw_meadow(
    t,
    obj,
):
    """Draw an explicit ground plane with a soft, rolling horizon."""

    x = obj["x"]
    y = obj["y"]
    scale = obj["scale"]
    width = 760 * scale * _number_property(obj, "width_scale", 1.0)
    height = 205 * scale * _number_property(obj, "height_scale", 1.0)
    color = _color(obj, "#78b957")
    highlight = obj.get("secondary_color") or "#9fd278"
    left = x - width / 2
    right = x + width / 2
    bottom = y - height / 2
    top = y + height / 2

    polygon(
        t,
        [
            (left, bottom),
            (left, top - height * 0.13),
            (x - width * 0.28, top - height * 0.02),
            (x, top - height * 0.12),
            (x + width * 0.28, top + height * 0.04),
            (right, top - height * 0.1),
            (right, bottom),
        ],
        fill=color,
    )
    polygon(
        t,
        [
            (left, top - height * 0.13),
            (x - width * 0.28, top - height * 0.02),
            (x, top - height * 0.12),
            (x + width * 0.28, top + height * 0.04),
            (right, top - height * 0.1),
            (right, top - height * 0.18),
            (x + width * 0.24, top - height * 0.04),
            (x - width * 0.05, top - height * 0.2),
            (x - width * 0.32, top - height * 0.09),
            (left, top - height * 0.2),
        ],
        fill=highlight,
    )


def draw_hill(
    t,
    obj,
):
    x = obj["x"]
    y = obj["y"]
    scale = obj["scale"]
    width = 260 * scale * _number_property(obj, "width_scale", 1.0)
    height = 115 * scale * _number_property(obj, "height_scale", 1.0)
    color = _color(obj, "#82b965")

    polygon(
        t,
        [
            (x - width / 2, y - height / 2),
            (x - width * 0.34, y + height * 0.05),
            (x - width * 0.16, y + height * 0.28),
            (x, y + height / 2),
            (x + width * 0.18, y + height * 0.24),
            (x + width * 0.34, y + height * 0.06),
            (x + width / 2, y - height / 2),
        ],
        fill=color,
    )


def _winding_banks(
    x,
    y,
    scale,
    bend,
    width_scale,
    length_scale,
    top_half,
    bottom_half,
):
    curve_direction = {"left": -1, "center": 0, "right": 1}.get(bend, 1)
    curve = curve_direction * 70 * scale
    length = 260 * scale * length_scale
    top_y = y + length / 2
    upper_y = y + length * 0.12
    lower_y = y - length * 0.16
    bottom_y = y - length / 2
    top_x = x - curve * 0.35
    upper_x = x + curve * 0.08
    lower_x = x + curve * 0.48
    bottom_x = x + curve * 0.82
    upper_half = top_half * 1.55
    lower_half = top_half * 2.3
    bottom_half = bottom_half * width_scale

    left_bank = [
        (top_x - top_half, top_y),
        (upper_x - upper_half, upper_y),
        (lower_x - lower_half, lower_y),
        (bottom_x - bottom_half, bottom_y),
    ]
    right_bank = [
        (bottom_x + bottom_half, bottom_y),
        (lower_x + lower_half, lower_y),
        (upper_x + upper_half, upper_y),
        (top_x + top_half, top_y),
    ]
    return left_bank, right_bank


def draw_river(
    t,
    obj,
):
    x = obj["x"]
    y = obj["y"]
    scale = obj["scale"]
    bend = str(_property(obj, "bend", "right")).lower()
    width_scale = _number_property(obj, "width_scale", 1.0)
    length_scale = _number_property(obj, "length_scale", 1.0)
    water_color = _color(obj, "dodgerblue")
    highlight_color = obj.get("secondary_color") or "#9ddcf5"
    left_bank, right_bank = _winding_banks(
        x,
        y,
        scale,
        bend,
        width_scale,
        length_scale,
        18 * scale * width_scale,
        58 * scale,
    )
    polygon(t, left_bank + right_bank, fill=water_color)

    inner_left = [
        (left_bank[0][0] + 10 * scale, left_bank[0][1]),
        (left_bank[1][0] + 16 * scale, left_bank[1][1]),
        (left_bank[2][0] + 24 * scale, left_bank[2][1]),
        (left_bank[3][0] + 35 * scale, left_bank[3][1]),
    ]
    inner_right = [
        (right_bank[0][0] - 27 * scale, right_bank[0][1]),
        (right_bank[1][0] - 19 * scale, right_bank[1][1]),
        (right_bank[2][0] - 13 * scale, right_bank[2][1]),
        (right_bank[3][0] - 8 * scale, right_bank[3][1]),
    ]
    polygon(t, inner_left + inner_right, fill=highlight_color)


def draw_path(
    t,
    obj,
):
    x = obj["x"]
    y = obj["y"]
    scale = obj["scale"]
    bend = str(_property(obj, "bend", "center")).lower()
    width_scale = _number_property(obj, "width_scale", 1.0)
    length_scale = _number_property(obj, "length_scale", 1.0)
    path_color = _color(obj, "#d2b48c")
    highlight_color = obj.get("secondary_color") or "#ecd9ad"
    left_edge, right_edge = _winding_banks(
        x,
        y,
        scale,
        bend,
        width_scale,
        length_scale,
        10 * scale * width_scale,
        45 * scale,
    )
    polygon(t, left_edge + right_edge, fill=path_color)

    center_left = []
    center_right = []

    for left, right in zip(left_edge, reversed(right_edge)):
        center_left.append((
            left[0] + (right[0] - left[0]) * 0.42,
            left[1],
        ))
        center_right.append((
            left[0] + (right[0] - left[0]) * 0.58,
            left[1],
        ))

    polygon(
        t,
        center_left + list(reversed(center_right)),
        fill=highlight_color,
    )


def draw_bush(
    t,
    obj,
):
    x = obj["x"]
    y = obj["y"]
    scale = obj["scale"]
    color = _color(obj, "forestgreen")
    highlight = obj.get("secondary_color") or "#5fae5d"
    puff_count = _int_property(obj, "puffs", 4, 3, 6)
    spread = 25 * scale
    base_radius = 20 * scale
    start = -(puff_count - 1) / 2

    for index in range(puff_count):
        offset = (start + index) * spread
        radius = base_radius * (1 + (index % 2) * 0.17)
        circle(
            t,
            x + offset,
            y + (4 * scale if index % 2 else -4 * scale),
            radius,
            fill=color,
        )

    circle(t, x - spread * 0.28, y + 10 * scale, base_radius * 0.36, fill=highlight)


def draw_flower(
    t,
    obj,
):
    x = obj["x"]
    y = obj["y"]
    scale = obj["scale"]
    petal_color = _color(obj, "deeppink")
    center_color = obj.get("secondary_color") or "gold"
    count = _int_property(obj, "count", 5, 1, 8)
    spacing = 25 * scale
    start = -(count - 1) / 2

    for index in range(count):
        flower_x = x + (start + index) * spacing
        stem_y = y + (-5 * scale if index % 2 else 4 * scale)
        line(t, flower_x, stem_y, 19 * scale, 90, color="forestgreen", width=2)
        line(t, flower_x, stem_y + 8 * scale, 8 * scale, 150, color="forestgreen", width=1)
        bloom_y = stem_y + 19 * scale

        for dx, dy in [(-4, 0), (4, 0), (0, -4), (0, 4)]:
            circle(
                t,
                flower_x + dx * scale,
                bloom_y + dy * scale,
                3.8 * scale,
                fill=petal_color,
            )

        circle(t, flower_x, bloom_y, 2.2 * scale, fill=center_color)


def draw_moon(
    t,
    obj,
):
    x = obj["x"]
    y = obj["y"]
    scale = obj["scale"]
    radius = 32 * scale
    moon_color = _color(obj, "ivory")
    circle(t, x, y, radius, fill=moon_color)

    if cutout := obj.get("secondary_color"):
        circle(t, x + 12 * scale, y + 2 * scale, radius * 0.84, fill=cutout)


def draw_star(
    t,
    obj,
):
    x = obj["x"]
    y = obj["y"]
    scale = obj["scale"]
    color = _color(obj, "lightyellow")
    outer_radius = 14 * scale
    inner_radius = outer_radius * 0.45
    points = []

    for index in range(10):
        radius = outer_radius if index % 2 == 0 else inner_radius
        angle = math.radians(90 + index * 36)
        points.append((
            x + math.cos(angle) * radius,
            y + math.sin(angle) * radius,
        ))

    polygon(t, points, fill=color)


def draw_basic_object(
    t,
    obj,
):
    obj_type = obj["type"]
    x = obj["x"]
    y = obj["y"]
    scale = obj["scale"]
    color = obj["color"]

    if obj_type == "rectangle":
        rectangle(t, x, y, 120 * scale, 80 * scale, fill=color)
    elif obj_type == "circle":
        circle(t, x, y, 50 * scale, fill=color)
    elif obj_type == "triangle":
        size = 100 * scale
        polygon(
            t,
            [
                (x, y + size / 2),
                (x - size / 2, y - size / 2),
                (x + size / 2, y - size / 2),
            ],
            fill=color,
        )
    elif obj_type == "line":
        line(t, x, y, 120 * scale, color=color)
