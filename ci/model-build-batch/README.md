# Shared model build batch

Released CAD-CI selects and schedules the graph. This producer generates
commands for active model roots, starts the released SolidCraft runtime once,
and writes separate result/provenance folders for each variant. Per-model items
then expose their output through released `copy: dependency`.
