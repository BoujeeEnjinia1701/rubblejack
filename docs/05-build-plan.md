---
doc_id: RBJ-BLD-001
title: RubbleJack prototype build plan
project: RubbleJack
doc_type: Build plan
version: "0.1"
status: Draft
date: '2026-10-03'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-03'
    author: Amish Chadha
    change: First build plan; design made constructable (RBJ-DDR-002); pictures by component, joint and step
---

# RubbleJack prototype build plan

**Plan, not yet built.** How to build the first proof-of-concept RubbleJack kit, component by component. Building and testing to it is TRL 4 work. Decisions are kept in the design decisions register ([docs/06-design-decisions.md](06-design-decisions.md)), not here.

> **Safety:** RubbleJack works with oil at 700 bar (10,000 psi) and forces of 142 kN (14.5 t). A failed part can throw fragments, and oil from a pinhole leak can be injected under the skin. Nothing built to this plan is rescue equipment: it is a prototype for proof testing, not certified to NFPA 1936, NFPA 1960 or EN 13204. No tool is pressurised until the safety stops in section 6 are passed, and no tool is used on a load, let alone a person, until it has been proof-loaded on CalRig and crack-checked. Hardened tool steel, 4340 and S690QL plate need proper heat treatment and welding procedures; cut edges are sharp.

## 1. What you are building

![Figure 1. Every component, pulled apart and numbered in build order](05-build-plan/overview.png)

*Figure 1. Every component of the kit pulled apart and numbered in build order: spreader 1 to 12, cutter 13 to 21, lifting ram 22 and 23, then the bought parts.*

The prototype is the whole kit: a bought two-speed hand pump with a gauge and two 2 m hoses, and three tools, each on its own bought 15 t cylinder. The spreader is two steel jaw arms on one pin, held between two aluminium plates and opened by a crosshead and two links. The cutter is a guillotine: a hardened blade on a carrier slides past a fixed blade, with the bar held in a hook cut in two steel plates. The lifting ram is the third cylinder standing on a steel base plate, with a riser block that can go under it. Eighteen kinds of part are made, in a machine shop and a fabrication shop: waterjet or laser cutting of plate, milling, turning, drilling and tapping, heat treatment of the arms, pins and blades, and a few welds on the ram parts and handles. Everything else is bought and bolted on. The parts cost about USD 5,895 from the bill of materials.

## 2. What changed to make it buildable

The scaffold described bolt-on heads, base plates and extension tubes without saying how any part is made or held. Each change below keeps what the kit does; all are recorded in decision record RBJ-DDR-002.

*Table 1. Changes from the concept.*

| Component | The concept had | The buildable design has | Why |
| --- | --- | --- | --- |
| Spreader and cutter heads | Bolt-on heads, no interface | Two plates bolted to an aluminium adapter that screws onto the cylinder's collar thread; a cylinder for each tool (Figure 20) | The collar thread is the cylinder's own fixing; a tool change is a hose swap |
| Spreader frame plates | 12 mm aluminium | 10 mm aluminium | Lighter; still strong enough at the pivot |
| Spreader pivot | Arms overlapping on a pin | Interleaved knuckles on one pin with a spacer each side (Figure 23) | Both arms share one pin; nothing slides along it |
| Pins | 4140 steel | 4340 steel, hardened and tempered | Stronger link pins |
| Jaw arm tail | Link slot from 95 mm | Link slot from 100 mm | Stronger tail; links still clear |
| Cutter stop bar | 30 mm long, one screw each side | 60 mm long, two screws each side (Figure 27) | It cannot turn and its screws are twice as strong |
| Fixed blade screws | Four M16, heads touching | Four M12 (Figure 26) | The heads now clear each other |
| Ram base plate | 12 mm mild steel | 20 mm high-strength steel (Figure 28) | The 12 mm plate would bend under full load |
| Riser block | 114 mm tube | 89 mm tube with a 10 mm wall | The tube wall stands right over the base ring and under the cylinder |
| Ram stack | Loose base plates and tubes | Locating rings and a spigot (Figure 28) | Stacked parts cannot slide |

