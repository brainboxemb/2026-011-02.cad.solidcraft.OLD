"""Regression checks for the reusable FlexBenchDog component."""

from pathlib import Path
import unittest

from scpf.runner import run_script

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models" / "components" / "flex_bench_dog" / "scpf" / "model.py"


class FlexBenchDogTests(unittest.TestCase):
    def test_uses_native_cylinders_sketch_cuts_and_chamfers(self):
        commands = run_script(MODEL)["commands"]
        names = [row["command"] for row in commands]

        self.assertEqual(names.count("solid.cylinder"), 4)
        self.assertEqual(names.count("sketch.create"), 11)
        self.assertEqual(names.count("sketch.rectangle.two_point"), 2)
        self.assertEqual(names.count("sketch.line"), 0)
        self.assertEqual(names.count("sketch.slot.center_to_center"), 9)
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
        self.assertEqual(cylinders[2]["base"], [0, 0, -20])
        self.assertEqual(cylinders[2]["height"], 20)
        self.assertEqual(cylinders[3]["base"], [0, 0, -20])
        self.assertEqual(cylinders[3]["height"], 2)
        self.assertIn(
            cylinders[3]["diameter"],
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

    def test_recessed_top_logo_uses_nine_independent_slot_rib_cuts(self):
        commands = run_script(MODEL)["commands"]
        expected = [
            ([0.0, 4.0], [3.5, 2.0]),
            ([3.5, 2.0], [3.5, -2.0]),
            ([3.5, -2.0], [0.0, -4.0]),
            ([0.0, -4.0], [-3.5, -2.0]),
            ([-3.5, -2.0], [-3.5, 2.0]),
            ([-3.5, 2.0], [0.0, 4.0]),
            ([0.0, 0.0], [0.0, 4.0]),
            ([0.0, 0.0], [3.5, -2.0]),
            ([0.0, 0.0], [-3.5, -2.0]),
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

        slots = [
            row["params"] for row in commands
            if row["command"] == "sketch.slot.center_to_center"
        ]
        self.assertEqual(len(slots), 9)
        for slot, (p0, p1) in zip(slots, expected):
            self.assertEqual(slot["p0"], p0)
            self.assertEqual(slot["p1"], p1)
            self.assertEqual(slot["width"], 0.6)

        self.assertFalse(any(row["command"] == "sketch.line" for row in commands))

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
