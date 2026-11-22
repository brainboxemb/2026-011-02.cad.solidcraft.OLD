"""Check the reusable hole-free CornerBracket built in SolidCraft."""

from cad_verification import (
    BodyEnvelope,
    SolidCraftBodyExpectation,
    SolidCraftModelExpectation,
    SolidCraftVerification,
)


VERIFICATION = SolidCraftVerification(
    verification_id="corner-bracket",
    baseline=SolidCraftModelExpectation(
        body_count=1,
        body_envelopes=(
            BodyEnvelope((-12.0, -12.0, -60.0), (60.0, 12.0, 12.0)),
        ),
        bounds_tolerance=0.001,
        named_bodies=(
            SolidCraftBodyExpectation(
                name_prefix="CornerBracket",
                closed=True,
            ),
        ),
    ),
)