## 3. Making the components

Make and check each component before the step that needs it. The making sketches give the three views with overall sizes; the notes on each sketch give the sizes that matter. Heat-treated parts are machined first, heat treated, then finished and crack-checked (dye penetrant or magnetic particle).

### 3.1 Collar adapters (make 2: one for the spreader, one for the cutter)

![Figure 2. Making sketch of the collar adapter](../cad/drawings/RBJ-DWG-101.png)

*Figure 2. Making sketch RBJ-DWG-101.*

**What it is.** An aluminium block 60 mm long, 130 mm wide and 92 mm tall that screws onto the cylinder's collar thread and carries the two plates of a tool. 7075-T6 plate, 100 mm thick.

**How to make it.**

1. Mill the block to 60 x 130 x 92 mm, faces square; the two 130 x 60 faces must be parallel and 92 mm apart.
2. Bore a 72 mm hole through on the long axis, centred on the 130 x 92 face.
3. From the front face, cut the cylinder's collar thread 40 mm deep. Measure the thread on the bought cylinder first and cut to match it (about 71.4 mm, 12 threads an inch).
4. In each 130 x 60 face, drill 14 mm and tap M16 four holes, 24 mm of full thread, at 15 and 45 mm from the front face, 50 mm each side of the centre line.
5. Break every edge 1 mm.

**How it fits.** It screws onto the collar until the collar's end is flush with its front face (Figure 20). The frame plates lie flat on the two 130 x 60 faces, held by four M16 screws each.

**Check.** A plate lies on each face with no rock, and all eight screws start by hand.

### 3.2 Spreader frame plates (make 2)

![Figure 3. Making sketch of the spreader frame plate](../cad/drawings/RBJ-DWG-102.png)

*Figure 3. Making sketch RBJ-DWG-102.*

**What it is.** The two plates above and below the jaw arms that carry the pivot pin and pull back on the adapter. 7075-T6 aluminium plate, 10 mm.

**How to make it.**

1. Cut the profile by waterjet or saw and file: 404 mm long, 130 mm wide for the first 60 mm, tapering to 100 mm wide 259 mm from the back edge, ending in a 55 mm radius round the pivot.
2. With both plates clamped together, bore the 45.4 mm pivot hole 349 mm from the back edge on the centre line, and drill four 18 mm holes 15 and 45 mm from the back edge, 50 mm each side of the centre line.
3. Cut the 30 mm wide window from 80 to 234 mm from the back edge; the crosshead runs under it.
4. Upper plate only: drill two 13.6 mm handle holes on the centre line, 69 and 199 mm from the back edge.
5. Deburr; round the outside corners about 3 mm.

**How it fits.** Each plate's back end sits flat on the adapter; the pivot bore carries the main pin with the spacers between plate and arms.

**Check.** A 45 mm pin passes through both pivot bores with the plates clamped together.

### 3.3 Crosshead

![Figure 4. Making sketch of the crosshead](../cad/drawings/RBJ-DWG-103.png)

*Figure 4. Making sketch RBJ-DWG-103.*

**What it is.** The block on the end of the spreader's plunger that pushes both links. 7075-T6 aluminium, 46 x 112 x 40 mm.

**How to make it.**

1. Mill the block to size.
2. Cut two slots 16.5 mm wide, centred in the 40 mm height, from 7 mm either side of the centre line out to each side face.
3. Bore two 25.4 mm pin holes through the top and bottom, 30 mm each side of the centre line, at the middle of the length.
4. In the back face, on the centre, drill 21 mm and tap M24, 25 mm deep, to suit the plunger stud.

**How it fits.** It screws onto an M24 stud in the plunger until its back face seats on the plunger end; the links sit in its slots (Figure 21).

