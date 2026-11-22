# Simple MFT

This model is the reusable worktop plate used by the Simple MFT examples.

## Documentation

The public background, reference basis and photo-derived measurement assumptions
are maintained in [page.md](page.md). The common model description and website
catalogue fields remain in [model.yml](model.yml).

The implementation itself lives in `scpf/model.py`. The guide-rail assembly
example lives in `scpf/assemblies/guide_rail.py`.

## Model boundary

The standalone `SimpleMFT` is the worktop-only reusable component. The
`simple-mft-assembly` variant combines that same worktop definition with the
generic `GuideRail` component.

The current assembly is a layout model. Rail dogs, support hardware, fence,
frame/legs and clamps are outside its current scope.

## Run

```powershell
python -m scpf models/advanced/simple_mft/scpf/model.py --out output/simple-mft.json
python -m scpf models/advanced/simple_mft/scpf/model.py --connect --new
```
