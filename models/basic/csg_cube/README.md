# CSG Cube — Python SCPF comparison

The Python [SCPF model](scpf/model.py) intersects a sphere with a cube
and subtracts three perpendicular cylindrical bores. Each native Cylinder
uses `.at(body)` to place its CENTER on the centered CSG body, so the model
does not manually calculate axis-specific `-size / 2` base coordinates.
Nominal size: 50 mm.

The [reviewed native commands](scpf/reference.json) are regression
fixtures for the SolidCraft Python compiler.

```powershell
python -m scpf models/basic/csg_cube/scpf/model.py --out output/csg-cube.json
code output/csg-cube.json
```

Cross-CAD reference implementations and syntax comparisons are owned by
[Forge](https://github.com/brainboxemb/lib.py.solidcraft.forge). This product
repository retains the SCPF model and its reviewed SolidCraft command fixture.
