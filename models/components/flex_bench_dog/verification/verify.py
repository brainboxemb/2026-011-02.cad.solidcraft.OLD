"""Physical acceptance for FlexBenchDog, including independent SCPC output."""

from cad_verification import (
    BodyEnvelope,
    SolidCraftBodyExpectation,
    SolidCraftModelExpectation,
    SolidCraftVerification,
)


VERIFICATION = SolidCraftVerification(
    verification_id="flex-bench-dog",
    baseline=SolidCraftModelExpectation(
        body_count=1,
        body_envelopes=(
            BodyEnvelope((-11.0, -11.0, -20.0), (11.0, 11.0, 20.0)),
        ),
        bounds_tolerance=0.005,
        sketch_count=3,
        named_bodies=(SolidCraftBodyExpectation(closed=True),),
    ),
)
