---
doc_id: RBJ-DDR-001
title: RubbleJack TRL 2 review decisions
project: RubbleJack
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: TRL 2 review decisions D1 to D14, decided under Amish's 2026-10-03 pre-approval
---

# 0001: TRL 2 review decisions

- **Date:** 2026-10-03
- **Status:** decided. Amish, 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." Each decision below is the recommendation made at the TRL 2 review and is decided as recommended.

## Context

The scaffold (RBJ-PRC-001 v0.1) described a kit built around one commodity hand pump, with bolt-on spreader and cutter heads on standard cylinders and a lifting ram, and left open how the heads attach, which cylinder class to use, how strong each part must be and how the kit is carried. The TRL 2 review settled these so the TRL 3 calculations (RBJ-CAL-001), the model and the build plan could proceed. Choices that touch safety take the conservative option; each says what evidence would relax it.

> **Safety:** RubbleJack lifts and spreads loads of up to 142 kN with oil at 700 bar, in collapsed structures. These decisions set the design basis on paper only. Nothing here makes the kit safe to use; it is not certified rescue equipment.

## Decisions

*Table 1. TRL 2 review decisions.*

| # | Decision | Reason | Affects |
| --- | --- | --- | --- |
| D1 | Use the commodity 700 bar (10,000 psi) class throughout: a two-speed hand pump with internal relief at 700 bar, single-acting spring-return 15 t cylinders with 101 mm stroke, 700 bar hoses and couplers, and a gauge on the pump outlet | The most widely stocked class of hand hydraulics; two or more makers offer every part (R9); 142 kN per cylinder covers R1, R2 and R4 | BOM lines 1 to 5; every calculation |
| D2 | Give each tool its own cylinder (three identical cylinders) rather than one cylinder with quick-change heads | A tool change becomes one coupler off and one on, about 20 s (R8), with no thread to clean of dust under rubble; the cylinders stay interchangeable as spares. Cost: two more cylinders (USD 840) | BOM line 5; R8; value engineering |
| D3 | Spreader: two jaw arms on one pivot pin, opened by a crosshead on the plunger and two links; 250 mm jaws; spreading only | Simple pinned linkage that local workshops can make; 49 to 64 kN at the tips and 262 mm opening (RBJ-CAL-001 section B). A single-acting cylinder gives no pulling or squeezing force, which is stated on the tool | Spreader parts; R2, R3 |
| D4 | Cutter: a guillotine shear with hardened S7 blades, single shear, rated for reinforcing bar up to 16 mm (B500B or ASTM A615 grade 60) | The cylinder can shear 18.7 mm bar at the upper strength, so a 16 mm rating keeps a ratio of 1.36. Conservative: no hardened bar, chain or larger bar. Relax only after proof cuts on CalRig at TRL 4 | Cutter parts; R4 |
| D5 | Lifting ram: the cylinder stands in a locating ring on a 250 mm base plate; one 150 mm riser may go under it, never on top of the plunger; a tilting saddle on the plunger | Load always passes straight down through located steel; a riser on the plunger is the classic way a ram kicks out | Ram parts; R1, R12 |
| D6 | Materials: 4340 quenched and tempered arms and pins; S690QL links and cutter plates; S7 blades; 7075-T6 aluminium for bulky, lightly stressed parts | High strength where sections are small, aluminium where parts are bulky, so each carried load stays under 25 kg (R6) | Every made part; R6, R11 |
| D7 | Strength rule (new R11): every made load-bearing part has at least 1.5 on yield at the 700 bar relief pressure, on conservative hand calculations | Conservative safety basis while nothing is tested. Relax only with strain-gauged proof loads on CalRig | RBJ-CAL-001; R11 |
| D8 | Publish as an open engineering reference with a not-certified notice naming NFPA 1936, NFPA 1960 and EN 13204 | Follows the patent and standards screen in RBJ-PRC-001 | README, every document, tool markings |
| D9 | Before any tool is used, it is proof-loaded on CalRig at 1.5 times the force at 700 bar and crack-checked; the plan for this is TRL 4 work | Conservative; matches the R1 verification method | First checks in RBJ-BLD-001; TRL 4 |
| D10 | Carry the kit as four loads in tool bags: pump, gauge and hoses; spreader; cutter; lifting ram set | Each stays under 25 kg packed (R6); four people can carry the whole kit | BOM line 23; R6 |
| D11 | The kit requires hardwood cribbing under the ram and next to every lifted load; cribbing is not designed or supplied (stays out of scope), and the documents give guidance on its use | Lifting without cribbing is the main hazard; local timber is widely available | Safety sections; R12 |
| D12 | Co-design: the first candidate partner to approach is a volunteer search and rescue association in southern Turkey (AKUT is the first candidate), with a local hydraulic workshop; first candidate region is the area hit in February 2023. Recorded as a first candidate, not agreed | A region with recent collapse experience, volunteer crews and a strong hydraulic trade | Co-design section of RBJ-PRB-001 |
| D13 | Shared blocks: the commodity hydraulics block (pump, hoses, couplers, gauge) is adopted as a shared block; CalRig is the proof-load rig; VoidScope stays a sibling | Re-use across the portfolio | RBJ-PRC-001 |
| D14 | The gauge stays fitted on the pump outlet whenever the kit is used | Crews see the pressure and stop before the relief valve is the only limit | BOM line 2; safety stops |

## Consequences

- The estimated cost rises above the USD 3,500 value-engineering target, mainly from D2 and D6 (see RBJ-DEC-001, Value engineering). Amish accepted cost overruns in the same instruction.
- R11 and R12 are added to RBJ-REQ-001.
