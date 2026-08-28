import re

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
    "lower-right": (260, -180),
}

SIZE_MAP = {
    "small": 0.65,
    "medium": 1.0,
    "large": 1.4,
}

LAYER_RANK = {
    "sky": 0,
    "background": 1,
    "midground": 2,
    "foreground": 3,
}

# Indonesian and descriptive colours that small models commonly use. Values
# stay in Turtle's named-colour/hex vocabulary, preventing a generated phrase
# such as "soft mountain blue" from crashing the renderer.
COLOR_MAP = {
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
    "ungu": "purple",
    "langit": "skyblue",
    "senja": "#f6b26b",
    "gelap": "#0f172a",
    "malam": "#0f172a",
    "dark": "#0f172a",
    "night": "#0f172a",
    "dark blue": "#172554",
    "dark navy": "#0f172a",
    "navy blue": "navy",
    "cream": "beige",
    "golden": "gold",
    "warm gold": "#ffd166",
    "light blue": "lightblue",
    "sky blue": "skyblue",
    "soft sky blue": "#87ceeb",
    "light gray": "lightgray",
    "dark gray": "dimgray",
    "blue gray": "slategray",
    "blue-grey": "slategray",
    "light green": "lightgreen",
    "dark green": "darkgreen",
    "forest green": "forestgreen",
    "meadow green": "#78b957",
    "leaf green": "#3d8b4d",
    "river blue": "dodgerblue",
    "snow white": "white",
}

SAFE_COLOR_NAMES = {
    "aliceblue", "antiquewhite", "aquamarine", "azure", "beige",
    "bisque", "black", "blue", "blueviolet", "brown", "burlywood",
    "cadetblue", "chartreuse", "chocolate", "coral", "cornflowerblue",
    "cornsilk", "crimson", "cyan", "darkblue", "darkcyan",
    "darkgoldenrod", "darkgray", "darkgreen", "darkkhaki", "darkmagenta",
    "darkolivegreen", "darkorange", "darkorchid", "darkred", "darksalmon",
    "darkseagreen", "darkslateblue", "darkslategray", "darkturquoise",
    "deeppink", "deepskyblue", "dimgray", "dodgerblue", "firebrick",
    "forestgreen", "gainsboro", "gold", "goldenrod", "gray", "green",
    "greenyellow", "honeydew", "hotpink", "indianred", "indigo", "ivory",
    "khaki", "lavender", "lawngreen", "lemonchiffon", "lightblue",
    "lightcoral", "lightcyan", "lightgoldenrodyellow", "lightgray",
    "lightgreen", "lightpink", "lightsalmon", "lightseagreen",
    "lightskyblue", "lightslategray", "lightsteelblue", "lightyellow",
    "limegreen", "linen", "magenta", "maroon", "mediumaquamarine",
    "mediumblue", "mediumorchid", "mediumpurple", "mediumseagreen",
    "mediumslateblue", "mediumspringgreen", "mediumturquoise",
    "mediumvioletred", "midnightblue", "mintcream", "mistyrose",
    "moccasin", "navajowhite", "navy", "oldlace", "olive", "olivedrab",
    "orange", "orangered", "orchid", "palegoldenrod", "palegreen",
    "paleturquoise", "palevioletred", "papayawhip", "peachpuff", "peru",
    "pink", "plum", "powderblue", "purple", "red", "rosybrown",
    "royalblue", "saddlebrown", "salmon", "sandybrown", "seagreen",
    "seashell", "sienna", "silver", "skyblue", "slateblue", "slategray",
    "snow", "springgreen", "steelblue", "tan", "teal", "thistle",
    "tomato", "turquoise", "violet", "wheat", "white", "whitesmoke",
    "yellow", "yellowgreen",
}

DEFAULT_OBJECT_COLORS = {
    "bush": "forestgreen",
    "cloud": "white",
    "flower": "deeppink",
    "hill": "#82b965",
    "house": "beige",
    "meadow": "#78b957",
    "moon": "ivory",
    "mountain": "slategray",
    "path": "#d2b48c",
    "river": "dodgerblue",
    "star": "lightyellow",
    "sun": "gold",
    "tree": "forestgreen",
}

