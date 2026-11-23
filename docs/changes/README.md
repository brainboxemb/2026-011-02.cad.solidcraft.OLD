# Change design records

Structural CAD-library changes are recorded here before or together with implementation.

Naming:

```text
NNNN-short-change-name.md
```

Rules:

- four-digit, monotonically increasing number;
- one design/change per document;
- link the matching GitHub issue;
- describe the problem, decision, repository/API/CI contract and verification;
- implementation follows the recorded decision;
- later changes add a new record instead of rewriting an older decision.

Current records:

- [0041-flex-bench-dog-rounded-slot-corners.md](0041-flex-bench-dog-rounded-slot-corners.md) — fillet the four vertical material corners around the FlexBenchDog central cross without changing slot dimensions (#333).
