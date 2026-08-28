import json
import unittest
from unittest.mock import MagicMock, patch

from pydantic import ValidationError

from renderer.renderer import render_scene
from scene.models import Scene
from scene.normalizer import normalize_scene


class JsonToTurtleTest(unittest.TestCase):
    def test_json_scene_can_be_validated_normalized_and_rendered(self):
        scene_json = json.dumps(
            {
                "background": "langit",
                "objects": [
                    {
                        "type": "mountain",
                        "position": "top-left",
                        "size": "large",
                        "color": "abu abu",
                        "properties": {
                            "offset_x": 20
                        }
                    },
                    {
                        "type": "sun",
                        "position": "top-right",
                        "size": "small",
                        "color": "kuning"
                    },
                    {
                        "type": "house",
                        "position": "bottom-center",
                        "size": "medium",
                        "color": "krem",
                        "secondary_color": "merah"
                    },
                    {
                        "type": "tree",
                        "position": "bottom-left",
                        "size": "medium",
                        "color": "hijau",
                        "secondary_color": "hijau tua",
                        "properties": {
                            "offset_x": 30,
                            "offset_y": 10,
                            "scale_multiplier": 1.2
                        }
                    }
                ]
            }
        )

        scene = Scene.model_validate_json(scene_json)
        normalized_scene = normalize_scene(scene)

        self.assertEqual(normalized_scene["background"], "skyblue")
        self.assertEqual(len(normalized_scene["objects"]), 4)

        mountain = normalized_scene["objects"][0]
        self.assertEqual(mountain["type"], "mountain")
        self.assertEqual(mountain["color"], "gray")
        self.assertEqual(mountain["x"], -240.0)
        self.assertEqual(mountain["y"], 180.0)
        self.assertEqual(mountain["scale"], 1.4)

        sun = normalized_scene["objects"][1]
        self.assertEqual(sun["type"], "sun")
        self.assertEqual(sun["color"], "yellow")
        self.assertEqual(sun["x"], 260.0)
        self.assertEqual(sun["y"], 180.0)
        self.assertEqual(sun["scale"], 0.65)

        house = normalized_scene["objects"][2]
        self.assertEqual(house["type"], "house")
        self.assertEqual(house["color"], "beige")
        self.assertEqual(house["secondary_color"], "red")
        self.assertEqual(house["x"], 0.0)
        self.assertEqual(house["y"], -180.0)
        self.assertEqual(house["scale"], 1.0)

        tree = normalized_scene["objects"][3]
        self.assertEqual(tree["type"], "tree")
        self.assertEqual(tree["color"], "green")
        self.assertEqual(tree["secondary_color"], "darkgreen")
        self.assertEqual(tree["x"], -230.0)
        self.assertEqual(tree["y"], -170.0)
        self.assertEqual(tree["scale"], 1.2)

        screen_mock = MagicMock()
        pen_mock = MagicMock()

        with (
            patch(
                "renderer.renderer.turtle.Screen",
                return_value=screen_mock
            ),
            patch(
                "renderer.renderer.turtle.Turtle",
                return_value=pen_mock
            ),
            patch("renderer.renderer.draw_mountain") as draw_mountain,
            patch("renderer.renderer.draw_sun") as draw_sun,
            patch("renderer.renderer.draw_house") as draw_house,
            patch("renderer.renderer.draw_tree") as draw_tree,
            patch("renderer.renderer.draw_basic_object") as draw_basic_object
        ):
            render_scene(normalized_scene)

        screen_mock.setup.assert_called_once()
        screen_mock.title.assert_called_once_with(
            "Tiny LLM Turtle AI"
        )
        screen_mock.bgcolor.assert_called_once_with(
            "skyblue"
        )
        screen_mock.tracer.assert_called_once_with(
            0,
            0
        )
        screen_mock.update.assert_called_once_with()
        screen_mock.mainloop.assert_called_once_with()

        pen_mock.hideturtle.assert_called_once_with()
        pen_mock.speed.assert_called_once_with(0)

        draw_mountain.assert_called_once_with(
            pen_mock,
            mountain
        )
        draw_sun.assert_called_once_with(
            pen_mock,
            sun
        )
        draw_house.assert_called_once_with(
            pen_mock,
            house
        )
        draw_tree.assert_called_once_with(
            pen_mock,
            tree
        )
        draw_basic_object.assert_not_called()

    def test_invalid_object_type_is_rejected_during_json_validation(self):
        invalid_scene_json = json.dumps(
            {
                "background": "white",
                "objects": [
                    {
                        "type": "mobil",
                        "position": "center",
                        "size": "medium",
                        "color": "red"
                    }
                ]
            }
        )

        with self.assertRaises(ValidationError):
            Scene.model_validate_json(
                invalid_scene_json
            )


if __name__ == "__main__":
    unittest.main()
