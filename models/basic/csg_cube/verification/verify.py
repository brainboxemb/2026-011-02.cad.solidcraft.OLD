"""Check that the cube/sphere intersection builds as one SolidCraft body."""

from cad_verification import SolidCraftModelExpectation, SolidCraftVerification


VERIFICATION = SolidCraftVerification(
    verification_id="csg-cube",
    baseline=SolidCraftModelExpectation(body_count=1),
    metadata={"follow_up": "Add detailed boolean geometry and volume checks."},
)
