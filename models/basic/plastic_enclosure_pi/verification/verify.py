"""Check physical Pi enclosure dimensions, body and four named sketches."""

from cad_verification import (
    BodyEnvelope,
    SolidCraftBodyExpectation,
    SolidCraftModelExpectation,
    SolidCraftVerification,
)


VERIFICATION = SolidCraftVerification(
    verification_id="plastic-enclosure-pi",
    baseline=SolidCraftModelExpectation(
        body_count=1,
        body_envelopes=(
            BodyEnvelope((-47.5, -33.0, 0.0), (47.5, 33.0, 24.0)),
        ),
        bounds_tolerance=0.001,
        sketch_count=4,
        named_bodies=(
            SolidCraftBodyExpectation(
                name_prefix="PlasticEnclosurePi",
                closed=True,
            ),
        ),
    ),
    metadata={"follow_up": "Add checks for four bosses and PETG material assignment."},
)
