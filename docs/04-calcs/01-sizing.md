---
doc_id: RBJ-CAL-001
title: RubbleJack sizing calculations
project: RubbleJack
doc_type: Calculation
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-03'
  author: Amish Chadha
  change: First issue for TRL 3 on the constructable design (RBJ-DDR-002); hydraulics, spreader linkage and strength, cutter, lifting ram, pump, masses, cost and results against every requirement
---

# RubbleJack sizing calculations

The kit meets every requirement on paper at the pump's 700 bar relief pressure: 142 kN per cylinder, 49 to 64 kN at the spreader tips over a 262 mm opening, 16 mm bar sheared with a ratio of 1.36, 14.5 t at the ram, four loads under 25 kg and every made load-bearing part at least 1.60 on yield. The estimated cost is USD 2,395 over the USD 3,500 value-engineering target.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that any part of RubbleJack is safe to load. Hydraulic oil at 700 bar, loads of 142 kN and collapsed structures can kill. Every made tool must be proof-loaded on CalRig at 1.5 times the force at 700 bar and crack-checked before any use (RBJ-DDR-001, D9). See RBJ-PRC-001, Safety.

## Scope and method

`docs/04-calcs/sizing.py` computes every number below; tags in brackets (for example [B1]) match its printed lines, and it writes `docs/04-calcs/results.csv`. It imports the parameters, the spreader kinematics and the part masses from `cad/src/model.py`, so the geometry is the geometry in the STEP files and drawings. Costs come from `bom/bom.csv`. Strength checks are hand calculations with minimum yield values; a check passes at 1.5 or more on yield (R11). Nothing is measured.

## Assumptions

- The highest pressure anywhere is the pump's internal relief, 700 bar; the gauge lets the operator stop below it.
- Cylinder effective area 20.3 cm² (15 t class, 101 mm stroke); the force is 142.1 kN [A1].
- Minimum yield strengths: 4340 quenched and tempered to about 300 HB, 850 MPa; S690QL, 690 MPa; 7075-T6 thick plate, 430 MPa; 7075-T6 10 mm plate, 500 MPa; S355, 345 MPa; class 12.9 screws in shear, 0.58 of 1,100 MPa.
- Reinforcing bar: tensile strength up to 650 MPa (upper bound for B500B and ASTM A615 grade 60), shear strength 0.8 of that.
- Pin friction in the linkage ignored for forces (it lowers them by a few percent); estimated at 8 % in the energy flow.
- Pump: 0.9 cm³ a stroke in the slow stage, 3.6 cm³ in the fast stage, 900 cm³ usable oil, 380 N handle effort at 700 bar (catalogue class values); a tired person keeps up 25 strokes a minute (estimate).
- Carry bags 0.8 kg each.

## A. Hydraulics (R1, R5)

One cylinder gives 142.1 kN (14.5 t) at 700 bar [A1]. A full stroke takes 205 cm³ of oil, well inside the pump's 900 cm³ [A2]; only one tool is coupled at a time, and the three together would take 615 cm³ [F3]. Every pressurised part is specified at 700 bar working, the hoses at 4 to 1 burst (2,800 bar), and the gauge reads to 1,000 bar, so R5 is met by specification; the ratings are checked on the makers' sheets when parts are bought.

## B. Spreader linkage (R2, R3)

The crosshead pushes two links; each link pushes the tail of a jaw arm 160 mm behind the pivot, 40° below the cylinder axis. By virtual work the force between the tips is the cylinder force times the crosshead's travel per radian of jaw turn, divided by twice the 250 mm jaw length.

*Table 1. Spreader opening and force at 700 bar [B1].*

| Plunger travel (mm) | Jaw turn (deg) | Tip opening (mm) | Force between the tips (kN) |
| --- | --- | --- | --- |
| 0 | 0.0 | 32 | 48.6 |
| 25 | 7.8 | 99 | 56.0 |
| 50 | 14.7 | 158 | 60.9 |
| 75 | 21.2 | 211 | 63.6 |
| 101 | 27.8 | 262 | 64.1 |