**Check.** A link slides into each slot with about 0.5 mm of play.

### 3.4 Links (make 2)

![Figure 5. Making sketch of the link](../cad/drawings/RBJ-DWG-104.png)

*Figure 5. Making sketch RBJ-DWG-104.*

**What it is.** The two bars that push the jaw arm tails. S690QL high-strength steel plate, 16 mm.

**How to make it.**

1. Laser or waterjet cut two links: 150 mm between bore centres, 44 mm eyes, 32 mm wide between the eyes.
2. With the two clamped together, drill and ream the 25.4 mm bores.
3. Deburr; leave no notches or scratches across the body.

**How it fits.** One eye goes in a crosshead slot and the other in the slot of an arm's tail, each on a 25 mm pin (Figures 21 and 22).

**Check.** Both links sit on two 25 mm pins at once without binding.

### 3.5 Jaw arm A (centre knuckle)

![Figure 6. Making sketch of jaw arm A](../cad/drawings/RBJ-DWG-105.png)

*Figure 6. Making sketch RBJ-DWG-105.*

**What it is.** One of the two jaws, with a tail behind the pivot that the link pushes. 4340 steel plate 40 mm, quenched and tempered to about 300 HB, milled to 36 mm.

**How to make it.**

1. Waterjet cut the profile from 40 mm plate: jaw 250 mm from the pivot to the tip, straight inner face, outer edge 70 mm deep near the pivot curving to 16 mm at the tip; tail behind the pivot ending in a 27 mm radius eye 160 mm from the pivot.
2. Mill both faces to 36 mm.
3. Bore and ream the 45.4 mm pivot hole and the 25.4 mm tail pin hole.
4. Mill the 16.5 mm slot in the tail, centred in the thickness, from 100 mm out to the tail end.
5. Within a 61 mm radius of the pivot, mill 9 mm off each face, leaving a centre knuckle 18 mm thick.
6. Mill 8 mm deep lightening pockets in both faces, 12 mm in from every edge, in the jaw and the tail.
7. Cut 2 mm serrations across the outer face of the tip for grip.
8. Break every edge 1 mm; leave no tool marks across the jaw near the pivot. Crack-check.

**How it fits.** Its knuckle sits in arm B's groove on the main pin (Figure 23); the link's eye sits in its tail slot (Figure 22).

**Check.** Its knuckle slides into arm B's groove and the bores line up.

### 3.6 Jaw arm B (twin knuckles)

![Figure 7. Making sketch of jaw arm B](../cad/drawings/RBJ-DWG-106.png)

*Figure 7. Making sketch RBJ-DWG-106.*

**What it is.** The other jaw, a mirror image of arm A with twin knuckles. Same material.

**How to make it.** As arm A, mirrored, except step 5: within a 61 mm radius of the pivot, mill an 18 mm wide groove centred in the thickness, leaving two knuckles 9 mm thick. Make arms A and B as a pair.

**How it fits.** Arm A's knuckle sits between its two knuckles on the main pin (Figure 23).

**Check.** As arm A.

### 3.7 Pivot spacers (make 2)

![Figure 8. Making sketch of the pivot spacer](../cad/drawings/RBJ-DWG-107.png)

*Figure 8. Making sketch RBJ-DWG-107.*

**What it is.** Two rings, 70 mm outside, 45.4 mm bore, 28 mm long, from 7075-T6 bar or tube; ends faced square and parallel.

**How it fits.** One above the arms and one below, between the arm faces and the frame plates (Figure 23).

**Check.** The two arms and two spacers stacked measure 92 mm, the gap between the plates.

### 3.8 Main pivot pin

![Figure 9. Making sketch of the main pivot pin](../cad/drawings/RBJ-DWG-108.png)

*Figure 9. Making sketch RBJ-DWG-108.*

