"""Compare independently written SCPF and SCPC native command plans.

Command-plan comparison catches accidental divergence, but SCPF may keep a
dimension symbolic where SCPC writes the equivalent native literal. Native CI
also executes and evaluates both designs, which remains the geometry proof.
"""
from copy import deepcopy
from pathlib import Path
import json
import unittest

from scpf.runner import run_script as forge_script
from scpc import load_script as native_script
from scripts.ci.model_catalog import source_path

ROOT = Path(__file__).resolve().parents[1]


def normalize_native_plan(document):
    """Normalize representation details that do not change the native design."""
    result = deepcopy(document)
    parameters = {
        command["params"]["name"]: float(command["params"]["expression"])
        for command in result["commands"]
        if command["command"] == "parameters.add"
    }

    parameter_commands = sorted(
        (
            command for command in result["commands"]
            if command["command"] == "parameters.add"
        ),
        key=lambda command: command["params"]["name"],
    )
    feature_commands = [
        command for command in result["commands"]
        if command["command"] != "parameters.add"
    ]

    for command in feature_commands:
        params = command["params"]
        if command["command"] == "solid.fillet":
            radius = params.get("radius")
            if isinstance(radius, str) and radius in parameters:
                params["radius"] = parameters[radius]

        # A positioned XZ sketch at the component origin is equivalent to
        # the unpositioned default plane used by the independent SCPC script.
        if command["command"] == "sketch.create" and params.get("offset") == 0:
            params.pop("offset")

    result["commands"] = parameter_commands + feature_commands
    return result


class InlineFrameDiagnosticTests(unittest.TestCase):
    def test_inline_frame_example_has_no_joint_origin(self):
        native = ROOT / "examples/single-inline-frame-joint/scpc/model.py"
        document = native_script(native).to_dict()

        origins = [
            command for command in document["commands"]
            if command["command"] == "joint.origin"
        ]
        joints = [
            command["params"] for command in document["commands"]
            if command["command"] == "joint.create"
        ]

        self.assertEqual(origins, [])
        self.assertEqual(len(joints), 1)
        self.assertEqual(
            joints[0]["b"],
            {
                "occurrence": "Child:1",
                "point": [40, -20, 80],
                "z": [0, 1, 0],
                "x": [1, 0, 0],
            },
        )


