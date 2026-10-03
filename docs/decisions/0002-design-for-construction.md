---
doc_id: RBJ-DDR-002
title: RubbleJack design for construction
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
  change: Changes that make the kit physically buildable, with the reason for each, decided under Amish's 2026-10-03 pre-approval
---

# 0002: Design for construction

- **Date:** 2026-10-03
- **Status:** decided. Amish, 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." This covers every change below.

## Context

The scaffold precis (RBJ-PRC-001 v0.1) described bolt-on spreader and cutter heads on standard cylinders, a ram with base plates and extension tubes, and a pump and hoses, but no part had been checked for how it is made or how it joins the next one. Under Amish's 2026-09-30 instruction ("fix the design assumptions to match and be physically feasible"), the model in `cad/src/model.py` was built as a constructable design: every part has a stated making process and material, every joint has a fixing, and 228 build123d checks confirm that parts which must touch do touch, parts which must not touch stay clear through the whole stroke of each tool, and every screw and pin passes through clear holes. All 228 pass.

The changes keep what the kit does: one hand pump drives a spreader, a cutter and a lifting ram, each carried in a load of 25 kg or less. None of them changes the pitch. Changes C2 and C8 to C10 touch the safety case and take the conservative option.

> **Safety:** These changes make the kit buildable on paper; they do not make it safe to use. Every tool must be proof-loaded on CalRig and inspected before use (RBJ-DDR-001, D9), and the kit is not certified rescue equipment.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Component | The concept had | The constructable design has | Why |
| --- | --- | --- | --- | --- |
| C1 | Spreader and cutter heads | "Bolt-on heads that fit onto standard cylinders", no interface defined | Each head is two frame plates bolted with eight M16 screws to a 7075-T6 collar adapter that screws onto the cylinder's collar thread; one cylinder per tool (RBJ-DDR-001, D2) | The collar thread is the cylinder's own fixture interface; the plates then carry the reaction back to it in plain tension |
| C2 | Spreader frame plates | 12 mm 7075-T6 in the first constructable layout | 10 mm 7075-T6 | Saves 0.4 kg on the heaviest load; the plates still have a margin of 1.82 at the pivot bore with a stress concentration of 2.5 (RBJ-CAL-001, C6) |
| C3 | Spreader pivot | One pin, arms shown overlapping | Arm A has a centre knuckle 18 mm thick and arm B twin knuckles 9 mm thick, interleaved on one 45 mm pin, with a 28 mm spacer each side filling the gap to the plates | Both arms share one pin with no overlap; the spacers stop the arms sliding along the pin |
| C4 | Pins | 4140 quenched and tempered | 4340 quenched and tempered to about 300 HB | Link pin bending margin was 1.35; now 1.76 (C5 in RBJ-CAL-001) |
| C5 | Jaw arm tail | Link slot from 95 mm | Link slot from 100 mm | Raises the tail's margin at the slot from 1.50 to 1.60; the links still clear the slot ends through the whole stroke (checked at nine positions) |
| C6 | Cutter stop bar | 30 mm long, one screw in each plate | 60 mm long, two M16 screws in each plate | With one screw a side each screw had a margin of 1.29 when the carrier lands at full pressure, and the bar could turn; with two a side the margin is 2.59 and it cannot turn |
| C7 | Fixed blade screws | Four M16 at 20 mm spacing | Four M12 at the same positions, 13.5 mm holes in the upper plate | The four M16 heads touched each other; the fixed blade's thrust goes into the nose block in bearing, so the screws only locate it |
| C8 | Ram base plate | 12 mm S355 | 20 mm S690QL with a welded S355 ring | A free plate on an even reaction bends to 931 MPa at 12 mm S355 (margin 0.37); 20 mm S690QL gives 335 MPa (margin 2.06). Conservative choice; relax only with a strain-gauged proof load on cribbing |
| C9 | Riser block | 114.3 x 8 tube between 160 mm plates | 88.9 x 10 tube between the same plates | The tube wall now stands right over the base ring and under the cylinder base, so the end plates carry the load in bearing instead of bending |
| C10 | Ram stack | Base plates and extension tubes, no location | A 15 mm locating ring on the base plate and on the riser's top plate, and a 70 mm spigot under the riser; the riser goes only under the cylinder | Every stacked part is held against sliding sideways; nothing stands on the plunger but the tilting saddle |
| C11 | Crosshead and blade carrier | Not defined | 7075-T6 blocks on an M24 stud into the plunger's attachment thread; the carrier slides between the cutter plates with 0.5 mm each side | The plunger turns freely in its cylinder, so the links and the plates set the angle; the carrier cannot twist |
| C12 | Shear | Not defined | Moving blade (lower half) on the carrier, fixed blade (upper half) held to the upper plate and bearing on a nose block, 0.2 mm apart, both with a 17 mm U notch in line with a 30 mm hook in the plates | Single shear with the bar held in the hook; the carrier lands on the stop bar 30 mm later, after the cut |
| C13 | Jaw arms | Solid plate | 8 mm deep lightening pockets each face, 12 mm in from every edge | Saves 0.84 kg on the spreader (0.42 kg an arm); the bending margins stay at 1.84 or more |
| C14 | Carry handles | Not defined | A 26.9 x 3.2 tube bent to a D, with welded M12 plugs, two M12 screws from under the upper plate | No weld on the aluminium or high-strength plates |

## Consequences

- Masses: spreader 24.0 kg, cutter 21.2 kg, ram set 22.9 kg, pump with gauge and hoses 15.1 kg; with a 0.8 kg bag each, every load is under 25 kg (R6). The spreader has 0.2 kg in hand.
- Cost: lines 12, 14, 15 and 21 changed and line 24 (M12 screws) was added; the estimate is USD 5,895 against the USD 3,500 value-engineering target.
- Drawings and media: STEP and STL regenerated, general arrangement RBJ-DWG-001 Rev P1 and making sketches RBJ-DWG-101 to 118 drawn from the constructable model, concept media refreshed.
- To confirm when parts are bought (RBJ-DEC-001): the collar thread and the load allowed through it, the plunger's attachment thread and that the plunger turns freely, the collapsed length, and the hose burst ratio.
