"""FlexBenchDog expressed directly as SolidCraft commands."""

from scpc import Script

script = Script()

for name, value in (
    ("hole_diameter", 20.0),
    ("interference", 0.20),
    ("rim_diameter", 22.0),
    ("slot_width", 1.5),
    ("slot_corner_radius", 0.5),
):
    script.add("parameters.add", name=name, expression=str(value), unit="mm")

# MFT stop collar at the worktop datum. The Ø22 × 1.5 mm envelope is
# chamfered on its lower outside edge so the underside returns to Ø20 over
# 1 mm at 45 degrees, leaving a 0.5 mm straight Ø22 land.
script.add(
    "solid.cylinder",
    height=1.5,
    diameter="rim_diameter",
    base=[0, 0, 0],
    axis="Z",
    operation="new",
    body_name="FlexBenchDog",
)
script.add(
    "solid.chamfer",
    body="FlexBenchDog",
    distance=1.0,
    edges=[[11, 0, 0]],
)

# Working section: top of collar to 20 mm above the worktop.
script.add(
    "solid.cylinder",
    height=18.5,
    diameter="hole_diameter",
    base=[0, 0, 1.5],
    axis="Z",
    operation="join",
    targets=["FlexBenchDog"],
)

# Straight 20 mm insert and a slightly oversized free tip.
script.add(
    "solid.cylinder",
    height=20,
    diameter="hole_diameter",
    base=[0, 0, -20],
    axis="Z",
    operation="join",
    targets=["FlexBenchDog"],
)
script.add(
    "solid.cylinder",
    height=2,
    diameter="hole_diameter + interference",
    base=[0, 0, -20],
    axis="Z",
    operation="join",
    targets=["FlexBenchDog"],
)

# Larger lead-in chamfer on the free insert edge.
script.add(
    "solid.chamfer",
    body="FlexBenchDog",
    distance=1.0,
    edges=[[10.1, 0, -20]],
)

# Flex slot X.
script.add(
    "sketch.create",
    plane={"origin": [0, 0, -20], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]},
    name="Flex slot X",
)
script.add(
    "sketch.rectangle.two_point",
    p0=["-(hole_diameter + interference + 2) / 2", "-slot_width / 2"],
    p1=["(hole_diameter + interference + 2) / 2", "slot_width / 2"],
)
script.add("sketch.finish")
script.add(
    "solid.extrude",
    distance=16,
    direction="positive",
    operation="cut",
    targets=["FlexBenchDog"],
    name="Flex slot X",
)

# Flex slot Y.
script.add(
    "sketch.create",
    plane={"origin": [0, 0, -20], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]},
    name="Flex slot Y",
)
script.add(
    "sketch.rectangle.two_point",
    p0=["-slot_width / 2", "-(hole_diameter + interference + 2) / 2"],
    p1=["slot_width / 2", "(hole_diameter + interference + 2) / 2"],
)
script.add("sketch.finish")
script.add(
    "solid.extrude",
    distance=16,
    direction="positive",
    operation="cut",
    targets=["FlexBenchDog"],
    name="Flex slot Y",
)

# Round only the four vertical material edges around the central cross.
script.add(
    "solid.fillet",
    body="FlexBenchDog",
    radius="slot_corner_radius",
    edges=[
        [0.75, 0.75, -12],
        [-0.75, 0.75, -12],
        [-0.75, -0.75, -12],
        [0.75, -0.75, -12],
    ],
)

# Light chamfer on the visible upper perimeter.
script.add(
    "solid.chamfer",
    body="FlexBenchDog",
    distance=0.6,
    edges=[[10, 0, 20]],
)

# Recessed square box logo.
script.add(
    "sketch.create",
    plane={"origin": [0, 0, 20], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]},
    name="Top logo",
)
script.add(
    "sketch.rectangle.two_point",
    p0=[-4, -4],
    p1=[4, 4],
)
script.add("sketch.finish")
script.add(
    "solid.extrude",
    distance=0.6,
    direction="negative",
    operation="cut",
    targets=["FlexBenchDog"],
    name="Top logo",
)
