"""Check that the extruded L bracket remains one editable SolidCraft body."""

from cad_verification import SolidCraftModelExpectation, SolidCraftVerification


VERIFICATION = SolidCraftVerification(
    verification_id="bracket",
    baseline=SolidCraftModelExpectation(
        body_count=1,
        sketch_count=1,
    ),
    metadata={"follow_up": "Add explicit envelope and mounting-hole geometry checks."},
)
