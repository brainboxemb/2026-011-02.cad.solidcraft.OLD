"""Native SolidCraft acceptance for the lower-compartment HUB75 case."""

from pathlib import Path

from cad_verification import (
    SolidCraftModelExpectation,
    SolidCraftSavedDesign,
    SolidCraftVerification,
)


ROOT = Path(__file__).resolve().parent


VERIFICATION = SolidCraftVerification(
    verification_id="hub75-wood-frame-iter2",
    baseline=SolidCraftModelExpectation(
        parameters={"lower_compartment_height": 70.0},
        parameter_match="subset",
    ),
    saved_designs=(
        SolidCraftSavedDesign(
            id="lower_compartment_90",
            command_path=ROOT / "lower-compartment-90.json",
            expectation=SolidCraftModelExpectation(
                parameters={"lower_compartment_height": 90.0},
                parameter_match="subset",
            ),
        ),
    ),
)