**What it is.** A 45 mm pin, 120 mm long under a 57 mm head 6 mm thick, with an 18 mm bore, from 4340 bar quenched and tempered to about 300 HB, ground.

**How to make it.** Turn, bore, cut a groove for a 45 mm external circlip 3 to 6 mm from the plain end, chamfer the plain end 2 mm, heat treat and grind.

**How it fits.** It goes up from below through the lower plate, spacer, knuckles, spacer and upper plate; a washer and circlip hold it on top (Figure 23).

**Check.** It slides through every bore by hand.

### 3.9 Link pins (make 4)

![Figure 10. Making sketch of the link pin](../cad/drawings/RBJ-DWG-109.png)

*Figure 10. Making sketch RBJ-DWG-109.*

**What it is.** Four 25 mm pins with 37 mm heads, from the same 4340 bar: two 48 mm long under the head for the crosshead, two 44 mm for the arm tails. Each has a groove for a 25 mm external circlip and a washer.

**How it fits.** Each goes up from below through a link eye and the crosshead or tail; washer and circlip on top (Figures 21 and 22).

**Check.** Each passes its link and bores without force.

### 3.10 Carry handles (make 2)

![Figure 11. Making sketch of the carry handle](../cad/drawings/RBJ-DWG-110.png)

*Figure 11. Making sketch RBJ-DWG-110.*

**What it is.** A D handle bent from 26.9 x 3.2 mm steel tube: two posts 70 mm tall, 130 mm apart for the spreader and 110 mm apart for the cutter, with an M12 threaded plug welded into each post foot and faced flat.

**How it fits.** Two M12 cap screws with spring washers come up through the upper plate into the plugs (Figure 24).

**Check.** Lift the finished tool by it; nothing moves at the feet.

### 3.11 Blade carrier

![Figure 12. Making sketch of the blade carrier](../cad/drawings/RBJ-DWG-111.png)

*Figure 12. Making sketch RBJ-DWG-111.*

**What it is.** The block on the cutter's plunger that carries the moving blade and slides between the cutter plates. 7075-T6 aluminium, 50 mm long, 102 mm wide, 91 mm tall.

**How to make it.**

1. Mill to size; the 91 mm height gives 0.5 mm of play each side between the plates.
2. In the back face, on the cylinder axis, 62 mm up from the lower long edge, drill 21 mm and tap M24, 25 mm deep.
3. Drill two 17 mm holes through, front to back, 23 mm below the middle of the height, 25 mm below and 30 mm above the cylinder axis; counterbore them 25 mm, 16 mm deep, from the back.

**How it fits.** The moving blade bolts to its front face with two M16 screws from the counterbores (Figure 25); it screws onto the plunger's M24 stud.

**Check.** It slides between two plates set 92 mm apart with 0.5 to 1 mm of play.

### 3.12 Moving blade

![Figure 13. Making sketch of the moving blade](../cad/drawings/RBJ-DWG-112.png)

*Figure 13. Making sketch RBJ-DWG-112.*

**What it is.** The lower half of the shear: S7 shock-resisting tool steel, 70 x 70 x 45.5 mm, hardened to 54 to 56 HRC.

**How to make it.**

1. Machine the block soft. Cut a 17 mm U notch, its round bottom centred 45 mm from the back face, open to the top long edge.
2. Drill and tap two M16 holes 28 mm deep in the back face, matching the carrier's holes.
3. Heat treat; grind the top face flat and the notch edges sharp and square.

**How it fits.** Bolted to the carrier; its top face slides 0.2 mm under the fixed blade (Figure 26).

**Check.** The top face is flat to 0.05 mm on a surface plate.

### 3.13 Fixed blade

![Figure 14. Making sketch of the fixed blade](../cad/drawings/RBJ-DWG-113.png)

*Figure 14. Making sketch RBJ-DWG-113.*

**What it is.** The upper half of the shear: S7 tool steel, 70.5 x 70 x 45.8 mm, hardened to 54 to 56 HRC.

