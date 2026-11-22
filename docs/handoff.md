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
- Op `dev-ci` zijn **9 van 16 fysieke modelmappen** al met de oude tussentijdse per-modelroute gebouwd en gecontroleerd (18 catalogusvarianten totaal). Dit is **geen** acceptatie van de beoogde efficiënte CI.
- Forge heeft het referentiepatroon in `cad-ci.yml`, `ci/model-verification-batch/ci.yml`, `scripts/model_verification_batch.py`: één batch en `copy: dependency` voor modelresultaten.
- **Actieve CAD-werkbranch:** `ci/174-shared-build-batch`, gebaseerd op `dev-ci`. Bouw hier de gezamenlijke batch en modelresultaatprojectie, met globs voor modelmappen; houd de 7 nog niet geteste mappen expliciet `process: false`.
- Gebruik de geteste gedeelde Forge-/SCPC-/verificatiepakketten. Test echte SolidCraft-bestanden, STEP, afbeeldingen, afzonderlijke modelcontroles, onafhankelijke SCPC-vergelijkingen en **één** Docker-run per batch. Controleer ook selectieve PR tegenover volledige controle; de selectiviteit van Forge's batch is nog een aandachtspunt in Forge #661.
- Daarna pas de overige modellen migreren, de bouwresultaten/Pages per ontwikkelbranch inrichten en oude Python-planners/publicatiescripts opruimen. Voor de publicatie de bestaande CAD-website vergelijken met de nieuwe.

Werk in logische PR's, vermijd veel kleine commits of extra CI-runs, en documenteer werkelijk uitgevoerde stappen/resultaten in `docs/plan.md`. **Doe de werkzaamheden in de huidige reactie; beloof geen achtergrondwerk.**
