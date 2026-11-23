# CAD repository handoff

Repository: `brainboxemb/2026-011-02.cad.solidcraft`.

This is the normal session entrypoint. It is intentionally kept under
`docs/handoff.md` so it is easy to find.

The copy block below is deliberately Dutch because it is intended to be pasted
into the user's Dutch-language ChatGPT session. Repository engineering
documentation remains English.

## Handoff message

Copy the complete text block below into a new chat.

~~~text
Je werkt verder aan de product-CAD repository
`brainboxemb/2026-011-02.cad.solidcraft`.

Gebruik deze handoff alleen als ingang. Bepaal de actuele werkzaamheden altijd
opnieuw uit GitHub en `docs/plan.md`; behandel een gekopieerde handoff nooit
als actueler dan die bronnen.

Begin zo:

1. inspecteer de actuele issues, PR's en branches;
2. lees `AGENTS.md` en `docs/plan.md`;
3. behandel `docs/plan.md` als source of truth voor onafgemaakt werk;
4. volg de actuele werkvolgorde uit het plan;
5. maak een issue voordat je een logische wijziging implementeert als die nog
   geen issue heeft;
6. houd één logische wijziging bij één issue, branch en PR;
7. werk `docs/requirements.md` en `docs/design.md` bij als gedrag of
   architectuur verandert;
8. behandel `dev-cad` en `dev-ci` als echte werklanes: meerdere afgeronde
   wijzigingen mogen daar blijven staan; promoveer niet na iedere PR naar
   `main`, maar pas op een bewust stabiel checkpoint;
9. pure repository-instructies en documentatiecorrecties in `AGENTS.md` en
   `docs/*` mogen rechtstreeks op `main`; documentatie die onderdeel is van
   een code/modelwijziging blijft bij de bijbehorende issue/branch/PR;
10. reconcileer het plan na een permanente-lane promotie/synchronisatie of
    andere wijziging die de geaccepteerde baseline verandert.

Repositoryrol:

- deze repository bezit product- en project-CAD modellen, model-specifieke
  verwachtingen, varianten, dependencies en de gepubliceerde CAD-catalogus;
- Forge (`lib.py.solidcraft.forge`) bezit herbruikbare CAD-API,
  compiler/lowering en generieke modellering;
- generieke CAD-CI hoort in `lib.py.cad.ci` / `tool.cad.ci`;
- generieke verificatie hoort in `lib.py.cad.verification`;
- runtime/container packaging hoort in `docker.cad.solidcraft`;
- voeg geen CAD-lokale workaround toe voor een generiek Forge-, CI-,
  verificatie- of runtimeprobleem.

Permanente lanes, merge/promotion-regels, actuele blockers, exacte versies,
SHAs en issuevolgorde staan in `AGENTS.md`, `docs/plan.md` en GitHub.
Dupliceer die actuele status niet in deze handoff.

Gedeelde SolidCraft/CAD documentstructuren staan in
`brainboxemb/meta.cad.solidcraft`:
`templates/docs/plan.md` en `templates/docs/handoff.md`.
~~~
