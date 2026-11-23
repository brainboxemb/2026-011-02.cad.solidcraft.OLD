"""CornerBracket expressed independently as native SolidCraft commands."""
from scpc import Script

script = Script()
for name, value in (
    ("arm_width", 24),
    ("arm_height", 12),
    ("horizontal_arm_length", 60),
    ("vertical_arm_length", 60),
    ("arm_end_chamfer", 3),
    ("outer_corner_chamfer", 6),
    ("inside_corner_radius", 4),
    ("elephant_foot_relief", 0.6),
    ("side_edge_chamfer", 2),
    ("plywood_thickness", 12),
    ("bolt_offset", 12),
    ("bolt_spacing", 18),
    ("bolt_y_offset", 0),
    ("bolt_diameter", 5),
    ("bolt_clearance", 0.4),
    ("head_diameter", 10),
    ("head_clearance", 0.4),
    ("head_recess", 1),
    ("bolt_hole_edge_relief", 0.2),
):
    script.add("parameters.add", name=name, expression=str(value), unit="mm")

# OpenSCAD base_profile_2d() including the two 0.6 mm arm-tip reliefs.
script.add("sketch.create", plane="XZ", name="Profile")
script.add(
    "sketch.line",
    points=[
        [0, 0],
        ["horizontal_arm_length - elephant_foot_relief", 0],
        ["horizontal_arm_length", "-(elephant_foot_relief)"],
        ["horizontal_arm_length", "-(arm_height - arm_end_chamfer)"],
        ["horizontal_arm_length - arm_end_chamfer", "-(arm_height)"],
        ["-(arm_height) + outer_corner_chamfer", "-(arm_height)"],
        ["-(arm_height)", "-(arm_height - outer_corner_chamfer)"],
        ["-(arm_height)", "-(-(vertical_arm_length) + arm_end_chamfer)"],
        ["-(arm_height) + arm_end_chamfer", "-(-(vertical_arm_length))"],
        ["-(elephant_foot_relief)", "-(-(vertical_arm_length))"],
        [0, "-(-(vertical_arm_length) + elephant_foot_relief)"],
    ],
    closed=True,
    ids=[
        "i_corner",
        "tip_hor_relief",
        "o_hor_tip",
        "o_hor_bevel",
        "o_hor",
        "o_corner",
        "o_vert",
        "o_vert_bevel",
        "o_vert_end",
        "tip_vert_relief",
        "v_tip",
    ],
)
script.add("sketch.finish")
script.add(
    "solid.extrude",
    distance="arm_width",
    direction="symmetric",
    body_name="CornerBracket",
)

script.add(
    "solid.fillet",
    edges=[[0, 0, 0]],
    radius="inside_corner_radius",
    body="CornerBracket",
)

# Reference pick points for the seven normal outside profile segments on each
# broad face. The two 0.6 mm tip-relief diagonals are intentionally excluded:
# a 2 mm chamfer on those tiny faces causes a native trim leak.
outside_edges = [
    [60, -12, 4.8],
    [58.5, -12, 10.5],
    [25.5, -12, 12],
    [-9, -12, 9],
    [-12, -12, -25.5],
    [-10.5, -12, -58.5],
    [-4.8, -12, -60],
    [60, 12, 4.8],
    [58.5, 12, 10.5],
    [25.5, 12, 12],
    [-9, 12, 9],
    [-12, 12, -25.5],
    [-10.5, 12, -58.5],
    [-4.8, 12, -60],
]
script.add(
    "solid.chamfer",
    edges=outside_edges,
    distance="side_edge_chamfer",
    body="CornerBracket",
)
script.add(
    "solid.chamfer",
    edges=[[29.7, -12, 0], [29.7, 12, 0]],
    distance="elephant_foot_relief",
    body="CornerBracket",
)


def add_bolt_seat(outside, direction, countersink_entry, inside, inside_direction):
    """Append the four native cuts that make one preserved M5 fixing seat."""
    script.add(
        "solid.hole",
        position=outside,
        targets=["CornerBracket"],
        diameter="head_diameter + head_clearance",
        depth="head_recess",
        direction=direction,
    )
    script.add(
        "solid.hole",
        position=countersink_entry,
        targets=["CornerBracket"],
        diameter="bolt_diameter + bolt_clearance",
        depth="arm_height - head_recess",
        direction=direction,
        type="countersink",
        cs_diameter="head_diameter + head_clearance",
        cs_angle=90,
    )
    script.add(
        "solid.hole",
        position=outside,
        targets=["CornerBracket"],
        diameter="head_diameter + head_clearance + 2 * bolt_hole_edge_relief",
        depth="bolt_hole_edge_relief",
        direction=direction,
    )
    script.add(
        "solid.hole",
        position=inside,
        targets=["CornerBracket"],
        diameter="bolt_diameter + bolt_clearance + 2 * bolt_hole_edge_relief",
        depth="bolt_hole_edge_relief",
        direction=inside_direction,
    )


for x in (24, 42):
    add_bolt_seat(
        [x, 0, 12],
        [0, 0, -1],
        [x, 0, 11],
        [x, 0, 0],
        [0, 0, 1],
    )

for z in (-24, -42):
    add_bolt_seat(
        [-12, 0, z],
        [1, 0, 0],
        [-11, 0, z],
        [0, 0, z],
        [-1, 0, 0],
    )
