"""Check SamplePlate dimensions and the three named editable sketches."""

from cad_verification import (
    BodyEnvelope,
    SolidCraftModelExpectation,
    SolidCraftVerification,
)


VERIFICATION = SolidCraftVerification(
    verification_id="sample-plate",
    baseline=SolidCraftModelExpectation(
        body_count=1,
        body_envelopes=(
            BodyEnvelope((-40.0, -25.0, 0.0), (40.0, 25.0, 22.0)),
        ),
        bounds_tolerance=0.001,
        sketch_count=3,
    ),
)
