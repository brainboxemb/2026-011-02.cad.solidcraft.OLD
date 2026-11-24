"""Regression checks for the standalone CornerBracket example."""
from pathlib import Path
import unittest

from scpf.runner import run_script

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "models" / "components" / "corner_bracket" / "scpf" / "model.py"
REFERENCE = (
    ROOT / "models" / "components" / "corner_bracket" / "scpf" / "reference.py"
)


class CornerBracketTests(unittest.TestCase):
    @staticmethod
    def _resolved(value, parameters):
        if isinstance(value, (int, float)):
            return float(value)
        expression = value[:-3] if value.endswith(" mm") else value
        return float(eval(expression, {"__builtins__": {}}, parameters))

    @classmethod
    def _parameter_values(cls, commands):
        return {
            row["params"]["name"]: float(row["params"]["expression"])
            for row in commands
            if row["command"] == "parameters.add"
        }

    def test_default_bracket_restores_exact_recessed_fixing_contract(self):
        commands = run_script(COMPONENT)["commands"]
        holes = [c["params"] for c in commands if c["command"] == "solid.hole"]
        chamfers = [c["params"] for c in commands if c["command"] == "solid.chamfer"]
        fillets = [c["params"] for c in commands if c["command"] == "solid.fillet"]

        self.assertEqual(len(commands), 58)
        self.assertEqual(len(holes), 16)
        self.assertEqual(len(chamfers), 2)
        self.assertEqual(len(fillets), 1)

        names = {
            c["params"]["name"]
            for c in commands
            if c["command"] == "parameters.add"
        }
        self.assertEqual(
            names,
            {
                "arm_width", "arm_height",
                "horizontal_arm_length", "vertical_arm_length",
                "outer_corner_chamfer", "arm_end_chamfer",
                "side_edge_chamfer", "elephant_foot_relief",
                "inside_corner_radius", "plywood_thickness",
                "bolt_offset", "bolt_spacing", "bolt_y_offset",
                "bolt_diameter", "bolt_clearance",
                "head_diameter", "head_clearance", "head_recess",
                "bolt_hole_edge_relief",
            },
        )

    def test_standalone_uses_exact_shared_component_class(self):
        source = COMPONENT.read_text(encoding="utf-8")
        self.assertIn("class CornerBracket:", source)
        self.assertNotIn("CornerBracket()", source)
        self.assertNotIn("_Shared.build", source)
        self.assertNotIn("hasattr(", source)
        self.assertNotIn("getattr(", source)
        self.assertEqual(source.count("        points = ["), 1)

    def test_profile_restores_open_scad_arm_tip_relief(self):
        commands = run_script(COMPONENT)["commands"]
        sketch = next(c for c in commands if c["command"] == "sketch.line")
        self.assertEqual(len(sketch["params"]["points"]), 11)
        self.assertEqual(
            sketch["params"]["ids"],
            [
                "i_corner",
                "tip_hor_relief",
                "o_hor_tip",
                "o_hor_bevel",
                "o_hor",
                "o_corner",
                "o_vert",
                "o_vert_bevel",
                "o_vert_end",
                "tip_vert_relief",
                "v_tip",
            ],
        )
        parameters = self._parameter_values(commands)
        actual = [
            [self._resolved(value, parameters) for value in point]
            for point in sketch["params"]["points"]
        ]
        self.assertEqual(
            actual,
            [
                [0.0, 0.0],
                [59.4, 0.0],
                [60.0, -0.6],
                [60.0, -9.0],
                [57.0, -12.0],
                [-6.0, -12.0],
                [-12.0, -6.0],
                [-12.0, 57.0],
                [-9.0, 60.0],
                [-0.6, 60.0],
                [0.0, 59.4],
            ],
        )

    def test_named_edges_compile_without_full_width_tip_chamfer(self):
        commands = run_script(COMPONENT)["commands"]
        fillet = next(c for c in commands if c["command"] == "solid.fillet")
        self.assertEqual(fillet["params"]["edges"], [[0, 0, 0]])

        chamfers = [c["params"] for c in commands if c["command"] == "solid.chamfer"]
        self.assertEqual(len(chamfers), 2)
        self.assertEqual(chamfers[0]["distance"], "side_edge_chamfer")
        self.assertEqual(len(chamfers[0]["edges"]), 14)
        self.assertEqual(chamfers[1]["distance"], "elephant_foot_relief")
        self.assertEqual(chamfers[1]["edges"], [[29.7, -12, 0], [29.7, 12, 0]])
        self.assertFalse(
            any(
                row["edges"] == [[60, 0, 0], [0, 0, -60]]
                for row in chamfers
            )
        )

    def test_arm_tip_wedges_match_preserved_open_scad_frames(self):
        commands = run_script(COMPONENT)["commands"]
        parameters = self._parameter_values(commands)
        s2 = 2 ** -0.5

        names = [
            "Horizontal tip relief +Y",
            "Horizontal tip relief -Y",
            "Vertical tip relief +Y",
            "Vertical tip relief -Y",
        ]
        sketches = [
            row["params"] for row in commands
            if row["command"] == "sketch.create"
            and row["params"]["name"] in names
        ]
        self.assertEqual([row["name"] for row in sketches], names)

        expected_origins = (
            [60.0 - 2.0 - s2, 12.0 + s2, 0.0],
            [60.0 - 2.0 - s2, -(12.0 + s2), 0.0],
            [0.0, 12.0 - 2.0 - s2, -60.0 - s2],
            [0.0, -(12.0 - 2.0 - s2), -60.0 - s2],
        )
        expected_axes = (
            ([s2, s2, 0.0], [0.0, 0.0, 1.0]),
            ([s2, -s2, 0.0], [0.0, 0.0, 1.0]),
            ([0.0, s2, -s2], [-1.0, 0.0, 0.0]),
            ([0.0, -s2, -s2], [-1.0, 0.0, 0.0]),
        )
        for sketch, expected_origin, (expected_x, expected_y) in zip(
            sketches, expected_origins, expected_axes
        ):
            plane = sketch["plane"]
            actual_origin = [
                self._resolved(value, parameters) for value in plane["origin"]
            ]
            for actual, expected in zip(actual_origin, expected_origin):
                self.assertAlmostEqual(actual, expected, places=9)
            for actual, expected in zip(plane["x_dir"], expected_x):
                self.assertAlmostEqual(actual, expected, places=9)
            for actual, expected in zip(plane["y_dir"], expected_y):
                self.assertAlmostEqual(actual, expected, places=9)

        lines = [
            row["params"] for row in commands
            if row["command"] == "sketch.line"
        ]
        self.assertEqual(len(lines), 5)
        for line in lines[1:]:
            actual = [
                [self._resolved(value, parameters) for value in point]
                for point in line["points"]
            ]
            self.assertEqual(
                actual,
                [[-1.6, -1.0], [1.0, -1.0], [1.0, 1.6]],
            )
            self.assertTrue(line["closed"])

        cuts = [
            row["params"] for row in commands
            if row["command"] == "solid.extrude"
            and row["params"].get("operation") == "cut"
        ]
        self.assertEqual(len(cuts), 4)
        self.assertEqual(
            [row["direction"] for row in cuts],
            ["positive", "negative", "positive", "negative"],
        )
        self.assertTrue(
            all(row["targets"] == ["CornerBracket"] for row in cuts)
        )
        expected_length = 2.0 * (2 ** 0.5) + 2.0
        for row in cuts:
            self.assertAlmostEqual(
                self._resolved(row["distance"], parameters),
                expected_length,
                delta=1e-5,
            )

        second_chamfer = max(
            index for index, row in enumerate(commands)
            if row["command"] == "solid.chamfer"
        )
        first_wedge = next(
            index for index, row in enumerate(commands)
            if row["command"] == "sketch.create"
            and row["params"]["name"] == names[0]
        )
        first_hole = next(
            index for index, row in enumerate(commands)
            if row["command"] == "solid.hole"
        )
        self.assertLess(second_chamfer, first_wedge)
        self.assertLess(first_wedge, first_hole)

    def test_each_bolt_seat_has_flat_recess_cone_and_two_edge_reliefs(self):
        commands = run_script(COMPONENT)["commands"]
        parameters = self._parameter_values(commands)
        holes = [c["params"] for c in commands if c["command"] == "solid.hole"]
        self.assertEqual(len(holes), 16)

        for index in range(0, 16, 4):
            flat, cone, outside_relief, inside_relief = holes[index:index + 4]

            self.assertAlmostEqual(self._resolved(flat["diameter"], parameters), 10.4)
            self.assertAlmostEqual(self._resolved(flat["depth"], parameters), 1.0)
            self.assertNotIn("type", flat)

            self.assertAlmostEqual(self._resolved(cone["diameter"], parameters), 5.4)
            self.assertAlmostEqual(self._resolved(cone["depth"], parameters), 11.0)
            self.assertEqual(cone["type"], "countersink")
            self.assertAlmostEqual(self._resolved(cone["cs_diameter"], parameters), 10.4)
            self.assertEqual(cone["cs_angle"], 90)

            self.assertAlmostEqual(
                self._resolved(outside_relief["diameter"], parameters), 10.8
            )
            self.assertAlmostEqual(
                self._resolved(outside_relief["depth"], parameters), 0.2
            )
            self.assertAlmostEqual(
                self._resolved(inside_relief["diameter"], parameters), 5.8
            )
            self.assertAlmostEqual(
                self._resolved(inside_relief["depth"], parameters), 0.2
            )

        outside_positions = [
            [self._resolved(value, parameters) for value in holes[i]["position"]]
            for i in range(0, 16, 4)
        ]
        self.assertEqual(
            outside_positions,
            [
                [24.0, 0.0, 12.0],
                [42.0, 0.0, 12.0],
                [-12.0, 0.0, -24.0],
                [-12.0, 0.0, -42.0],
            ],
        )
        self.assertEqual(
            [holes[i]["direction"] for i in range(0, 16, 4)],
            [[0, 0, -1], [0, 0, -1], [1, 0, 0], [1, 0, 0]],
        )

    def test_missing_profile_edge_name_is_rejected(self):
        from scpf import Sketch
        from scpf.core import Polygon2D, Edges
        from scpf.features import compile_features
        from scpf.compiler import ModelError

        with Sketch(plane="XZ") as sketch:
            Polygon2D(
                [(0, 0), (10, 0), (10, 10), (0, 10)],
                plane="XZ",
                ids=["bottom", "right", "top", "left"],
            )
        shape = sketch.extrude(10, sym=True)
        shape = shape.chamfer(1, edges=Edges.from_profile("o_*"))
        with self.assertRaisesRegex(ModelError, "no polygon segment or vertex matches"):
            compile_features(shape, "Square")

    def test_named_profile_selection_requires_segment_ids(self):
        from scpf import Sketch
        from scpf.core import Polygon2D, Edges
        from scpf.features import compile_features
        from scpf.compiler import ModelError

        with Sketch(plane="XZ") as sketch:
            Polygon2D(
                [(0, 0), (10, 0), (10, 10), (0, 10)],
                plane="XZ",
            )
        shape = sketch.extrude(10, sym=True)
        shape = shape.chamfer(1, edges=Edges.from_profile("o_*"))
        with self.assertRaisesRegex(ModelError, "must define ids"):
            compile_features(shape, "Square")

    def test_sweep_edge_selection_uses_named_vertices(self):
        from scpf import Sketch
        from scpf.core import Polygon2D, Edges
        from scpf.features import compile_features

        with Sketch(plane="XZ") as sketch:
            Polygon2D([
                ("start", (0, 0)), ("tip", (10, 0)),
                ("far", (10, 8)), ("end", (0, 8)),
            ], plane="XZ", world=True)
        shape = sketch.extrude(8, sym=True)
        shape = shape.chamfer(0.5, edges=Edges.from_vertices("tip", "end"))
        chamfer = next(
            c for c in compile_features(shape, "Plate")
            if c["command"] == "solid.chamfer"
        )
        self.assertEqual(chamfer["params"]["edges"], [[10, 0, 0], [0, 0, 8]])

    def test_historical_reference_remains_original_and_separate(self):
        # Archived source remains verbatim; the live component ports its
        # geometry intent to current Hole/CountersinkHole features.
        reference = REFERENCE.read_text(encoding="utf-8")
        self.assertIn("class CornerBracket:", reference)
        self.assertEqual(reference.count("countersink_d=head_d"), 2)
        self.assertEqual(reference.count("countersink_recess=self.head_recess"), 2)
        self.assertIn("CornerBracket()", reference)
        self.assertNotIn("CountersinkHole(", reference)


if __name__ == "__main__":
    unittest.main()
