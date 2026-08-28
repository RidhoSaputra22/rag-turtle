import importlib.util
import sys
import types
import unittest
from unittest.mock import MagicMock, patch

# The composition helpers do not call Ollama or Chroma. Stubs keep this focused
# unit test runnable before the optional runtime dependencies are installed.
if importlib.util.find_spec("ollama") is None:
    sys.modules["ollama"] = types.ModuleType("ollama")

if importlib.util.find_spec("chromadb") is None:
    sys.modules["chromadb"] = types.ModuleType("chromadb")

from agent.pipeline import TurtlePipeline
from renderer import objects as drawing_objects
from renderer.renderer import render_scene
from scene.models import PlanObject, Scene, SceneryPlan
from scene.normalizer import normalize_scene


class ScenicCompositionTest(unittest.TestCase):
    def setUp(self):
        # These helpers are pure and do not need Ollama or a Chroma database.
        self.pipeline = TurtlePipeline.__new__(TurtlePipeline)

    def test_sparse_landscape_plan_gets_balanced_depth(self):
        plan = SceneryPlan(
            expanded_prompt="Mountain, tree, and flowers.",
            background="skyblue",
            planned_objects=[
                PlanObject(
                    type="mountain",
                    position="top-left",
                    size="large",
                    color="slategray",
                    secondary_color="white",
                    layer="background",
                    properties={"snow_cap": True},
                ),
                PlanObject(
                    type="tree",
                    position="bottom-right",
                    size="medium",
                    color="forestgreen",
                    layer="foreground",
                ),
                PlanObject(
                    type="flower",
                    position="bottom-left",
                    size="small",
                    color="pink",
                    layer="foreground",
                ),
            ],
        )

        enriched, added_types = self.pipeline._enrich_plan_for_scenery(
            "Buat pemandangan gunung, pohon, dan bunga yang indah",
            plan,
        )

        object_types = [obj.type for obj in enriched.planned_objects]
        self.assertIn("cloud", object_types)
        self.assertIn("sun", object_types)
        self.assertIn("meadow", object_types)
        self.assertIn("hill", object_types)
        self.assertIn("bush", object_types)
        self.assertEqual(
            added_types,
            ["cloud", "sun", "meadow", "hill", "bush"],
        )
        self.assertEqual(
            [obj.layer for obj in enriched.planned_objects],
            sorted(
                (obj.layer for obj in enriched.planned_objects),
                key=self.pipeline._layer_rank,
            ),
        )

    def test_scene_reconciles_missing_objects_from_the_plan(self):
        plan = SceneryPlan(
            expanded_prompt="Layered countryside.",
            planned_objects=[
                PlanObject(
                    type="cloud",
                    position="top-left",
                    size="small",
                    color="white",
                    layer="sky",
                ),
                PlanObject(
                    type="meadow",
                    position="bottom",
                    size="large",
                    color="#78b957",
                    layer="background",
                ),
                PlanObject(
                    type="tree",
                    position="bottom-right",
                    size="medium",
                    color="forestgreen",
                    layer="foreground",
                ),
            ],
        )

        scene, added_types = self.pipeline._augment_scene(
            "Buat pemandangan alam",
            plan,
            Scene(background="skyblue", objects=[]),
        )

        self.assertEqual(added_types, ["cloud", "meadow", "tree"])
        self.assertEqual(
            [obj.type for obj in scene.objects],
            ["cloud", "meadow", "tree"],
        )
        self.assertEqual(
            [obj.layer for obj in scene.objects],
            ["sky", "background", "foreground"],
        )

    def test_normalizer_keeps_only_supported_rendering_properties(self):
        scene = Scene.model_validate({
            "background": "langit",
            "objects": [
                {
                    "type": "meadow",
                    "position": "bottom",
                    "size": "large",
                    "color": "meadow green",
                    "secondary_color": "light green",
                    "layer": "background",
                    "properties": {
                        "offset_y": -55,
                        "width_scale": 1.05,
                        "not_a_renderer_property": "discard me",
                    },
                }
            ],
        })

        normalized = normalize_scene(scene)
        meadow = normalized["objects"][0]

        self.assertEqual(normalized["background"], "skyblue")
        self.assertEqual(meadow["color"], "#78b957")
        self.assertEqual(meadow["layer"], "background")
        self.assertEqual(
            meadow["properties"],
            {"offset_y": -55.0, "width_scale": 1.05},
        )

    def test_renderer_dispatches_new_explicit_ground_and_path_objects(self):
        scene = {
            "background": "skyblue",
            "objects": [
                {"type": "meadow"},
                {"type": "path"},
            ],
        }
        screen_mock = MagicMock()
        pen_mock = MagicMock()

        with (
            patch("renderer.renderer.turtle.Screen", return_value=screen_mock),
            patch("renderer.renderer.turtle.Turtle", return_value=pen_mock),
            patch("renderer.renderer.draw_meadow") as draw_meadow,
            patch("renderer.renderer.draw_path") as draw_path,
            patch("renderer.renderer.draw_basic_object") as draw_basic_object,
        ):
            render_scene(scene)

        draw_meadow.assert_called_once_with(pen_mock, scene["objects"][0])
        draw_path.assert_called_once_with(pen_mock, scene["objects"][1])
        draw_basic_object.assert_not_called()

    def test_enhanced_drawers_accept_a_complete_normalized_scene(self):
        scene = Scene.model_validate({
            "background": "skyblue",
            "objects": [
                {
                    "type": "cloud", "position": "top-left",
                    "size": "small", "color": "white", "layer": "sky",
                },
                {
                    "type": "sun", "position": "top-right",
                    "size": "medium", "color": "#ffd166", "layer": "sky",
                },
                {
                    "type": "mountain", "position": "top-left",
                    "size": "large", "color": "slategray",
                    "secondary_color": "white", "layer": "background",
                    "properties": {"snow_cap": True},
                },
                {
                    "type": "meadow", "position": "bottom",
                    "size": "large", "color": "#78b957",
                    "layer": "background",
                },
                {
                    "type": "hill", "position": "bottom-left",
                    "size": "large", "color": "yellowgreen", "layer": "midground",
                },
                {
                    "type": "path", "position": "bottom",
                    "size": "medium", "color": "tan", "layer": "midground",
                    "properties": {"bend": "center"},
                },
                {
                    "type": "river", "position": "bottom-right",
                    "size": "medium", "color": "dodgerblue", "layer": "midground",
                    "properties": {"bend": "left"},
                },
                {
                    "type": "tree", "position": "bottom-right",
                    "size": "medium", "color": "forestgreen", "layer": "foreground",
                },
                {
                    "type": "bush", "position": "bottom-left",
                    "size": "small", "color": "forestgreen", "layer": "foreground",
                },
                {
                    "type": "flower", "position": "bottom-right",
                    "size": "small", "color": "pink", "layer": "foreground",
                },
            ],
        })
        drawers = {
            "cloud": drawing_objects.draw_cloud,
            "sun": drawing_objects.draw_sun,
            "mountain": drawing_objects.draw_mountain,
            "meadow": drawing_objects.draw_meadow,
            "hill": drawing_objects.draw_hill,
            "path": drawing_objects.draw_path,
            "river": drawing_objects.draw_river,
            "tree": drawing_objects.draw_tree,
            "bush": drawing_objects.draw_bush,
            "flower": drawing_objects.draw_flower,
        }
        pen_mock = MagicMock()

        for obj in normalize_scene(scene)["objects"]:
            drawers[obj["type"]](pen_mock, obj)

        self.assertTrue(pen_mock.begin_fill.called)


if __name__ == "__main__":
    unittest.main()