COMMON_PROPERTIES = {
    "offset_x",
    "offset_y",
    "scale_multiplier",
}

OBJECT_PROPERTIES = {
    "bush": {"puffs"},
    "cloud": {"puffs"},
    "flower": {"count"},
    "hill": {"width_scale", "height_scale"},
    "house": {"windows", "chimney", "style"},
    "meadow": {"width_scale", "height_scale"},
    "mountain": {
        "snow_cap", "width_scale", "height_scale", "shadow_color",
    },
    "path": {"bend", "width_scale", "length_scale"},
    "river": {"bend", "width_scale", "length_scale"},
    "tree": {"trunk_color"},
}

NUMBER_LIMITS = {
    "offset_x": (-420.0, 420.0),
    "offset_y": (-300.0, 300.0),
    "scale_multiplier": (0.35, 2.0),
    "width_scale": (0.4, 2.2),
    "height_scale": (0.4, 2.2),
    "length_scale": (0.4, 2.2),
    "puffs": (3, 6),
    "count": (1, 8),
    "windows": (1, 6),
}

HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")


def normalize_color(
    color: str | None,
    fallback: str | None = None,
) -> str | None:
    """Translate natural-language colours and keep only safe Turtle values."""

    if color is None:
        return fallback

    candidate = COLOR_MAP.get(
        color.strip().lower(),
        color.strip().lower(),
    )

    if HEX_COLOR.fullmatch(candidate) or candidate in SAFE_COLOR_NAMES:
        return candidate

    return fallback


def _number_property(
    properties,
    name,
    default,
):
    value = properties.get(name, default)

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _clamp(
    value,
    minimum,
    maximum,
):
    return max(minimum, min(value, maximum))


def _normalize_properties(obj):
    """Keep the compact JSON contract predictable before drawing it."""

    source = dict(obj.properties)
    allowed = COMMON_PROPERTIES | OBJECT_PROPERTIES.get(obj.type, set())
    normalized = {}

    for name in allowed:
        if name not in source:
            continue

        value = source[name]

        if name in NUMBER_LIMITS:
            minimum, maximum = NUMBER_LIMITS[name]
            value = _clamp(
                _number_property(source, name, minimum),
                minimum,
                maximum,
            )

            if name in {"puffs", "count", "windows"}:
                value = int(value)

        elif name == "chimney" or name == "snow_cap":
            if isinstance(value, str):
                value = value.strip().lower() in {
                    "true",
                    "1",
                    "yes",
                }
            else:
                value = bool(value)

        elif name == "bend":
            value = str(value).lower()
            if value not in {"left", "center", "right"}:
                continue

        elif name == "style":
            value = str(value).lower()
            if value not in {"basic", "victorian"}:
                continue

        elif name in {"shadow_color", "trunk_color"}:
            value = normalize_color(value)
            if value is None:
                continue

        normalized[name] = value

    return normalized


def normalize_scene(scene: Scene):
    normalized_objects = []

    for obj in scene.objects:
        properties = _normalize_properties(obj)
        x, y = POSITION_MAP[obj.position]
        scale = SIZE_MAP[obj.size] * _number_property(
            properties,
            "scale_multiplier",
            1.0,
        )

        x += _number_property(properties, "offset_x", 0.0)
        y += _number_property(properties, "offset_y", 0.0)

        normalized_objects.append({
            **obj.model_dump(),
            "color": normalize_color(
                obj.color,
                DEFAULT_OBJECT_COLORS.get(obj.type, "black"),
            ),
            "secondary_color": normalize_color(obj.secondary_color),
            "properties": properties,
            "x": x,
            "y": y,
            "scale": scale,
        })

    # Stable sorting preserves the model's order inside each visual layer.
    normalized_objects.sort(
        key=lambda obj: LAYER_RANK.get(obj["layer"], 2)
    )

    return {
        "background": normalize_color(scene.background, "white"),
        "objects": normalized_objects,
    }