**How to make it.**

1. Machine soft; cut the same 17 mm U notch, its round bottom 8.5 mm from the back face.
2. Drill and tap four M12 holes 20 mm deep in the top face, at 30 and 50 mm in front of the notch centre, 15 mm toward the lower edge and 25 mm toward the upper.
3. Heat treat; grind the bottom face flat, the notch edges sharp and the front face square.

**How it fits.** Its front face bears on the nose block; four M12 screws through the upper plate hold it 0.2 mm above the moving blade (Figure 26).

**Check.** With both blades on a surface plate, the notches line up.

### 3.14 Nose block

![Figure 15. Making sketch of the nose block](../cad/drawings/RBJ-DWG-114.png)

*Figure 15. Making sketch RBJ-DWG-114.*

**What it is.** A 7075-T6 block 30 x 90 x 92 mm that takes the fixed blade's thrust. Each 90 x 30 face has two M16 holes, 26 mm deep, on the middle of the 30 mm length, 35 mm below and 20 mm above the cylinder axis.

**How it fits.** Between the plates at the front, held by two screws in each plate; the fixed blade bears on its back face (Figure 26).

**Check.** It stands square between the plates with no gap at either.

### 3.15 Stop bar

![Figure 16. Making sketch of the stop bar](../cad/drawings/RBJ-DWG-115.png)

*Figure 16. Making sketch RBJ-DWG-115.*

**What it is.** An S355 steel bar 60 x 32 x 92 mm that ends the cutter's stroke. Each 60 x 32 face has two M16 holes, drilled 14 mm and tapped 24 mm deep, 15 and 45 mm from the back end, on the width centre.

**How it fits.** Between the plates below the blades; the carrier lands on its back end 30 mm after the cut starts (Figure 27).

**Check.** The back end is square to the faces.

### 3.16 Cutter plates (make 2)

![Figure 17. Making sketch of the cutter plate](../cad/drawings/RBJ-DWG-116.png)

*Figure 17. Making sketch RBJ-DWG-116.*

**What it is.** The two steel plates that hold the cutter together, with a hook for the bar. S690QL high-strength steel, 16 mm, 259 x 122 mm.

**How to make it.**

1. Laser cut both plates with the 30 mm hook: centred 167 mm from the back edge, its round bottom 57 mm up from the lower edge, open to the upper edge.
2. With the plates clamped together, drill the shared 18 mm holes: adapter at 15 and 45 mm from the back, 50 mm each side of the axis (the axis is 72 mm up from the lower edge); nose at 244 mm from the back, 37 and 92 mm up; stop at 167 and 197 mm from the back, 20 mm up.
3. Upper plate only: four 13.5 mm fixed blade holes and two 13.6 mm handle holes, as the sketch shows.

**How it fits.** Each bolts to the adapter's faces, and to the nose block and stop bar; the upper plate also holds the fixed blade and handle.

**Check.** The hooks line up when the plates are stacked.

### 3.17 Ram base plate

![Figure 18. Making sketch of the ram base plate](../cad/drawings/RBJ-DWG-117.png)

*Figure 18. Making sketch RBJ-DWG-117.*

**What it is.** A 250 mm square plate of S690QL high-strength steel, 20 mm thick, with two 24 x 90 mm hand slots and a locating ring 92 mm outside, 72 mm inside and 15 mm tall welded on the centre. Do not swap it for mild steel.

**How to make it.** Cut the plate and slots; turn the ring from S355; weld it with a 6 mm fillet all round using low-hydrogen consumables, preheating as the plate maker's sheet says; let it cool slowly.

**How it fits.** The cylinder base or the riser spigot drops into the ring (Figure 28). The plate always sits on hardwood cribbing.

**Check.** The plate is flat to 1 mm after welding.

### 3.18 Riser block

![Figure 19. Making sketch of the riser block](../cad/drawings/RBJ-DWG-118.png)

