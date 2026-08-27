from scene.models import Scene


POSITION_MAP = {
    "left": (-260, 0),
    "center": (0, 0),
    "middle": (0, 0),
    "mid": (0, 0),
    "centre": (0, 0),
    "right": (260, 0),
    "center-left": (-260, 0),
    "center-right": (260, 0),
    "middle-left": (-260, 0),
    "middle-right": (260, 0),
    "mid-left": (-260, 0),
    "mid-right": (260, 0),

    "top-left": (-260, 180),
    "top": (0, 180),
    "top-center": (0, 180),
    "top-right": (260, 180),
    "upper-left": (-260, 180),
    "upper-right": (260, 180),

    "bottom-left": (-260, -180),
    "bottom": (0, -180),
    "bottom-center": (0, -180),
    "bottom-right": (260, -180),
    "lower-left": (-260, -180),
    "lower-right": (260, -180)
}

SIZE_MAP = {
    "small": 0.65,
    "medium": 1.0,
    "large": 1.4
}

COLOR_MAP = {
    # Indonesian
    "krem": "beige",
    "merah": "red",
    "biru": "blue",
    "biru muda": "lightblue",
    "kuning": "yellow",
    "hijau": "green",
    "hijau muda": "lightgreen",
    "hijau tua": "darkgreen",
    "coklat": "brown",
    "hitam": "black",
    "putih": "white",
    "abu-abu": "gray",
    "abu abu": "gray",
    "merah muda": "pink",
    "oranye": "orange",
    "langit": "skyblue",

    # Semantic colors
    "dark": "#0f172a",
    "night": "#0f172a",
    "dark blue": "#172554",
    "dark navy": "#0f172a",
    "navy blue": "navy",

    "cream": "beige",
    "golden": "gold",
    "light blue": "lightblue",
    "sky blue": "skyblue",
    "light gray": "lightgray",
    "dark gray": "dimgray",
    "light green": "lightgreen",
    "dark green": "darkgreen",
}


def normalize_color(color: str | None) -> str | None:
    if color is None:
        return None

    color = color.strip().lower()

    return COLOR_MAP.get(
        color,
        color
    )


def _number_property(
    properties,
    name,
    default
):

    value = properties.get(
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


def normalize_scene(scene: Scene):

    normalized_objects = []

    for obj in scene.objects:

        properties = dict(
            obj.properties
        )

        x, y = POSITION_MAP[obj.position]
        scale = (
            SIZE_MAP[obj.size]
            * _number_property(
                properties,
                "scale_multiplier",
                1.0
            )
        )

        x += _number_property(
            properties,
            "offset_x",
            0.0
        )

        y += _number_property(
            properties,
            "offset_y",
            0.0
        )

        normalized_objects.append({
            **obj.model_dump(),
            "color": normalize_color(obj.color),
            "secondary_color": normalize_color(obj.secondary_color),
            "x": x,
            "y": y,
            "scale": scale
        })

    return {
        "background": normalize_color(scene.background) or "white",
        "objects": normalized_objects
    }