The force rises as the jaws open because the links turn toward square with the tails. R2 (40 kN) is met over the whole opening, and R3 (250 mm) is met with 262 mm [B2]. The tips are 32 mm thick closed, so they need a gap of about 32 mm to start; a crew opens a starting gap with the ram or a pry bar. The largest link force is 115 kN, at full stroke, with the link at 52° to the cylinder axis [B3].

## C. Spreader strength (R11)

*Table 2. Spreader parts at 700 bar.*

| Part | Load case | Stress | Margin on yield | Tag |
| --- | --- | --- | --- | --- |
| Jaw arm, 60 mm from the pivot | 64.1 kN at the tip, solid section 70 mm deep | 416 MPa | 2.04 | [C1] |
| Jaw arm, 100 mm from the pivot | As above, 62 mm deep with both pockets | 461 MPa | 1.84 | [C1] |
| Jaw arm, 150 mm from the pivot | As above, 51 mm deep with both pockets | 436 MPa | 1.95 | [C1] |
| Jaw arm tail at the link slot | Tail moment at 100 mm, two 9.75 mm cheeks either side of the slot | 532 MPa | 1.60 | [C2] |
| Jaw arm knuckle | Whole arm moment (16.0 kN m) through the 18 mm knuckle round the pin | 392 MPa | 2.17 | [C3] |
| Main pivot pin, 45 mm, 18 mm bore | Whole cylinder force as a central point load over 102 mm (conservative) | 416 MPa | 2.04 | [C4] |
| Link pins, 25 mm | 115 kN link force, double shear and bending | 118 MPa shear, 484 MPa bending | 1.76 | [C5] |
| Link, net section at the eye | 115 kN | 388 MPa | 1.78 | [C5b] |
| Frame plate, net section at the window | Half the cylinder force in tension | 102 MPa | 4.93 | [C6] |
| Frame plate at the pivot bore | As above, stress concentration 2.5 | 275 MPa | 1.82 | [C6b] |
| Adapter screws, M16 class 12.9 | 17.8 kN each in shear on the root area | 123 MPa | 5.17 | [C7] |

Other checks: bearing of an arm's knuckle on the pin 167 MPa [C4b]; the crosshead's bearing on its pins 196 MPa against 430 MPa yield [C5c]; the links buckle out of plane at about 1,000 kN against 115 kN [C5b]; the collar thread in the adapter has about 4,490 mm² of thread in shear, 32 MPa [C7b]. The 10 mm frame plates (RBJ-DDR-002, C2) have a margin of 1.82 at their weakest section. The 4340 pins (C4) and the link slot starting at 100 mm (C5) raised the two lowest margins above 1.5.

## D. Cutter (R4, R11)

A 16 mm bar has 201 mm² of section; at a shear strength of 520 MPa it needs about 105 kN, or 515 bar, against 142 kN available: a ratio of 1.36 [D1]. At the same upper strength the cylinder could shear 18.7 mm bar [D1b]; the rating stays at 16 mm (RBJ-DDR-001, D4). The moving blade closes the cut after about 37 cm³ of oil, about 41 slow-stage strokes or under 2 minutes [D5].

After the cut the carrier lands on the stop bar with the whole cylinder force if the operator keeps pumping. With two M16 screws in each plate, each screw carries 35.5 kN, 247 MPa on its root area, margin 2.59; with one screw a side (the earlier design) the margin was 1.29 [D2, D2b] (RBJ-DDR-002, C6). The nose block, which takes the fixed blade's thrust, has the same four-screw fixing and margin [D2]. The cutter plates carry 48 MPa at the hook, margin 14.3 [D3]; the carrier's 7075 face bears on the stop at 60 MPa [D4].

## E. Lifting ram (R1, R12)

The ram lifts 14.5 t at 700 bar against the 10 t target (R1); a CalRig proof load at 1.5 times rated load is TRL 4 work. The riser tube, 88.9 x 10, carries 57 MPa, margin 6.02, and its wall stands at 34.5 to 44.5 mm from the axis, over the base ring at 36 to 46 mm and under the 70 mm cylinder base, so its end plates work in bearing [E1] (RBJ-DDR-002, C9).