class ParallelModelTests(unittest.TestCase):
    def test_bolted_flange_scpc_matches_simple_primitive_model(self):
        native = source_path(ROOT, "bolted-flange", "scpc")
        forge = source_path(ROOT, "bolted-flange")
        source = native.read_text(encoding="utf-8")
        self.assertIn("script.add(", source)
        self.assertNotIn("from scpf", source)
        self.assertNotIn("scpf.runner", source)

        scpc_doc = native_script(native).to_dict()
        scpf_doc = forge_script(forge)

        self.assertEqual(
            normalize_native_plan(scpc_doc),
            normalize_native_plan(scpf_doc),
        )
        commands = scpc_doc["commands"]
        self.assertEqual(len(commands), 9)
        self.assertEqual(
            [row["command"] for row in commands],
            ["solid.cylinder", "solid.cylinder"] + ["solid.hole"] * 7,
        )
        self.assertFalse(
            any(row["command"].startswith("sketch.") for row in commands)
        )
        self.assertFalse(
            any(row["command"].startswith("solid.pattern.") for row in commands)
        )

    def test_flex_bench_dog_scpc_matches_mft_collar_contract(self):
        native = source_path(ROOT, "flex-bench-dog", "scpc")
        forge = source_path(ROOT, "flex-bench-dog")
        scpc_doc = native_script(native).to_dict()
        scpf_doc = forge_script(forge)

        def collar_contract(document):
            features = [
                row for row in document["commands"]
                if row["command"] != "parameters.add"
            ]
            cylinders = [
                row["params"] for row in features
                if row["command"] == "solid.cylinder"
            ]
            chamfers = [
                row["params"] for row in features
                if row["command"] == "solid.chamfer"
            ]
            return cylinders[0], cylinders[1], chamfers[0]

        scpc_rim, scpc_upper, scpc_seat = collar_contract(scpc_doc)
        scpf_rim, scpf_upper, scpf_seat = collar_contract(scpf_doc)

        for rim in (scpc_rim, scpf_rim):
            self.assertEqual(rim["base"], [0, 0, 0])
            self.assertEqual(rim["height"], 1.5)
            self.assertEqual(rim["diameter"], "rim_diameter")

        for upper in (scpc_upper, scpf_upper):
            self.assertEqual(upper["base"], [0, 0, 1.5])
            self.assertEqual(upper["height"], 18.5)
            self.assertEqual(upper["diameter"], "hole_diameter")

        for seat in (scpc_seat, scpf_seat):
            self.assertEqual(seat["distance"], 1.0)
            self.assertEqual(seat["body"], "FlexBenchDog")

    def test_flex_bench_dog_scpc_matches_inner_corner_fillet_contract(self):
        native = source_path(ROOT, "flex-bench-dog", "scpc")
        forge = source_path(ROOT, "flex-bench-dog")
        scpc_doc = native_script(native).to_dict()
        scpf_doc = forge_script(forge)

        for document in (scpc_doc, scpf_doc):
            fillets = [
                row["params"] for row in document["commands"]
                if row["command"] == "solid.fillet"
            ]
            self.assertEqual(len(fillets), 1)
            self.assertEqual(fillets[0]["body"], "FlexBenchDog")
            self.assertEqual(len(fillets[0]["edges"]), 4)

        scpc_fillet = next(
            row["params"] for row in scpc_doc["commands"]
            if row["command"] == "solid.fillet"
        )
        self.assertEqual(scpc_fillet["radius"], "slot_corner_radius")
        self.assertEqual(
            scpc_fillet["edges"],
            [
                [0.75, 0.75, -12],
                [-0.75, 0.75, -12],
                [-0.75, -0.75, -12],
                [0.75, -0.75, -12],
            ],
        )

    def test_flex_bench_dog_scpc_matches_independent_slot_logo_contract(self):
        native = source_path(ROOT, "flex-bench-dog", "scpc")
        forge = source_path(ROOT, "flex-bench-dog")
        scpc_doc = native_script(native).to_dict()
        scpf_doc = forge_script(forge)

        for document in (scpc_doc, scpf_doc):
            logo_sketches = [
                row["params"] for row in document["commands"]
                if row["command"] == "sketch.create"
                and row["params"]["name"].startswith("Top logo rib ")
            ]
            slots = [
                row["params"] for row in document["commands"]
                if row["command"] == "sketch.slot.center_to_center"
            ]
            cuts = [
                row["params"] for row in document["commands"]
                if row["command"] == "solid.extrude"
                and row["params"]["name"].startswith("Top logo rib ")
            ]

            self.assertEqual(len(logo_sketches), 9)
            self.assertEqual(len(slots), 9)
            self.assertEqual(len(cuts), 9)
            self.assertTrue(all(row["width"] == 0.6 for row in slots))
            self.assertTrue(all(row["operation"] == "cut" for row in cuts))
            self.assertTrue(all(row["distance"] == 0.6 for row in cuts))
            self.assertTrue(all(row["direction"] == "negative" for row in cuts))
            self.assertFalse(
                any(row["command"] == "sketch.line" for row in document["commands"])
            )

        scpc_slots = [
            row["params"] for row in scpc_doc["commands"]
            if row["command"] == "sketch.slot.center_to_center"
        ]
        scpf_slots = [
            row["params"] for row in scpf_doc["commands"]
            if row["command"] == "sketch.slot.center_to_center"
        ]
        self.assertEqual(scpc_slots, scpf_slots)

    def test_plate_and_corner_bracket_have_independent_native_scripts(self):
        for slug in ("plate", "corner-bracket"):
            with self.subTest(slug=slug):
                forge = source_path(ROOT, slug)
                native = source_path(ROOT, slug, "scpc")
                self.assertTrue(forge.is_file())
                self.assertTrue(native.is_file())

                source = native.read_text(encoding="utf-8")
                self.assertIn("script.add(", source)
                self.assertNotIn("from scpf", source)
                self.assertNotIn("scpf.runner", source)
                self.assertNotIn("json.load", source)
                self.assertNotIn("run_script", source)

                scpc_doc = native_script(native).to_dict()
                scpf_doc = forge_script(forge)

                # Plate lowers identically after representation
                # normalization. CornerBracket now deliberately routes the
                # shared component through private placement inputs, so Forge
                # may write algebraically equivalent profile expressions such
                # as "x * 1 + 0". For that model compare the native contract
                # here; native CI proves equal BRep + feature history.
                if slug == "plate":
                    self.assertEqual(
                        normalize_native_plan(scpc_doc),
                        normalize_native_plan(scpf_doc),
                    )
                else:
                    def parameter_map(document):
                        return {
                            row["params"]["name"]:
                                float(row["params"]["expression"])
                            for row in document["commands"]
                            if row["command"] == "parameters.add"
                        }

                    def feature_kinds(document):
                        return [
                            row["command"]
                            for row in document["commands"]
                            if row["command"] != "parameters.add"
                        ]

                    self.assertEqual(
                        parameter_map(scpc_doc),
                        parameter_map(scpf_doc),
                    )
                    self.assertEqual(
                        feature_kinds(scpc_doc),
                        feature_kinds(scpf_doc),
                    )

                    scpc_sketch = next(
                        row["params"] for row in scpc_doc["commands"]
                        if row["command"] == "sketch.line"
                    )
                    scpf_sketch = next(
                        row["params"] for row in scpf_doc["commands"]
                        if row["command"] == "sketch.line"
                    )
                    self.assertEqual(scpc_sketch["ids"], scpf_sketch["ids"])
                    self.assertEqual(
                        len(scpc_sketch["points"]),
                        len(scpf_sketch["points"]),
                    )

                self.assertEqual(
                    len(scpc_doc["commands"]),
                    9 if slug == "plate" else 42,
                )


if __name__ == "__main__":
    unittest.main()