*Figure 19. Making sketch RBJ-DWG-118.*

**What it is.** An S355 tube 88.9 x 10 mm, 150 mm long, welded between two 160 mm square, 10 mm plates, with a 70 mm spigot 12 mm tall under the bottom plate and a ring like the base plate's on the top plate.

**How it fits.** Its spigot drops into the base plate's ring; the cylinder base drops into its top ring (Figure 28). It goes only under the cylinder.

**Check.** The end plates are parallel to 0.5 mm and it stands without rocking.

### 3.19 Bought components

| Component | What to buy | What to do to it |
| --- | --- | --- |
| Hand pump | Two-speed, 700 bar, internal relief at 700 bar, about 900 cm³ oil, for single-acting cylinders | Fill and bleed as the maker says |
| Gauge and adapter | 0 to 1,000 bar glycerine gauge and a 700 bar gauge adapter | Fit to the pump outlet with thread sealant |
| Hoses and couplers | Two 2 m hoses, 700 bar, at least 4 to 1 burst; coupler halves for the three cylinders; dust caps | Check every coupler is the same series |
| Cylinders (3) | 15 t single-acting, spring return, 101 mm stroke, collar thread, plunger with an attachment thread | Measure the collar and plunger threads before making the adapters and studs |
| Tilting saddle | For a 15 t cylinder | None |
| Screws and studs | M16 and M12 class 12.9 cap screws, M24 class 10.9 studs, hardened and spring washers, circlips | None |
| Carry bags (4) | Heavy nylon tool bags with straps | None |

## 4. Putting it together

Torque every class 12.9 screw to the fastener maker's table, using the lower value for threads tapped in aluminium, with thread-locker on studs and on screws into aluminium.

### Step 1: collar adapter onto the spreader cylinder

![Step 1](05-build-plan/step-01.png)

Screw the adapter onto the collar by hand until the collar's end is flush with its front face.

### Step 2: crosshead onto the plunger

![Step 2](05-build-plan/step-02.png)

Fit the M24 stud into the plunger with thread-locker, then screw the crosshead on until it seats on the plunger end. The plunger turns in the cylinder, so the crosshead's angle is set later by the links.

### Step 3: links onto the crosshead

![Step 3](05-build-plan/step-03.png)

Put a link eye into each crosshead slot and push a 48 mm link pin up from below; washer and circlip on top of each (Figure 21).

### Step 4: lower frame plate onto the adapter

![Step 4](05-build-plan/step-04.png)

Hold the lower plate flat against the adapter's lower face and fit four M16 screws from below with hardened washers. Snug only until step 7.

### Step 5: pair the jaw arms

![Step 5](05-build-plan/step-05.png)

Slide arm A's centre knuckle sideways into arm B's groove until the pivot bores line up.

### Step 6: spacer and jaw arms onto the lower plate

![Step 6](05-build-plan/step-06.png)

Set the tool on two wooden blocks so the pin can come from below. Put the lower spacer on the plate's pivot bore and the paired arms on it, with the links' free eyes in the tail slots. Push the two 44 mm tail pins up from below; washers and circlips on top (Figure 22).

### Step 7: upper spacer, upper plate and main pin

![Step 7](05-build-plan/step-07.png)

Put the upper spacer on the arms and the upper plate on the adapter; fit its four screws. Push the main pin up from below through everything; washer and circlip on top (Figure 23). Torque all eight adapter screws. **Hold point:** the arms turn by hand through their whole opening with no bind.

### Step 8: carry handle onto the spreader

![Step 8](05-build-plan/step-08.png)

Two M12 cap screws with spring washers from under the upper plate into the handle feet (Figure 24).

### Step 9: collar adapter onto the cutter cylinder

![Step 9](05-build-plan/step-09.png)

As step 1.

### Step 10: blade carrier onto the plunger

![Step 10](05-build-plan/step-10.png)

