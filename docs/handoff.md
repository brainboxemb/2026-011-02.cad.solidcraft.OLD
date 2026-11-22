# Handoff — CAD-repository (nieuwe chat)

**Werk uitsluitend in `brainboxemb/2026-011-02.cad.solidcraft`.**
Hoofdissue: [#174](https://github.com/brainboxemb/2026-011-02.cad.solidcraft/issues/174); volledige 0.45/Forge 0.11 controle: #172.
Forge is de centrale CAD-library. Generieke CAD-CI-, verificatie- en runtimebesluiten horen bij hun eigen repositories; Forge #661 levert alleen Forge-consumerbewijs voor batchselectiviteit. Maak vanuit deze CAD-repo geen lokale workaround en verplaats productmodelregistratie niet naar Forge.

## Afgesproken architectuur
- Hergebruik Forge's vrijgegeven `tool.cad.ci` + `lib.py.cad.ci`: **eenmalig ontdekken → plannen met SCons → gedeelde SolidCraft-bouwgroep → resultaten per model**.
- Gebruik één SolidCraft-containerstart voor de bouwgroep; geen Docker-start, eigen selectiemotor of eigen publicatiesysteem **per model**.
- Eén eenvoudige `ci.yml` per fysiek modelroot: `id`, `template`, `process`; root-templates en gedeelde batch regelen de uitvoering. `model_catalog.py` blijft de productregistratie voor varianten/dependencies/site-metadata en is géén generieke CI-registry.
- `lib.py.cad.verification` controleert de modellen; onafhankelijke Forge/SCPC-versies blijven vergelijkbaar. Zeg **bouwen**, **controleren**, **bouwresultaten** (Engels `build`, `verify`, `results`), niet het onduidelijke woord dat daarvoor gebruikt werd. Bestaande technische opslagpaden alleen met compatibiliteitscontrole wijzigen.
- Behoud de bestaande openbare CAD-website qua navigatie, modelpagina's, afbeeldingen, downloads en URL's. **Niet** de website van Forge overnemen.
- Bronbranches `main`, `dev-cad`, `dev-ci`; ontwikkeling via squash-PR's naar de juiste ontwikkelbranch. `main`/openbare Pages ongewijzigd tot de migratie aantoonbaar werkt.

## Feitelijke status en hervatten
- De centrale SolidCraft-container is al in gebruik; Forge 0.11 en SolidCraft 0.45 zijn gepind. De oude `main`-workflow werkt maar bouwde bij de upgrade **niet alle modellen**.
- **PR #184 en #186 zijn met squash gemerged op `dev-ci`** (huidig akkoord: `75ea0fb6db0459872255b7f51e9ae506b9ed7f4c`). Eén gedeelde SolidCraft-bouwgroep volgens Forge's `copy: dependency`-patroon. **11 modelmappen / 12 varianten** zijn in één containerstart gebouwd en gecontroleerd; de resterende 5 mappen blijven `process: false` (16 mappen, 18 catalogusvarianten).
- Bewijs uit #186: **15/15 SCons-doelen**, 12 modelcontroles, vijf onafhankelijke Forge/SCPC-vergelijkingen geslaagd, `docker_run_count=1`, gezamenlijke bouwgroep **31,760 s** (inclusief 7,434 s image pull). GuideRail bevat Festool én Makita als twee varianten in één CI-item.
- Root-`cad-ci.yml` ontdekt automatisch `models/basic/*`, `models/components/*` en `models/advanced/*`; model-`ci.yml` bevat alleen `id`, `template`, `process`. De exacte vrijgegeven stack is `tool.cad.ci 0.17.1` / `lib.py.cad.ci 0.10.0`; Forge/SCPC/controleroutines blijven externe afhankelijke pakketten.
- **Vervolg in CAD:** documentatie-only PR **#185** liet de modelbouw correct achterwege. Controleer nog een enkel gewijzigd model en de invloed op de batch; sluit daarna de vijf resterende modelmappen / zes varianten aan, versterk de individuele modelcontroles, richt build/Pages per bronbranch in en vergelijk de website vóór promotie. Let op: een wijziging aan één actief model kan nu nog de **hele ingeschakelde bouwgroep** opnieuw uitvoeren; Forge #661 meet dit aan de Forge-kant. Als generieke fijnere selectiviteit nodig blijkt, hoort de wijziging in de CAD-CI-eigenaar, niet in Forge of deze consumer.
- Daarna pas de overige modellen migreren, de bouwresultaten/Pages per ontwikkelbranch inrichten en oude Python-planners/publicatiescripts opruimen. Voor de publicatie de bestaande CAD-website vergelijken met de nieuwe.

Werk in logische PR's, vermijd veel kleine commits of extra CI-runs, en documenteer werkelijk uitgevoerde stappen/resultaten in `docs/plan.md`. **Doe de werkzaamheden in de huidige reactie; beloof geen achtergrondwerk.**
