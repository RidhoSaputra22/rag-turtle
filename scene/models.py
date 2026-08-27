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
    "mountain",
    "hill",
    "river",
    "bush",
    "flower",
    "moon",
    "star",
    "rectangle",
    "circle",
    "triangle",
    "line"
]

Position = Literal[
    "left",
    "center",
    "middle",
    "mid",
    "centre",
    "right",
    "center-left",
    "center-right",
    "middle-left",
    "middle-right",
    "mid-left",
    "mid-right",

    "top-left",
    "top",
    "top-center",
    "top-right",
    "upper-left",
    "upper-right",

    "bottom-left",
    "bottom",
    "bottom-center",
    "bottom-right",
    "lower-left",
    "lower-right"
]


Size = Literal[
    "small",
    "medium",
    "large"
]

Layer = Literal[
    "sky",
    "background",
    "midground",
    "foreground"
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


class PlanObject(BaseModel):
    type: ObjectType
    position: Position = "center"
    size: Size = "medium"
    color: str = "black"
    secondary_color: (
        str | None
    ) = None
    layer: Layer = "midground"
    reason: str = ""
    properties: dict[
        str,
        Any,
    ] = Field(
        default_factory=dict
    )


class SceneryPlan(BaseModel):
    expanded_prompt: str
    background: str = "white"
    atmosphere: str = "balanced"
    focus: str = "balanced landscape"
    composition_notes: List[
        str
    ] = Field(
        default_factory=list
    )
    planned_objects: List[
        PlanObject
    ]
