from dataclasses import dataclass
import re
from typing import Any

from pydantic import (
    ValidationError
)

from config import (
    DEBUG_MODE,
    MAX_RETRIES,
    PLAN_SKILL_PATH,
    SKILL_PATH
)
from llm.ollama_provider import (
    OllamaProvider
)
from rag.retriever import (
    Retriever
)
from scene.models import (
    PlanObject,
    Scene,
    SceneObject,
    SceneryPlan
)
from utils.debug_mode import Debug


debug = Debug(
    DEBUG_MODE
)

REQUESTED_OBJECT_KEYWORDS = {
    "house": [
        "house",
        "rumah",
        "home"
    ],
    "tree": [
        "tree",
        "trees",
        "pohon"
    ],
    "sun": [
        "sun",
        "matahari"
    ],
    "cloud": [
        "cloud",
        "clouds",
        "awan"
    ],
    "mountain": [
        "mountain",
        "mountains",
        "gunung"
    ],
    "hill": [
        "hill",
        "hills",
        "bukit"
    ],
    "river": [
        "river",
        "sungai",
        "stream"
    ],
    "bush": [
        "bush",
        "bushes",
        "semak"
    ],
    "flower": [
        "flower",
        "flowers",
        "bunga"
    ],
    "moon": [
        "moon",
        "bulan"
    ],
    "star": [
        "star",
        "stars",
        "bintang"
    ],
}


@dataclass
class PipelineResult:
    plan: SceneryPlan
    scene: Scene
    hits: list[dict[str, Any]]
    plan_response: Any
    scene_response: Any


