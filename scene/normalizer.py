from scene.models import Scene


POSITION_MAP = {
    "left": (-260, 0),
    "center": (0, 0),
    "right": (260, 0),

    "top-left": (-260, 180),
    "top": (0, 180),
    "top-right": (260, 180),

    "bottom-left": (-260, -180),
    "bottom": (0, -180),
    "bottom-right": (260, -180)
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
    "kuning": "yellow",
    "hijau": "green",
    "coklat": "brown",
    "hitam": "black",
    "putih": "white",
    "abu-abu": "gray",

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
}


def normalize_color(color: str | None) -> str | None:
    if color is None:
        return None

    color = color.strip().lower()

    return COLOR_MAP.get(
        color,
        color
    )

def normalize_scene(scene: Scene):

    normalized_objects = []

    for obj in scene.objects:

        x, y = POSITION_MAP[obj.position]
        scale = SIZE_MAP[obj.size]

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