"""Expected physical Plate geometry, independent of shared checker code."""

from cad_verification import (
    BodyEnvelope,
    SolidCraftModelExpectation,
    SolidCraftVerification,
)


VERIFICATION = SolidCraftVerification(
    verification_id="plate",
    baseline=SolidCraftModelExpectation(
        body_count=1,
        body_envelopes=(
            BodyEnvelope((-50.0, -30.0, 0.0), (50.0, 30.0, 10.0)),
        ),
        bounds_tolerance=0.001,
    ),
)