class TurtlePipeline:
    def __init__(self):
        self.llm = (
            OllamaProvider()
        )

        self.retriever = (
            Retriever()
        )

        self.skill = (
            SKILL_PATH.read_text(
                encoding="utf-8"
            )
        )

        self.plan_skill = (
            PLAN_SKILL_PATH.read_text(
                encoding="utf-8"
            )
        )

    def _emit_status(
        self,
        on_status,
        message
    ):

        if on_status:
            on_status(
                message
            )

        debug.save_on_file(
            message=f"# status\n{message}\n"
        )

    def _emit_chunk(
        self,
        on_chunk,
        label
    ):

        if on_chunk is None:
            return None

        def writer(
            content
        ):
            on_chunk(
                label,
                content
            )

        return writer

    def _summarize_hits(
        self,
        hits
    ):

        if not hits:
            return (
                "Tidak ada knowledge yang cocok."
            )

        labels = []

        for hit in hits:
            labels.append(
                hit["metadata"][
                    "source"
                ]
            )

        return ", ".join(
            labels
        )

    def _build_context(
        self,
        hits
    ):

        if not hits:
            return (
                "No relevant drawing knowledge found."
            )

        context = []

        for index, hit in enumerate(
            hits,
            start=1
        ):
            context.append(
                f"""
RECIPE {index}:
{hit["context"]}
"""
            )

        return "\n".join(
            context
        )

    def _clean_json(
        self,
        text
    ):

        text = text.strip()

        if text.startswith(
            "```"
        ):

            lines = (
                text.splitlines()
            )

            lines = lines[1:]

            if (
                lines
                and lines[-1].startswith(
                    "```"
                )
            ):
                lines = lines[:-1]

            text = "\n".join(
                lines
            )

        start = text.find(
            "{"
        )

        end = text.rfind(
            "}"
        )

        if (
            start != -1
            and end != -1
        ):
            text = text[
                start:end + 1
            ]

        return text

    def _serialize_plan(
        self,
        plan
    ):

        return plan.model_dump_json(
            indent=2
        )

    def _extract_requested_types(
        self,
        user_request
    ):

        lowered = user_request.lower()

        tokens = set(
            re.findall(
                r"[\w-]+",
                lowered
            )
        )

        requested = set()

        for obj_type, keywords in (
            REQUESTED_OBJECT_KEYWORDS.items()
        ):
            if any(
                keyword in tokens
                for keyword in keywords
            ):
                requested.add(
                    obj_type
                )

        return requested

    def _missing_requested_types(
        self,
        user_request,
        objects
    ):

        requested = (
            self._extract_requested_types(
                user_request
            )
        )

        present = {
            obj.type
            for obj in objects
        }

        return sorted(
            requested - present
        )

    def _layer_rank(
        self,
        layer
    ):

        ranks = {
            "sky": 0,
            "background": 1,
            "midground": 2,
            "foreground": 3,
        }

        return ranks.get(
            layer,
            2
        )

    def _default_plan_object(
        self,
        obj_type,
        background
    ):

        defaults = {
            "house": {
                "position": "center",
                "size": "medium",
                "color": "beige",
                "secondary_color": "red",
                "layer": "midground",
                "reason": "Memenuhi objek rumah yang diminta user.",
                "properties": {
                    "windows": 2,
                    "chimney": True,
                    "style": "basic",
                },
            },
            "mountain": {
                "position": "top-left",
                "size": "large",
                "color": "lightgray",
                "secondary_color": "white",
                "layer": "background",
                "reason": "Memenuhi elemen gunung yang diminta user.",
                "properties": {
                    "offset_x": 80,
                    "offset_y": -20,
                    "snow_cap": True,
                    "width_scale": 1.1,
                },
            },
            "river": {
                "position": "left",
                "size": "large",
                "color": "dodgerblue",
                "secondary_color": "lightblue",
                "layer": "midground",
                "reason": "Memenuhi elemen sungai yang diminta user.",
                "properties": {
                    "offset_x": -60,
                    "offset_y": -60,
                    "bend": "right",
                    "length_scale": 1.3,
                },
            },
            "hill": {
                "position": "bottom-right",
                "size": "large",
                "color": "yellowgreen",
                "secondary_color": None,
                "layer": "midground",
                "reason": "Memenuhi elemen bukit yang diminta user.",
                "properties": {
                    "offset_x": -80,
                    "offset_y": 30,
                    "width_scale": 1.2,
                },
            },
            "tree": {
                "position": "bottom-left",
                "size": "medium",
                "color": "green",
                "secondary_color": None,
                "layer": "midground",
                "reason": "Memenuhi elemen pohon yang diminta user.",
                "properties": {
                    "offset_x": 120,
                    "offset_y": 70,
                },
            },
            "flower": {
                "position": "bottom-right",
                "size": "small",
                "color": "pink",
                "secondary_color": "yellow",
                "layer": "foreground",
                "reason": "Memenuhi elemen bunga yang diminta user.",
                "properties": {
                    "offset_x": -10,
                    "offset_y": 10,
                    "count": 5,
                },
            },
            "bush": {
                "position": "bottom-right",
                "size": "small",
                "color": "forestgreen",
                "secondary_color": None,
                "layer": "foreground",
                "reason": "Menambah semak pendukung di foreground.",
                "properties": {
                    "offset_x": 60,
                    "offset_y": 20,
                    "puffs": 4,
                },
            },
            "sun": {
                "position": "top-right",
                "size": "medium",
                "color": "gold",
                "secondary_color": None,
                "layer": "sky",
                "reason": "Memenuhi elemen matahari yang diminta user.",
                "properties": {
                    "offset_x": -20,
                    "offset_y": 10,
                },
            },
            "cloud": {
                "position": "top-right",
                "size": "medium",
                "color": "white",
                "secondary_color": None,
                "layer": "sky",
                "reason": "Menambah keseimbangan pada area langit.",
                "properties": {
                    "offset_x": -90,
                    "offset_y": -10,
                },
            },
            "moon": {
                "position": "top-right",
                "size": "medium",
                "color": "ivory",
                "secondary_color": background,
                "layer": "sky",
                "reason": "Memenuhi elemen bulan yang diminta user.",
                "properties": {
                    "offset_x": -30,
                    "offset_y": 10,
                },
            },
            "star": {
                "position": "top",
                "size": "small",
                "color": "lightyellow",
                "secondary_color": None,
                "layer": "sky",
                "reason": "Memenuhi elemen bintang yang diminta user.",
                "properties": {
                    "offset_y": 30,
                },
            },
        }

        payload = defaults.get(
            obj_type,
            {
                "position": "center",
                "size": "medium",
                "color": "gray",
                "secondary_color": None,
                "layer": "midground",
                "reason": "Objek pendukung hasil fallback.",
                "properties": {},
            }
        )

        return PlanObject(
            type=obj_type,
            **payload
        )

    def _augment_plan(
        self,
        user_request,
        plan
    ):

        missing_types = (
            self._missing_requested_types(
                user_request,
                plan.planned_objects
            )
        )

        if not missing_types:
            return plan, []

        planned_objects = list(
            plan.planned_objects
        )

        for obj_type in missing_types:
            planned_objects.append(
                self._default_plan_object(
                    obj_type,
                    plan.background
                )
            )

        planned_objects.sort(
            key=lambda obj: (
                self._layer_rank(
                    obj.layer
                ),
                obj.position,
            )
        )

        return (
            SceneryPlan(
                **{
                    **plan.model_dump(),
                    "planned_objects": [
                        obj.model_dump()
                        for obj in planned_objects
                    ],
                }
            ),
            missing_types,
        )

    def _plan_object_to_scene_object(
        self,
        plan_object
    ):

        return SceneObject(
            **{
                key: value
                for key, value in (
                    plan_object.model_dump().items()
                )
                if key not in {
                    "layer",
                    "reason",
                }
            }
        )

    def _augment_scene(
        self,
        user_request,
        plan,
        scene
    ):

        missing_types = (
            self._missing_requested_types(
                user_request,
                scene.objects
            )
        )

        if not missing_types:
            return scene, []

        scene_objects = list(
            scene.objects
        )

        planned_by_type = {}

        for plan_object in plan.planned_objects:
            planned_by_type.setdefault(
                plan_object.type,
                []
            ).append(
                plan_object
            )

        for obj_type in missing_types:

            if planned_by_type.get(
                obj_type
            ):
                plan_object = (
                    planned_by_type[
                        obj_type
                    ][0]
                )
            else:
                plan_object = (
                    self._default_plan_object(
                        obj_type,
                        scene.background
                    )
                )

            scene_objects.append(
                self._plan_object_to_scene_object(
                    plan_object
                )
            )

        layer_by_type = {}

        for plan_object in plan.planned_objects:
            layer_by_type.setdefault(
                plan_object.type,
                plan_object.layer
            )

        scene_objects = sorted(
            scene_objects,
            key=lambda obj: self._layer_rank(
                layer_by_type.get(
                    obj.type,
                    "midground"
                )
            )
        )

        return (
            Scene(
                background=scene.background,
                objects=scene_objects
            ),
            missing_types,
        )

    def _build_retrieval_query(
        self,
        user_request,
        plan
    ):

        planned_types = ", ".join(
            obj.type
            for obj in plan.planned_objects
        )

        composition = "; ".join(
            plan.composition_notes[:4]
        )

        return "\n".join(
            [
                user_request,
                plan.expanded_prompt,
                f"Atmosphere: {plan.atmosphere}",
                f"Focus: {plan.focus}",
                f"Background: {plan.background}",
                f"Planned objects: {planned_types}",
                f"Composition notes: {composition}",
            ]
        )

    def _log_generation(
        self,
        title,
        system_prompt,
        user_prompt,
        response,
        raw_json
    ):

        debug.save_on_file(
            message=f"""
#{title}

## system prompt

{system_prompt}

## user prompt

{user_prompt}

## response

{response}

## raw json

{raw_json}

## cleaned json

{self._clean_json(raw_json)}
"""
        )

    def _build_plan_prompt(
        self,
        user_request
    ):

        return f"""
USER REQUEST

{user_request}

Create a valid scenery plan JSON.

Remember:

- Expand the request into a richer but still relevant landscape brief.
- Every user-requested supported object must appear in planned_objects.
- planned_objects must already be ordered from back to front.
- Return JSON only.
"""

    def _build_scene_prompt(
        self,
        user_request,
        plan,
        context
    ):

        serialized_plan = (
            self._serialize_plan(
                plan
            )
        )

        return f"""
DRAWING KNOWLEDGE

{context}

USER REQUEST

{user_request}

SCENERY PLAN

{serialized_plan}

Create a valid scene JSON that implements the scenery plan.

Remember:

- User instructions override recipe defaults.
- Use the scenery plan as the implementation blueprint.
- Keep the same overall object ordering from the plan whenever possible.
- Every visible element must appear explicitly in JSON.
- There is no hidden scenic backdrop outside the JSON.
- If the user explicitly asks for a supported object, include it.
- Return JSON only.
"""

    def _build_plan_repair_prompt(
        self,
        user_request,
        cleaned,
        error
    ):

        return f"""
Your previous scenery plan JSON was invalid.

USER REQUEST:

{user_request}

INVALID JSON:

{cleaned}

VALIDATION ERROR:

{error}

Fix the scenery plan JSON.

Remember:

- Keep the plan practical for Turtle drawing.
- Keep planned_objects ordered from back to front.
- Return JSON only.
"""

    def _build_scene_repair_prompt(
        self,
        user_request,
        plan,
        context,
        cleaned,
        error
    ):

        serialized_plan = (
            self._serialize_plan(
                plan
            )
        )

        return f"""
Your previous scene JSON was invalid.

USER REQUEST:

{user_request}

SCENERY PLAN:

{serialized_plan}

DRAWING KNOWLEDGE:

{context}

INVALID JSON:

{cleaned}

VALIDATION ERROR:

{error}

Fix the JSON.

Every visible element must remain explicit in JSON.

Return JSON only.
"""

    def _generate_plan(
        self,
        user_request,
        on_status=None,
        on_chunk=None
    ):

        prompt = (
            self._build_plan_prompt(
                user_request
            )
        )

        self._emit_status(
            on_status,
            "Membuat scenery plan dari prompt user..."
        )

        raw_json, response = (
            self.llm.generate_json(
                self.plan_skill,
                prompt,
                on_chunk=self._emit_chunk(
                    on_chunk,
                    "SCENERY PLAN"
                )
            )
        )

        self._emit_status(
            on_status,
            "Scenery plan selesai dibuat. "
            "Memvalidasi plan..."
        )

        self._log_generation(
            "scenery plan generation",
            self.plan_skill,
            prompt,
            response,
            raw_json
        )

        for attempt in range(
            MAX_RETRIES + 1
        ):

            cleaned = (
                self._clean_json(
                    raw_json
                )
            )

            try:
                plan = (
                    SceneryPlan.model_validate_json(
                        cleaned
                    )
                )

                plan, added_types = (
                    self._augment_plan(
                        user_request,
                        plan
                    )
                )

                if added_types:
                    self._emit_status(
                        on_status,
                        "Scenery plan dilengkapi "
                        "otomatis dengan objek: "
                        + ", ".join(
                            added_types
                        )
                    )

                self._emit_status(
                    on_status,
                    "Scenery plan valid."
                )

                return (
                    plan,
                    response
                )

            except (
                ValidationError,
                ValueError
            ) as error:

                if (
                    attempt
                    >= MAX_RETRIES
                ):
                    self._emit_status(
                        on_status,
                        "Model gagal membuat "
                        "scenery plan valid. "
                        "Menggunakan fallback plan."
                    )

                    fallback_plan = (
                        SceneryPlan(
                            expanded_prompt=(
                                user_request
                            ),
                            background="skyblue",
                            atmosphere="balanced",
                            focus=(
                                "user requested scenery"
                            ),
                            composition_notes=[
                                "Place distant objects first.",
                                "Keep the main subject readable.",
                                "Add foreground detail last.",
                            ],
                            planned_objects=[
                                self._default_plan_object(
                                    obj_type,
                                    "skyblue"
                                )
                                for obj_type in sorted(
                                    self._extract_requested_types(
                                        user_request
                                    )
                                )
                            ],
                        )
                    )

                    fallback_plan, added_types = (
                        self._augment_plan(
                            user_request,
                            fallback_plan
                        )
                    )

                    if added_types:
                        self._emit_status(
                            on_status,
                            "Fallback plan "
                            "ditambah objek: "
                            + ", ".join(
                                added_types
                            )
                        )

                    return (
                        fallback_plan,
                        response
                    )

                self._emit_status(
                    on_status,
                    "Scenery plan tidak valid. "
                    f"Repair attempt {attempt + 2}/"
                    f"{MAX_RETRIES + 1}..."
                )

                repair_prompt = (
                    self._build_plan_repair_prompt(
                        user_request,
                        cleaned,
                        error
                    )
                )

                raw_json, response = (
                    self.llm.generate_json(
                        self.plan_skill,
                        repair_prompt,
                        on_chunk=self._emit_chunk(
                            on_chunk,
                            "SCENERY PLAN REPAIR"
                        )
                    )
                )

                self._emit_status(
                    on_status,
                    "Respons repair plan selesai. "
                    "Memvalidasi ulang..."
                )

                self._log_generation(
                    "scenery plan repair",
                    self.plan_skill,
                    repair_prompt,
                    response,
                    raw_json
                )

        raise RuntimeError(
            "Unexpected plan generation error."
        )

    def _generate_scene_json(
        self,
        user_request,
        plan,
        context,
        on_status=None,
        on_chunk=None
    ):

        prompt = (
            self._build_scene_prompt(
                user_request,
                plan,
                context
            )
        )

        self._emit_status(
            on_status,
            "Mengimplementasikan scenery plan menjadi scene JSON..."
        )

        raw_json, response = (
            self.llm.generate_json(
                self.skill,
                prompt,
                on_chunk=self._emit_chunk(
                    on_chunk,
                    "SCENE JSON"
                )
            )
        )

        self._emit_status(
            on_status,
            "Scene JSON selesai dihasilkan. "
            "Memvalidasi scene..."
        )

        self._log_generation(
            "scene generation",
            self.skill,
            prompt,
            response,
            raw_json
        )

        for attempt in range(
            MAX_RETRIES + 1
        ):

            cleaned = (
                self._clean_json(
                    raw_json
                )
            )

            try:
                scene = (
                    Scene.model_validate_json(
                        cleaned
                    )
                )

                scene, added_types = (
                    self._augment_scene(
                        user_request,
                        plan,
                        scene
                    )
                )

                if added_types:
                    self._emit_status(
                        on_status,
                        "Scene JSON dilengkapi "
                        "otomatis dengan objek: "
                        + ", ".join(
                            added_types
                        )
                    )

                self._emit_status(
                    on_status,
                    "Scene JSON valid. "
                    "Scene siap dirender."
                )

                return (
                    scene,
                    response
                )

            except (
                ValidationError,
                ValueError
            ) as error:

                if (
                    attempt
                    >= MAX_RETRIES
                ):
                    raise RuntimeError(
                        "LLM failed to "
                        "produce valid scene"
                    ) from error

                self._emit_status(
                    on_status,
                    "Scene JSON tidak valid. "
                    f"Repair attempt {attempt + 2}/"
                    f"{MAX_RETRIES + 1}..."
                )

                repair_prompt = (
                    self._build_scene_repair_prompt(
                        user_request,
                        plan,
                        context,
                        cleaned,
                        error
                    )
                )

                raw_json, response = (
                    self.llm.generate_json(
                        self.skill,
                        repair_prompt,
                        on_chunk=self._emit_chunk(
                            on_chunk,
                            "SCENE JSON REPAIR"
                        )
                    )
                )

                self._emit_status(
                    on_status,
                    "Respons repair scene selesai. "
                    "Memvalidasi ulang scene..."
                )

                self._log_generation(
                    "scene repair",
                    self.skill,
                    repair_prompt,
                    response,
                    raw_json
                )

        raise RuntimeError(
            "Unexpected scene generation error."
        )

    def generate_scene(
        self,
        user_request,
        on_status=None,
        on_chunk=None
    ):

        plan, plan_response = (
            self._generate_plan(
                user_request,
                on_status=on_status,
                on_chunk=on_chunk
            )
        )

        retrieval_query = (
            self._build_retrieval_query(
                user_request,
                plan
            )
        )

        self._emit_status(
            on_status,
            "Mencari knowledge RAG "
            "berdasarkan scenery plan..."
        )

        hits = (
            self.retriever.search(
                retrieval_query
            )
        )

        self._emit_status(
            on_status,
            "Knowledge ditemukan: "
            f"{self._summarize_hits(hits)}"
        )

        context = (
            self._build_context(
                hits
            )
        )

        scene, scene_response = (
            self._generate_scene_json(
                user_request,
                plan,
                context,
                on_status=on_status,
                on_chunk=on_chunk
            )
        )

        return PipelineResult(
            plan=plan,
            scene=scene,
            hits=hits,
            plan_response=plan_response,
            scene_response=scene_response
        )
