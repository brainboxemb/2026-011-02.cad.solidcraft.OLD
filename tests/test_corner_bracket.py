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
    def test_default_bracket_restores_exact_recessed_fixing_contract(self):
        commands = run_script(COMPONENT)["commands"]
        holes = [c["params"] for c in commands if c["command"] == "solid.hole"]
        chamfers = [c["params"] for c in commands if c["command"] == "solid.chamfer"]
        fillets = [c["params"] for c in commands if c["command"] == "solid.fillet"]

        self.assertEqual(len(commands), 42)
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
        self.assertEqual(source.count("points = ["), 1)

    def test_profile_restores_open_scad_arm_tip_relief(self):
        commands = run_script(COMPONENT)["commands"]
        sketch = next(c for c in commands if c["command"] == "sketch.line")
        self.assertEqual(len(sketch["params"]["points"]), 11)
        self.assertEqual(
            sketch["params"]["ids"],
            [
                "i_corner",
                "o_hor_tip_relief",
                "o_hor_tip",
                "o_hor_bevel",
                "o_hor",
                "o_corner",
                "o_vert",
                "o_vert_bevel",
                "o_vert_end",
                "o_vert_tip_relief",
                "v_tip",
            ],
        )
        points = sketch["params"]["points"]
        self.assertEqual(points[0], [0, 0])
        self.assertEqual(points[1], ["horizontal_arm_length - (elephant_foot_relief)", 0])
        self.assertEqual(points[2], ["horizontal_arm_length", "-(elephant_foot_relief)"])
        self.assertEqual(points[-2], ["-(elephant_foot_relief)", "-(vertical_arm_length)"])
        self.assertEqual(points[-1], [0, "-((vertical_arm_length) - (elephant_foot_relief))"])

    def test_named_edges_compile_without_full_width_tip_chamfer(self):
        commands = run_script(COMPONENT)["commands"]
        fillet = next(c for c in commands if c["command"] == "solid.fillet")
        self.assertEqual(fillet["params"]["edges"], [[0, 0, 0]])

        chamfers = [c["params"] for c in commands if c["command"] == "solid.chamfer"]
        self.assertEqual(len(chamfers), 2)
        self.assertEqual(chamfers[0]["distance"], "side_edge_chamfer")
        self.assertEqual(len(chamfers[0]["edges"]), 18)
        self.assertEqual(chamfers[1]["distance"], "elephant_foot_relief")
        self.assertEqual(chamfers[1]["edges"], [[29.7, -12, 0], [29.7, 12, 0]])
        self.assertFalse(
            any(
                row["edges"] == [[60, 0, 0], [0, 0, -60]]
                for row in chamfers
            )
        )

    def test_each_bolt_seat_has_flat_recess_cone_and_two_edge_reliefs(self):
        commands = run_script(COMPONENT)["commands"]
        holes = [c["params"] for c in commands if c["command"] == "solid.hole"]
        self.assertEqual(len(holes), 16)

        for index in range(0, 16, 4):
            flat, cone, outside_relief, inside_relief = holes[index:index + 4]
            self.assertEqual(flat["diameter"], "head_diameter + head_clearance")
            self.assertEqual(flat["depth"], "head_recess")
            self.assertNotIn("type", flat)

            self.assertEqual(cone["diameter"], "bolt_diameter + bolt_clearance")
            self.assertEqual(cone["depth"], "arm_height - head_recess")
            self.assertEqual(cone["type"], "countersink")
            self.assertEqual(cone["cs_diameter"], "head_diameter + head_clearance")
            self.assertEqual(cone["cs_angle"], 90)

            self.assertEqual(
                outside_relief["diameter"],
                "head_diameter + head_clearance + 2 * bolt_hole_edge_relief",
            )
            self.assertEqual(outside_relief["depth"], "bolt_hole_edge_relief")
            self.assertEqual(
                inside_relief["diameter"],
                "bolt_diameter + bolt_clearance + 2 * bolt_hole_edge_relief",
            )
            self.assertEqual(inside_relief["depth"], "bolt_hole_edge_relief")

        outside_positions = [holes[i]["position"] for i in range(0, 16, 4)]
        self.assertEqual(
            outside_positions,
            [
                ["plywood_thickness + bolt_offset", "bolt_y_offset", "arm_height"],
                ["plywood_thickness + bolt_offset + bolt_spacing", "bolt_y_offset", "arm_height"],
                ["-(arm_height)", "bolt_y_offset", "-(plywood_thickness + bolt_offset)"],
                ["-(arm_height)", "bolt_y_offset", "-(plywood_thickness + bolt_offset + bolt_spacing)"],
            ],
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
