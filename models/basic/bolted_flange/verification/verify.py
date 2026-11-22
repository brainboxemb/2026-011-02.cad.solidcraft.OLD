"""Check the physical bolted flange in SolidCraft.

The expected volume is derived from the two joined cylinders and seven cuts.
The same contract checks both Forge and the separately authored SCPC model.
"""

from math import pi

from cad_verification import (
    BodyEnvelope,
    SolidCraftBodyExpectation,
    SolidCraftModelExpectation,
    SolidCraftVerification,
)


EXPECTED_VOLUME = (
    pi * 50.0**2 * 10.0
    + pi * 22.0**2 * 16.0
    - pi * 12.0**2 * 26.0
    - 6.0 * pi * 4.5**2 * 10.0
)

VERIFICATION = SolidCraftVerification(
    verification_id="bolted-flange",
    baseline=SolidCraftModelExpectation(
        body_count=1,
        body_envelopes=(
            BodyEnvelope((-50.0, -50.0, 0.0), (50.0, 50.0, 26.0)),
        ),
        bounds_tolerance=0.001,
        named_bodies=(
            SolidCraftBodyExpectation(
                name_prefix="Flange",
                closed=True,
                volume_mm3=EXPECTED_VOLUME,
                volume_tolerance=0.01,
            ),
        ),
    ),
)
