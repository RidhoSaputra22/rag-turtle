"""
File ini dimaksudkan agar model yang menghasilkan tipe dari tipe yang di tentukan
langsung di tolak
"""



from typing import (
    Any,
    List,
    Literal
)

from pydantic import (
    BaseModel,
    Field
)

ObjectType = Literal[
    "house",
    "tree",
    "sun",
    "cloud",
    "rectangle",
    "circle",
    "triangle",
    "line"
]

Position = Literal[
    "left",
    "center",
    "right",

    "top-left",
    "top",
    "top-right",

    "bottom-left",
    "bottom",
    "bottom-right"
]


Size = Literal[
    "small",
    "medium",
    "large"
]


class SceneObject(BaseModel):
    type : ObjectType
    position: Position = "center"
    size: Size = "medium"
    color: str = "black"

    secondary_color: (
        str | None
    ) = None

    properties: dict[
        str,
        Any,
    ] = Field(
        default_factory=dict
    )

class Scene(BaseModel):
    
    background: str = "white"
    objects: List[
        SceneObject
    ]