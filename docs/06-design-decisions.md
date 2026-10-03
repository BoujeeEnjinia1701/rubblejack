---
doc_id: RBJ-DEC-001
title: RubbleJack design decisions register
project: RubbleJack
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: Register opened at TRL 3; every decision made under Amish's 2026-10-03 pre-approval
---

# RubbleJack design decisions register

Every design decision made, and everything still to confirm, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands.

> **Safety:** RubbleJack is a safety-critical lifting, spreading and cutting kit working at 700 bar. Every decision that touches safety took the conservative option, and the evidence that would relax it is named in its record. Nothing here makes the kit certified rescue equipment.

## Open decisions

None. All decisions were made under Amish's 2026-10-03 pre-approval.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The cylinder's collar thread size and length, and that the maker allows the full 15 t through the collar thread | The collar adapters are cut to match it; the spreader and cutter react their whole force through it | RBJ-DDR-002, C1 |
| 2 | The plunger's attachment thread, and that the plunger turns freely in the cylinder | Sets the stud size for the crosshead and carrier; the tools rely on the links and plates to set the plunger's angle | RBJ-DDR-002, C11 |
| 3 | The cylinder's collapsed length (216 mm assumed), stroke and effective area | Set the spreader linkage geometry, the frame plate length and every force | RBJ-CAL-001, A and B |
| 4 | Hose burst rating at least 4 to 1 and all couplers of one series | R5; couplers of mixed series may not seal or lock | RBJ-CAL-001, A |
| 5 | Pump stage volumes, relief setting and handle effort | Stroke counts and times in RBJ-CAL-001, F; the 700 bar limit | RBJ-CAL-001, F |
| 6 | Mill certificates for S690QL and 7075-T6 plate, and hardness after heat treatment of the 4340 and S7 parts | Every strength margin uses minimum yield values | RBJ-CAL-001, C to E |

## Value engineering

Value-engineering target: USD 3,500 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 5,895 (USD 2,395 over the target). Made parts are about USD 3,030 and bought parts about USD 2,865. Main cost drivers and savings worth trying:

- The three cylinders (USD 1,260) are the largest line. One cylinder per tool (D2) costs USD 840 more than a single shared cylinder; sharing one cylinder with heads screwed onto its collar would save that, at the cost of a slower tool change (over 1 minute, so R8 would be missed) and threads exposed to dust.
- The two jaw arms (USD 900) are machined from quenched and tempered 4340 plate. Waterjet cutting of pre-hardened plate with only the bores and knuckles machined is the saving worth pricing first.
- The pump (USD 650), the hoses (USD 420) and the S7 blades (USD 440 the pair) follow. Prices are indicative; local workshops in the first candidate region may be much cheaper for the made parts, and a second quote should be sought before TRL 4.
- Design for construction added the M12 screws (line 24) and raised the base plate to 20 mm high-strength steel; together about USD 30.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-03 | TRL 2 review items D1 to D14: commodity 700 bar hydraulics, one 15 t cylinder per tool, linkage spreader, guillotine cutter rated for 16 mm bar, located ram stack, materials, the 1.5 on yield strength rule (R11), not-certified notice, proof load before use, four carried loads, required cribbing (R12), shared blocks, gauge always fitted | Amish: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." | [RBJ-DDR-001](decisions/0001-trl2-review-decisions.md) |
| 2026-10-03 | Co-design: the first candidate partner to approach is a volunteer search and rescue association in southern Turkey (AKUT first), in the region hit in February 2023; a first candidate, not agreed | Amish, same pre-approval | [RBJ-DDR-001](decisions/0001-trl2-review-decisions.md), D12 |
| 2026-10-03 | Design for construction C1 to C14: collar adapters, 10 mm frame plates, interleaved pivot, 4340 pins, link slot from 100 mm, stop bar with two screws in each plate, M12 fixed blade screws, 20 mm S690QL base plate, 88.9 mm riser tube, locating rings and spigot, stud-mounted crosshead and carrier, shear layout, lightening pockets, bolted handles | Amish, same pre-approval | [RBJ-DDR-002](decisions/0002-design-for-construction.md) |
| 2026-10-03 | Cost overrun against the value-engineering target accepted; `budget_usd` left at USD 3,500 | Amish, same pre-approval ("I also accept any cost overruns") | This register, Value engineering |
