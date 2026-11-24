"""Native frame-thickness associativity regression for Hub75DisplayCase."""

from pathlib import Path

from cad_verification import (
    BodyEnvelope,
    SolidCraftBodyGroupExpectation,
    SolidCraftModelExpectation,
    SolidCraftSavedDesign,
    SolidCraftVerification,
)


ROOT = Path(__file__).resolve().parent


BASELINE_BOARDS = (
    BodyEnvelope((-434.0, 0.0, 12.0), (-422.0, 100.0, 374.0)),
    BodyEnvelope((422.0, 0.0, 12.0), (434.0, 100.0, 374.0)),
    BodyEnvelope((-434.0, 0.0, 0.0), (434.0, 100.0, 12.0)),
    BodyEnvelope((-434.0, -10.0, 374.0), (434.0, 110.0, 386.0)),
    BodyEnvelope((-434.0, 100.0, 0.0), (434.0, 109.0, 374.0)),
)

THICK_BOARDS = (
    BodyEnvelope((-440.0, 0.0, 18.0), (-422.0, 100.0, 380.0)),
    BodyEnvelope((422.0, 0.0, 18.0), (440.0, 100.0, 380.0)),
    BodyEnvelope((-440.0, 0.0, 0.0), (440.0, 100.0, 18.0)),
    BodyEnvelope((-440.0, -10.0, 380.0), (440.0, 110.0, 398.0)),
    BodyEnvelope((-440.0, 100.0, 0.0), (440.0, 109.0, 380.0)),
)

BASELINE_BRACKETS = (
    BodyEnvelope((-446.0, 0.0, 326.0), (-374.0, 24.0, 398.0)),
    BodyEnvelope((-446.0, 76.0, 326.0), (-374.0, 100.0, 398.0)),
    BodyEnvelope((374.0, 0.0, 326.0), (446.0, 24.0, 398.0)),
    BodyEnvelope((374.0, 76.0, 326.0), (446.0, 100.0, 398.0)),
    BodyEnvelope((374.0, 0.0, -12.0), (446.0, 24.0, 60.0)),
    BodyEnvelope((374.0, 76.0, -12.0), (446.0, 100.0, 60.0)),
    BodyEnvelope((-446.0, 0.0, -12.0), (-374.0, 24.0, 60.0)),
    BodyEnvelope((-446.0, 76.0, -12.0), (-374.0, 100.0, 60.0)),
)

THICK_BRACKETS = (
    BodyEnvelope((-452.0, 0.0, 338.0), (-380.0, 24.0, 410.0)),
    BodyEnvelope((-452.0, 76.0, 338.0), (-380.0, 100.0, 410.0)),
    BodyEnvelope((380.0, 0.0, 338.0), (452.0, 24.0, 410.0)),
    BodyEnvelope((380.0, 76.0, 338.0), (452.0, 100.0, 410.0)),
    BodyEnvelope((380.0, 0.0, -12.0), (452.0, 24.0, 60.0)),
    BodyEnvelope((380.0, 76.0, -12.0), (452.0, 100.0, 60.0)),
    BodyEnvelope((-452.0, 0.0, -12.0), (-380.0, 24.0, 60.0)),
    BodyEnvelope((-452.0, 76.0, -12.0), (-380.0, 100.0, 60.0)),
)


def _groups(boards, brackets):
    return (
        SolidCraftBodyGroupExpectation(
            name_prefix="Board",
            count=5,
            body_envelopes=boards,
            bounds_tolerance=0.001,
        ),
        SolidCraftBodyGroupExpectation(
            name_prefix="CornerBracket",
            count=8,
            body_envelopes=brackets,
            bounds_tolerance=0.001,
        ),
    )


VERIFICATION = SolidCraftVerification(
    verification_id="hub75-wood-frame",
    baseline=SolidCraftModelExpectation(
        parameters={"frame_wood_thickness": 12.0},
        parameter_match="subset",
        body_groups=_groups(BASELINE_BOARDS, BASELINE_BRACKETS),
    ),
    saved_designs=(
        SolidCraftSavedDesign(
            id="frame_thickness_18",
            command_path=ROOT / "frame-thickness-18.json",
            expectation=SolidCraftModelExpectation(
                parameters={"frame_wood_thickness": 18.0},
                parameter_match="subset",
                body_groups=_groups(THICK_BOARDS, THICK_BRACKETS),
            ),
        ),
    ),
)