The base plate is the critical part. Treated as a free circular plate of the same area (141 mm radius) on an even reaction, loaded on the 35 mm radius of the cylinder base, a 12 mm S355 plate would reach 931 MPa (margin 0.37); the 20 mm S690QL plate reaches 335 MPa, margin 2.06 [E2] (RBJ-DDR-002, C8). This model is conservative where the cribbing is stiff under the centre.

Under the 250 mm plate the bearing pressure is 2.27 MPa, far more than rubble can take. On three 100 mm hardwood sleepers 600 mm long it falls to 0.79 MPa [E3], which meets R12; the plate never goes on bare rubble. Reach: 256 mm closed, 357 mm open, 527 mm on the riser [E4].

> **Safety:** Never work under a load held only by the ram. Crib the load as it rises. The riser goes under the cylinder, never on the plunger.

## F. Pump and time (R7)

A full stroke under load takes about 228 slow-stage strokes, about 9 minutes; with no load the fast stage needs 57 strokes, about 2 minutes [F1]. Handle effort at 700 bar is 380 N on a 600 mm handle [F2]. One full spreader stroke at 700 bar moves 14.35 kJ of oil; with estimated losses the operator puts in about 16.9 kJ and 12.5 kJ reaches the jaw tips [F4] (Figure 4 of RBJ-PRC-001). Setting up needs two coupler connections and no tools, about 1 to 2 minutes from the bags (R7, estimate); a tool change is one coupler off and one on, about 20 s (R8).

## G. Masses (R6)

*Table 3. Packed loads, bag included [G1].*

| Load | Mass (kg) |
| --- | --- |
| Pump, gauge and hoses | 15.9 |
| Spreader | 24.8 |
| Cutter | 22.0 |
| Lifting ram set (base, riser, cylinder, saddle) | 23.7 |
| Whole kit [G2] | 86.4 |

Every load is under 25 kg; the spreader has 0.2 kg in hand. Bought parts use catalogue masses; made parts use the model's volumes.

## H. Cost (R10)

Value-engineering target: USD 3,500. Estimated cost of the constructable design: USD 5,895 (USD 2,395 over the target); made parts USD 3,030, bought parts USD 2,865 [H1]. The main drivers and the savings worth trying are in RBJ-DEC-001, Value engineering.

## L. Results against every requirement

*Table 4. Results (also in docs/04-calcs/results.csv).*

| ID | Result | Target | Status |
| --- | --- | --- | --- |
| R1 | 14.5 t at 700 bar (cylinder rated 15 t) | 10 t or more | Met on paper (proof load is TRL 4) |
| R2 | 48.6 kN closed to 64.1 kN open | 40 kN or more at the tips | Met on paper |
| R3 | 262 mm open; tips 32 mm thick closed | 250 mm or more | Met on paper |
| R4 | About 105 kN needed; 142 kN available, ratio 1.36 | Cut 16 mm bar | Met on paper |
| R5 | All parts 700 bar; hoses 2,800 bar burst; gauge to 1,000 bar | At or above relief; hoses 4 to 1 | Met by specification (to confirm when parts are bought) |
| R6 | 15.9, 24.8, 22.0 and 23.7 kg | No load over 25 kg | Met on paper (spreader 0.2 kg under) |
| R7 | Two coupler connections, about 1 to 2 min | Within 3 min | Met on paper |
| R8 | One coupler swap, about 20 s | Under 1 min | Met by design |
| R9 | Every hydraulic part in a class two or more makers offer | Two suppliers | Met by specification |
| R10 | USD 5,895 | Value-engineering target USD 3,500 | Over the value-engineering target by USD 2,395 |
| R11 | Lowest 1.60, the jaw arm tail | 1.5 or more on yield | Met on paper |
| R12 | 0.79 MPa on three hardwood sleepers | Never on bare rubble | Met by design and procedure |

No requirement fails. The figures that most need confirming at TRL 4 are the jaw arm tail and link pins (the lowest margins), the base plate on real cribbing, and the cutting force on the bar grades crews actually meet.
