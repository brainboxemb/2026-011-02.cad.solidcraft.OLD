"""Repository ownership contracts for product CAD sources."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RepositoryOwnershipTests(unittest.TestCase):
    def test_cross_cad_reference_implementations_are_not_product_sources(self):
        roots = (
            ROOT / "models/basic/csg_cube",
            ROOT / "models/basic/plate",
        )
        implementations = ("cadquery", "microcad", "pythonscad", "vcad")
        for root in roots:
            for implementation in implementations:
                with self.subTest(root=root.name, implementation=implementation):
                    self.assertFalse((root / implementation).exists())


if __name__ == "__main__":
    unittest.main()
