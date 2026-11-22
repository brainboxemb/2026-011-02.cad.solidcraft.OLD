"""Check the shelled plastic enclosure can be built in SolidCraft."""

from cad_verification import (
    SolidCraftBodyExpectation,
    SolidCraftModelExpectation,
    SolidCraftVerification,
)


VERIFICATION = SolidCraftVerification(
    verification_id="plastic-enclosure",
    baseline=SolidCraftModelExpectation(
        body_count=1,
        named_bodies=(SolidCraftBodyExpectation(closed=True),),
    ),
    metadata={"follow_up": "Preserve the existing seven-feature construction-history check."},
)
