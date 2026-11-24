"""Regression checks for the reusable FlexBenchDog component."""

from pathlib import Path
import unittest

from scpf.runner import run_script

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models" / "components" / "flex_bench_dog" / "scpf" / "model.py"


class FlexBenchDogTests(unittest.TestCase):
    def test_uses_native_cylinders_cone_sketch_cuts_and_chamfers(self):
        commands = run_script(MODEL)["commands"]
        names = [row["command"] for row in commands]

        self.assertEqual(names.count("solid.cylinder"), 2)
        self.assertEqual(names.count("solid.cone"), 1)
        self.assertEqual(names.count("sketch.create"), 11)
        self.assertEqual(names.count("sketch.rectangle.two_point"), 2)
        self.assertEqual(names.count("sketch.line"), 9)
        self.assertEqual(names.count("sketch.slot.center_to_center"), 0)
        self.assertEqual(names.count("solid.extrude"), 11)
        self.assertEqual(names.count("solid.fillet"), 1)
        self.assertEqual(names.count("solid.chamfer"), 3)
        self.assertFalse(any(name == "solid.hole" for name in names))

    def test_native_parameters_are_fit_dimensions(self):
        commands = run_script(MODEL)["commands"]
        params = {
            row["params"]["name"]: row["params"]["expression"]
            for row in commands
            if row["command"] == "parameters.add"
        }
        self.assertEqual(
            params,
            {
                "hole_diameter": "20",
                "interference": "0.2",
                "rim_diameter": "22",
                "slot_width": "1.5",
                "slot_corner_radius": "0.5",
            },
        )

    def test_body_is_symmetric_twenty_mm_around_worktop(self):
        commands = run_script(MODEL)["commands"]
        cylinders = [
            row["params"] for row in commands
            if row["command"] == "solid.cylinder"
        ]

        self.assertEqual(cylinders[0]["base"], [0, 0, 0])
        self.assertEqual(cylinders[0]["height"], 1.5)
        self.assertEqual(cylinders[1]["base"], [0, 0, 1.5])
        self.assertEqual(cylinders[1]["height"], 18.5)

        cones = [
            row["params"] for row in commands
            if row["command"] == "solid.cone"
        ]
        self.assertEqual(len(cones), 1)
        cone = cones[0]
        self.assertEqual(cone["base"], [0, 0, -20])
        self.assertEqual(cone["height"], 20)
        self.assertEqual(cone["axis"], "Z")
        self.assertEqual(cone["top_diameter"], "hole_diameter")
        self.assertIn(
            cone["diameter"],
            ("hole_diameter + interference", "hole_diameter + (interference)"),
        )

    def test_cross_slots_leave_four_mm_flex_root(self):
        commands = run_script(MODEL)["commands"]
        sketches = [
            row["params"]
            for row in commands
            if row["command"] == "sketch.create"
        ]
        self.assertEqual(
            [row["name"] for row in sketches[:2]],
            ["Flex slot X", "Flex slot Y"],
        )
        self.assertEqual(sketches[0]["plane"]["origin"], [0, 0, -20])
        self.assertEqual(sketches[1]["plane"]["origin"], [0, 0, -20])

        cuts = [
            row["params"]
            for row in commands
            if row["command"] == "solid.extrude"
            and row["params"]["operation"] == "cut"
            and row["params"]["name"] in ("Flex slot X", "Flex slot Y")
        ]
        self.assertEqual(len(cuts), 2)
        self.assertTrue(all(row["distance"] == 16 for row in cuts))

    def test_cross_slot_inner_corners_use_one_symmetric_fillet(self):
        commands = run_script(MODEL)["commands"]
        fillets = [
            row["params"]
            for row in commands
            if row["command"] == "solid.fillet"
        ]
        self.assertEqual(len(fillets), 1)
        fillet = fillets[0]
        self.assertEqual(fillet["body"], "FlexBenchDog")
        self.assertIn(fillet["radius"], ("slot_corner_radius", 0.5))
        self.assertEqual(len(fillet["edges"]), 4)

        z_values = {str(edge[2]).replace(" ", "") for edge in fillet["edges"]}
        self.assertEqual(len(z_values), 1)
        self.assertIn(
            next(iter(z_values)),
            ("-12", "-12.0", "-INSERTION_LENGTH+SLOT_LENGTH/2",
             "-(INSERTION_LENGTH)+SLOT_LENGTH/2"),
        )

    def test_mft_collar_has_45_degree_seat_profile(self):
        commands = run_script(MODEL)["commands"]
        chamfers = [
            row["params"]
            for row in commands
            if row["command"] == "solid.chamfer"
        ]
        self.assertEqual(len(chamfers), 3)

        collar = chamfers[0]
        self.assertEqual(collar["distance"], 1.0)
        self.assertEqual(collar["body"], "FlexBenchDog")
        self.assertEqual(collar["edges"][0][1:], [0, 0])
        self.assertIn(
            str(collar["edges"][0][0]).replace(" ", ""),
            ("11", "11.0", "rim_diameter/2", "(rim_diameter)/2"),
        )

        # The 1 mm radial difference between Ø22 and Ø20 makes this selected
        # edge chamfer a 45-degree seat. The remaining 0.5 mm stays vertical.
        cylinders = [
            row["params"]
            for row in commands
            if row["command"] == "solid.cylinder"
        ]
        self.assertEqual(cylinders[0]["height"], 1.5)
        self.assertEqual(cylinders[1]["base"], [0, 0, 1.5])
        self.assertEqual(cylinders[1]["height"], 18.5)

        self.assertEqual(chamfers[1]["distance"], 1.0)
        self.assertEqual(chamfers[2]["distance"], 0.6)

    def test_recessed_top_logo_uses_nine_independent_polygon_rib_cuts(self):
        commands = run_script(MODEL)["commands"]

        segments = (
            ((0.0, 4.0), (3.5, 2.0)),
            ((3.5, 2.0), (3.5, -2.0)),
            ((3.5, -2.0), (0.0, -4.0)),
            ((0.0, -4.0), (-3.5, -2.0)),
            ((-3.5, -2.0), (-3.5, 2.0)),
            ((-3.5, 2.0), (0.0, 4.0)),
            ((0.0, 0.0), (0.0, 4.0)),
            ((0.0, 0.0), (3.5, -2.0)),
            ((0.0, 0.0), (-3.5, -2.0)),
        )

        def strip_points(p0, p1, width=0.6):
            x0, y0 = p0
            x1, y1 = p1
            dx = x1 - x0
            dy = y1 - y0
            length = (dx * dx + dy * dy) ** 0.5
            half_width = width / 2
            ux = dx / length
            uy = dy / length
            px = -uy * half_width
            py = ux * half_width
            ex = ux * half_width
            ey = uy * half_width
            return [
                [x0 - ex + px, y0 - ey + py],
                [x1 + ex + px, y1 + ey + py],
                [x1 + ex - px, y1 + ey - py],
                [x0 - ex - px, y0 - ey - py],
            ]

        sketches = [
            row["params"] for row in commands
            if row["command"] == "sketch.create"
            and row["params"]["name"].startswith("Top logo rib ")
        ]
        self.assertEqual(
            [row["name"] for row in sketches],
            [f"Top logo rib {index}" for index in range(1, 10)],
        )
        self.assertTrue(
            all(row["plane"]["origin"] == [0, 0, 20] for row in sketches)
        )

        self.assertFalse(
            any(row["command"] == "sketch.slot.center_to_center" for row in commands)
        )

        lines = [
            row["params"] for row in commands
            if row["command"] == "sketch.line"
        ]
        self.assertEqual(len(lines), 9)
        for line, segment in zip(lines, segments):
            self.assertTrue(line["closed"])
            self.assertEqual(line["ids"], ["a", "b", "c", "d"])
            expected = strip_points(*segment)
            self.assertEqual(len(line["points"]), 4)
            for actual_point, expected_point in zip(line["points"], expected):
                for actual_value, expected_value in zip(actual_point, expected_point):
                    self.assertAlmostEqual(actual_value, expected_value, places=9)

        cuts = [
            row["params"] for row in commands
            if row["command"] == "solid.extrude"
            and row["params"]["name"].startswith("Top logo rib ")
        ]
        self.assertEqual(len(cuts), 9)
        self.assertTrue(all(row["operation"] == "cut" for row in cuts))
        self.assertTrue(all(row["distance"] == 0.6 for row in cuts))
        self.assertTrue(all(row["direction"] == "negative" for row in cuts))


if __name__ == "__main__":
    unittest.main()