Bolt the moving blade to the carrier first with two M16 screws from the counterbores, with thread-locker (Figure 25). Fit the M24 stud into the plunger and screw the carrier on until it seats on the plunger end.

### Step 11: lower cutter plate onto the adapter

![Step 11](05-build-plan/step-11.png)

Four M16 screws from below; snug only.

### Step 12: fixed blade, nose block and stop bar

![Step 12](05-build-plan/step-12.png)

Stand the nose block and stop bar on the lower plate and fit their two screws each from below. Lay the fixed blade on the moving blade, notches in line, front face against the nose block.

### Step 13: upper cutter plate

![Step 13](05-build-plan/step-13.png)

Put the upper plate on; fit four M16 adapter screws, two nose and two stop screws, and four M12 fixed blade screws. Torque all twenty. **Hold point:** a 0.2 mm feeler passes between the blades and the carrier slides by hand from open to the stop bar; shim under the upper plate at the fixed blade if the gap is short.

### Step 14: carry handle onto the cutter

![Step 14](05-build-plan/step-14.png)

As step 8.

### Step 15: the lifting ram stack

![Step 15](05-build-plan/step-15.png)

Drop the riser's spigot into the base plate's ring (only when the extra reach is needed), the cylinder's base into the riser's ring (or the base plate's ring), and the saddle's stem into the plunger (Figure 28). Never put the riser on top of the plunger.

### Step 16: gauge and hose onto the pump

![Step 16](05-build-plan/step-16.png)

Fit the gauge adapter to the pump outlet with thread sealant and the hose's coupler to the adapter. Fit a dust cap on every open coupler.

### Joint close-ups

![Figure 20. Joint 1: collar adapter between the frame plates](05-build-plan/joint-01.png)

*Figure 20. Joint 1: the adapter screws onto the collar thread; the plates bolt flat to it with four M16 screws each.*

![Figure 21. Joint 2: crosshead, links and pins](05-build-plan/joint-02.png)

*Figure 21. Joint 2: each link sits in a slot in the crosshead on one pin.*

![Figure 22. Joint 3: link in the arm's tail](05-build-plan/joint-03.png)

*Figure 22. Joint 3: the link sits in the tail's 16.5 mm slot; the pin carries it in double shear.*

![Figure 23. Joint 4: the pivot stack](05-build-plan/joint-04.png)

*Figure 23. Joint 4: plate, spacer, arm B, arm A, arm B, spacer, plate, all on the main pin; 92 mm between the plates.*

![Figure 24. Joint 5: carry handle on the upper plate](05-build-plan/joint-05.png)

*Figure 24. Joint 5: one M12 screw from under the plate into each handle foot.*

![Figure 25. Joint 6: moving blade on the carrier](05-build-plan/joint-06.png)

*Figure 25. Joint 6: two M16 screws from the carrier's counterbores hold the moving blade.*

![Figure 26. Joint 7: blades, nose block and the bar](05-build-plan/joint-07.png)

*Figure 26. Joint 7: the bar crosses both notches; the fixed blade bears on the nose block, 0.2 mm above the moving blade.*

![Figure 27. Joint 8: stop bar between the plates](05-build-plan/joint-08.png)

*Figure 27. Joint 8: the carrier lands on the stop bar after the cut; two screws in each plate hold it.*

![Figure 28. Joint 9: the lifting ram stack](05-build-plan/joint-09.png)

*Figure 28. Joint 9: riser spigot in the base ring, cylinder base in the riser's ring, saddle on the plunger.*

## 5. First checks

These are listed here and recorded in a TRL 4 test report; none is done at TRL 3.

| Check | Requirement | Pass when |
| --- | --- | --- |
| Every tool moves through its stroke by hand pressure on the pump, no load | R3, R8 | Spreader opens to at least 250 mm; cutter carrier reaches the stop; ram extends 101 mm; nothing binds |
| Couplers swap between tools | R7, R8 | Pump to working tool in 3 min from the bags; a tool change in under 1 min |
| Pressure hold, each tool against a fixed stop, at 700 bar on the gauge for 5 min | R5 | No leak, no gauge drop over 5 %, no visible deformation |
| Proof load on CalRig at 1.5 times the force at 700 bar, then crack check | R1, R2, R11 | No crack, no permanent set over 0.2 mm at the tips, pins or plates |
| Spreading force at the tips at five openings | R2 | 40 kN or more at every opening |
| Cut 16 mm B500B or A615 grade 60 bar | R4 | Clean cut below 700 bar on the gauge; blades undamaged |
| Weigh each packed bag | R6 | Each 25 kg or less |
| Ram on three hardwood sleepers with cribbing | R1, R12 | Lifts 10 t on CalRig without the plate rocking or the sleepers crushing |

## 6. Safety stops

Work stops at each point until everything listed is true.

| Stop | Before | What must be true to carry on |
| --- | --- | --- |
| S1 | Heat treatment is accepted | Arms, pins and blades have a hardness test result in range and pass a crack check; S690QL and 7075-T6 have mill certificates |
| S2 | Welded parts are used | Base plate and riser welds pass visual and dye-penetrant checks; the base plate is flat |
| S3 | First pressure on any tool | Every hose, coupler, gauge and cylinder is marked or documented at 700 bar; the gauge is fitted; couplers fully engaged; every screw torqued and every circlip seated; people out of the line of the tool and the hoses; eye and face protection on |
| S4 | First load | The tool is against a fixed stop or a load cell on CalRig, inside a guard, never on a load anyone stands near |
| S5 | Proof load | CalRig rated above 1.5 times 142 kN; operator behind a shield; pressure raised in steps of 100 bar with a pause at each |
| S6 | Any lift with the ram | Base plate on hardwood sleepers; cribbing ready to follow the load within 25 mm; nobody under the load; riser only under the cylinder |
| S7 | Any cut | Only reinforcing bar of 16 mm or less; bar ends guarded or held; everyone clear of the line of the ends |
| S8 | Any use outside the test bench | The tool has passed its proof load and crack check, and the co-design partner has trained the crew; it is still not certified rescue equipment |

> **Safety:** Never feel for a leak by hand. Release pressure at the pump's valve before uncoupling a hose, adjusting a tool or touching a load. Replace any hose that is kinked, abraded or bulging.

## 7. Tools, skills and workspace

- **Workshop:** waterjet or laser cutting service; a milling machine and lathe with boring and threading; drilling and tapping to M24; a surface plate; access to heat treatment with hardness testing; MIG or stick welding with low-hydrogen consumables and preheat; dye-penetrant crack-check kit.
- **Assembly:** torque wrench covering M12 and M16 class 12.9, circlip pliers, feeler gauges, thread-locker and thread sealant, two wooden blocks.
- **Skills:** machinist able to cut a fine collar thread and hold 0.05 mm flatness; welder qualified for high-strength steel; someone trained in high-pressure hydraulics for the first pressure checks.
- **Space:** a bench in a workshop with a clear zone around the test bench and a guard or shield for any pressurised test.

## 8. Where the numbers come from

- Model and constructability checks: `cad/src/model.py` (`cad/step/rubblejack-kit.step`, `-spreader`, `-cutter`, `-ram`)
- General arrangement: `cad/drawings/RBJ-DWG-001`; making sketches `cad/drawings/RBJ-DWG-101` to `RBJ-DWG-118`
- Pictures: `cad/src/build_plan_media.py`
- Calculations: `docs/04-calcs/01-sizing.md` (RBJ-CAL-001) and `docs/04-calcs/sizing.py`
- Parts and prices: `bom/bom.csv`
- Design changes: `docs/decisions/0002-design-for-construction.md` (RBJ-DDR-002)
