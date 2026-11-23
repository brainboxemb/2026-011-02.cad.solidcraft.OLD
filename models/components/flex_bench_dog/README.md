# Flex bench dog

Reusable 3D-printable bench dog for a **20 mm MFT dog hole**.

The model uses a functional CAD orientation: the worktop surface is **Z=0**,
with **20 mm above and 20 mm below** the worktop. Print orientation is
deliberately not encoded in the model.

## Passive clamping

There is no screw mechanism.

The main insert is nominally **20.00 mm**. At the free end, the final 2 mm
flares to **20.20 mm**. Two 1.5 mm crossing slots split the lower 16 mm into
four flexible legs. The four material corners around the central cross use
**R0.5 mm** vertical fillets, matching the softly rounded underside reference
instead of leaving sharp 90° corners. Those free ends can spring inward when
inserted into the hole, providing passive tension without separate hardware.

The initial **0.20 mm** flare is a prototype value. The useful fit will depend
on the actual dog-hole diameter, printer, filament and print settings.

## Shape

- **20 mm** insertion below the worktop;
- **20 mm** overall body height above the worktop, including the 1.5 mm collar;
- Ø22 × 1.5 mm MFT stop collar with a 1.0 mm 45° underside seat chamfer back to Ø20;
- light **0.6 mm chamfer** around the upper edge;
- larger **1.0 mm chamfer** on the lower insertion edge as a lead-in;
- recessed **BrainBox cube/box wireframe** in the top face: six perimeter strokes plus three centre spokes;
- 2 mm long flared flex tips;
- 16 mm flex slots, leaving 4 mm solid material below the rim.

## Initial dimensions

| Parameter | Default |
| --- | ---: |
| Dog-hole diameter | 20.00 mm |
| Tip flare / interference | 0.20 mm |
| Height above worktop | 20 mm |
| Insertion length | 20 mm |
| Stop-collar diameter | 22 mm |
| Stop-collar axial zone | 1.5 mm |
| Stop-collar seat chamfer | 1.0 mm at 45° |
| Flared tip length | 2 mm |
| Cross-slot width | 1.5 mm |
| Cross-slot length | 16 mm |
| Central slot-corner fillet | R0.5 mm |
| Top chamfer | 0.6 mm |
| Bottom lead-in chamfer | 1.0 mm |
| Logo line width | 0.6 mm |
| Logo depth | 0.6 mm |

The physical body spans **40 mm** from the bottom of the insert to the top
face. That is intentionally slightly longer than an 18 mm worktop; the insert
does not need to stop flush with the underside.

## Top mark

The top mark is not a filled square. It is the preserved recessed BrainBox
cube/box wireframe: six outer segments plus three spokes meeting at the centre.
Each visible cube rib is a separate 0.6 mm-wide closed polygon strip, recessed
0.6 mm into the top face. The strips overlap only at their cube vertices; the
three projected cube faces remain material rather than becoming filled cuts.

## Source and confidence

The overall construction is inferred from the supplied Mini-MFT image. The
nominal 20 mm dog-hole size and the current symmetric 20/20 mm proportions are
project decisions. The collar profile follows the supplied MFT reference and nominal Ø20 hole with a
small 45° mouth chamfer. Flex-slot dimensions, the R0.5 inner-corner relief and the 0.20 mm tip flare
have not yet been verified by a physical fit test.

After a first print, the first value to tune is `interference`, followed by
`slot_width` if more or less spring movement is needed.
