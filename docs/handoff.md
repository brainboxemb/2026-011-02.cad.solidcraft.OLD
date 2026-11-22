# Handoff — CAD-repository (nieuwe chat)

**Werk uitsluitend in `brainboxemb/2026-011-02.cad.solidcraft`.**
Hoofdissue: [#174](https://github.com/brainboxemb/2026-011-02.cad.solidcraft/issues/174); volledige 0.45/Forge 0.11 controle: #172.
Algemene CI-wensen en architectuurbesluiten lopen **via Forge-issues** (momenteel [Forge #661](https://github.com/brainboxemb/lib.py.solidcraft.forge/issues/661)); wijzig generieke libraries niet vanuit deze CAD-chat.

## Afgesproken architectuur
- Hergebruik Forge's vrijgegeven `tool.cad.ci` + `lib.py.cad.ci`: **eenmalig ontdekken → plannen met SCons → gedeelde SolidCraft-bouwgroep → resultaten per model**.
- Gebruik één SolidCraft-containerstart voor de bouwgroep; geen Docker-start, eigen selectiemotor of eigen publicatiesysteem **per model**.
- Eén eenvoudige `ci.yml` per model: `id`, `template`, `process`; root-templates en gedeelde batch regelen de uitvoering.
- `lib.py.cad.verification` controleert de modellen; onafhankelijke Forge/SCPC-versies blijven vergelijkbaar. Zeg **bouwen**, **controleren**, **bouwresultaten** (Engels `build`, `verify`, `results`), niet het onduidelijke woord dat daarvoor gebruikt werd. Bestaande technische opslagpaden alleen met compatibiliteitscontrole wijzigen.
- Behoud de bestaande openbare CAD-website qua navigatie, modelpagina's, afbeeldingen, downloads en URL's. **Niet** de website van Forge overnemen.
- Bronbranches `main`, `dev-cad`, `dev-ci`; ontwikkeling via squash-PR's naar de juiste ontwikkelbranch. `main`/openbare Pages ongewijzigd tot de migratie aantoonbaar werkt.

## Feitelijke status en hervatten
- De centrale SolidCraft-container is al in gebruik; Forge 0.11 en SolidCraft 0.45 zijn gepind. De oude `main`-workflow werkt maar bouwde bij de upgrade **niet alle modellen**.
- **PR #184 is met squash gemerged op `dev-ci`** (`670960db48c80317a37f72bc1ea0a62a09595090`): één gedeelde SolidCraft-bouwgroep volgens Forge's `copy: dependency`-patroon. Alle **9 ingeschakelde modelmappen** zijn in één containerstart gebouwd en gecontroleerd; 7 andere mappen zijn bewust `process: false` (16 mappen, 18 catalogusvarianten).
- Bewijs uit #184: **13/13 SCons-doelen geslaagd**, negen modelcontroles geslaagd, vier onafhankelijke Forge/SCPC-vergelijkingen geslaagd, `docker_run_count=1`, gezamenlijke bouwgroep **29,843 s** (inclusief 8,791 s image pull).
- Root-`cad-ci.yml` ontdekt automatisch `models/basic/*`, `models/components/*` en `models/advanced/*`; model-`ci.yml` bevat alleen `id`, `template`, `process`. De exacte vrijgegeven stack is `tool.cad.ci 0.17.1` / `lib.py.cad.ci 0.10.0`; Forge/SCPC/controleroutines blijven externe afhankelijke pakketten.
- **Vervolg in CAD:** bewijs documentatie-only selectie en een gewijzigde modelbron; sluit daarna de overige zeven modelmappen en twee extra catalogusvarianten aan, controleer STEP/afbeeldingen/vergelijkingen, richt build/Pages per bronbranch in en vergelijk de website vóór promotie. Selectiviteit *binnen* de gezamenlijke batch is nog een generieke vraag in Forge #661.
- Daarna pas de overige modellen migreren, de bouwresultaten/Pages per ontwikkelbranch inrichten en oude Python-planners/publicatiescripts opruimen. Voor de publicatie de bestaande CAD-website vergelijken met de nieuwe.

Werk in logische PR's, vermijd veel kleine commits of extra CI-runs, en documenteer werkelijk uitgevoerde stappen/resultaten in `docs/plan.md`. **Doe de werkzaamheden in de huidige reactie; beloof geen achtergrondwerk.**
