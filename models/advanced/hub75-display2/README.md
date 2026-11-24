# Hub75DisplayCase v2

Hub75DisplayCase v2 is the second HUB75 enclosure design. It is developed
**in parallel** with the existing
[Hub75DisplayCase](../hub75_wood_frame/README.md).

v2 started from the verified v1 geometry as a comparison baseline, then added
the lower storage compartment and deeper cabinet design from #154. It owns its
own model-local source tree and does not import v1 assemblies.

Reusable physical parts remain shared from `models/components/`, including
`Hub75PanelBasic` and `CornerBracket`.

## Lower storage compartment

The v2 vertical stack is:

| Section | Height |
| --- | ---: |
| Bottom board | 12 mm |
| Clear lower compartment | 70 mm |
| Intermediate shelf | 12 mm |
| Display opening | 362 mm |
| Roof board | 12 mm |
| **Total cabinet height** | **468 mm** |

The display opening starts at **Z=94 mm**. The five HUB75 panels, glazing frame
and plexiglass all use that derived datum.

`lower_compartment_height` is an editable native SolidCraft parameter.
Changing it moves the intermediate shelf, display opening, roof, rear-board
height and top CornerBrackets together while Z=0 remains the outside bottom
datum.

Two 12 mm vertical dividers split the free lower width **30 / 40 / 30%**.
With the default 844 mm opening this gives **246 / 328 / 246 mm** clear bays,
with divider centre-lines at X=-170 mm and X=+170 mm.

## Hand openings and rear board

The side walls are 120 mm deep and use one native 30 mm wide vertical hand
slot per side:

- R15 ends;
- 20 mm rear-edge clearance;
- Y=70..100 mm;
- global hand-zone extent preserved from the accepted #154 geometry.

The inset 9 mm rear board occupies Y=111..120 and starts at Z=82 mm. It uses
two open 50 mm deep, R20 side cutouts rather than closed slots.

## Main dimensions

| Item | Value |
| --- | ---: |
| Opening | 844 × 362 mm |
| Lower compartment clear height | 70 mm |
| Lower bays | 246 / 328 / 246 mm |
| Lower divider plates | 2 × 12 mm |
| Panel count / pitch | 5 / 160 mm |
| Panel recess | 25 mm |
| Frame wood | 12 mm |
| Cabinet / side depth | 120 mm |
| Rear board | 9 mm, inset Y=111..120, starts Z=82 |
| Side hand slot | 30 mm, R15 |
| Roof total depth | 131 mm |
| Window | 840 × 360 × 4 mm |
| Corner brackets | 8 |

World axes remain X left/right, Y front/back and Z up.
