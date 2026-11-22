"""Vent Plate physical design contract, independent of Forge/SCPC history.

The editable SolidCraft source defines a 120 x 80 x 4 mm rounded plate
with 18 patterned 6 x 14 mm ventilation cuts. Both independently compiled
sources must satisfy the same dimensions, then match in native body volume.
"""

from cad_verification import (
    BodyEnvelope,
    SolidCraftModelExpectation,
    SolidCraftVerification,
)


VERIFICATION = SolidCraftVerification(
    verification_id="vent-plate",
    baseline=SolidCraftModelExpectation(
        body_count=1,
        body_envelopes=(
            BodyEnvelope((0.0, 0.0, 0.0), (120.0, 80.0, 4.0)),
        ),
        bounds_tolerance=0.001,
    ),
)
