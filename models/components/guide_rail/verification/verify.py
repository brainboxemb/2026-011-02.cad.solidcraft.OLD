"""Check both guide-rail profiles against earlier accepted SolidCraft results.

These are user/reference measurements, not official manufacturer geometry.
One physical CI item owns two catalog variants and their expectations.
"""

from cad_verification import (
    BodyEnvelope,
    SolidCraftBodyExpectation,
    SolidCraftModelExpectation,
    SolidCraftVerification,
)


def _case(slug: str, width: float, height: float, volume: float):
    return SolidCraftVerification(
        verification_id=slug,
        baseline=SolidCraftModelExpectation(
            body_count=1,
            body_envelopes=(
                BodyEnvelope((0.0, -300.0, 0.0), (width, 300.0, height)),
            ),
            bounds_tolerance=0.005,
            sketch_count=1,
            named_bodies=(
                SolidCraftBodyExpectation(
                    name_prefix="GuideRail",
                    closed=True,
                    volume_mm3=volume,
                    volume_tolerance=1.0,
                ),
            ),
        ),
    )


VERIFICATIONS = {
    "guide-rail": _case("guide-rail", 184.20, 10.50, 268064.22),
    "guide-rail-makita": _case(
        "guide-rail-makita", 182.50, 10.28, 276769.0773
    ),
}
