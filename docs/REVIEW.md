# Review note: RubbleJack

## Session 2026-09-30: scaffolded

### What was done

- Repository created from kit 1.6.0 at TRL 1, target TRL 2.
- `docs/01-problem.md` (RBJ-PRB-001 v0.1): problem with cited evidence, users, environment, constraints, prior work, open questions.
- `docs/02-concept.md` (RBJ-PRC-001 v0.1): how it works, components, patent design-arounds, shared blocks, safety.
- `docs/03-requirements.md` (RBJ-REQ-001 v0.1): 10 proposed requirements.
- `README.md` with concept rationale, burning platform, where it could be used, and what sparked the idea.

## Session 2026-10-03: TRL 2 (populate)

Run as the first half of the TRL 3 path (`/to-trl3`) on kit 1.7.0, under Amish's pre-approval of 2026-10-03: "start with the first 14 repos from the list of 29 projects. I pre-approve the batch runs along with any recommendations you come up with. I also accept any cost overruns or variations from the assumed scope cost." That go counts as the TRL 2 approval.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`, root `CLAUDE.md`); `.kit/PHASE.yaml` kept as installed.
- `docs/01-problem.md` (RBJ-PRB-001 v0.2): budget stated as a value-engineering target, co-design candidate and checklist, open questions answered, safety note.
- `docs/03-requirements.md` (RBJ-REQ-001 v0.2): measurable targets; R11 (1.5 on yield at 700 bar) and R12 (lift only on cribbing) added.
- `docs/02-concept.md` (RBJ-PRC-001 v0.2): how it works, components with BOM numbers, key design choices, first-order numbers, safety section.
- `docs/decisions/0001-trl2-review-decisions.md` (RBJ-DDR-001): TRL 2 review decisions D1 to D14.
- Concept media from `cad/src/concept_media.py`: `media/hero.png`, `media/concept-blueprint.png` and `.pdf` (RBJ-DWG-010), `media/model.glb` and `media/viewer.html`, `media/cutaway.png` (spreader pivot), `media/exploded.png` (BOM callouts), `media/flow.png` (energy for one spreader stroke, estimates). The media were drawn from the constructable model (below), not a separate massing model.
- `bom/bom.csv`: every line with a specification and indicative price.

### Results

- Concept: one 700 bar two-speed hand pump drives three tools, each on its own 15 t cylinder, so a tool change is a coupler swap (R8).
- First-order numbers were confirmed by the TRL 3 calculations below.

### Requirements not met

None at TRL 2; see TRL 3.

### Decisions made under the pre-approval

D1 to D14 in RBJ-DDR-001 (commodity 700 bar class, one cylinder per tool, linkage spreader, guillotine cutter rated 16 mm, located ram stack, materials, strength rule R11, not-certified notice, proof load before use, four loads, cribbing required, co-design first candidate, shared blocks, gauge always fitted).

### Safety concerns

Lifting, spreading, cutting and 700 bar oil; see TRL 3.

## Session 2026-10-03: TRL 3 (advance and build plan)

### What was done

- **Model.** `cad/src/model.py`: the constructable design, with 228 constructability checks (all pass). The pending edits from the interrupted run were made: spreader frame plates 12 mm to 10 mm, and two screws in each plate for the cutter stop bar (stop bar lengthened from 30 to 60 mm). Further changes found by the calculations and checks are in the list below. STEP and STL: `cad/step/rubblejack-{kit,spreader,cutter,ram}.step`, `cad/stl/` the same.
- **Calculations.** RBJ-CAL-001: `docs/04-calcs/01-sizing.md`, `docs/04-calcs/sizing.py`, `docs/04-calcs/results.csv`.
- **Drawing.** General arrangement RBJ-DWG-001 Rev P1 from `cad/src/sheets.py` (SVG, PDF, PNG).
- **BOM.** `bom/bom.csv`, 24 lines, every unit cost filled, a supplier class for each.
- **Concept media** refreshed from the model (as at TRL 2).
- **Build plan.** `cad/src/build_plan_media.py`: overview, 18 making sketches (RBJ-DWG-101 to 118), 9 joint close-ups and 16 step pictures; `docs/05-build-plan.md` (RBJ-BLD-001); `docs/decisions/0002-design-for-construction.md` (RBJ-DDR-002); `docs/06-design-decisions.md` (RBJ-DEC-001).
- **Appearance model.** `cad/src/product_model.py` (`product_parts()`, `TITLE`, `RENDER_VIEWS` hero, exploded and detail) on the constructable components, with a 1.75 m `mannequin()` for scale; scenes exported with `.kit/export_views.py` to `/home/claude/renders/rubblejack` for the photoreal render on Amish's Mac. The README leads with `media/render-hero.png`, which will exist after that render.
- `project.yaml`: trl 3, trl_target 3, `design_state: constructable`, trl_evidence listed; `budget_usd` unchanged at 3,500. README updated (TRL 3, renders, links, Building the prototype, Safety).

### Results

*Table 1. Key results at 700 bar (RBJ-CAL-001).*

| Quantity | Result |
| --- | --- |
| Force per cylinder | 142 kN (14.5 t) |
| Spreader | 48.6 kN closed to 64.1 kN open between the tips; 262 mm opening; tips 32 mm thick |
| Cutter | 16 mm bar needs about 105 kN; ratio 1.36; largest bar at the upper strength 18.7 mm |
| Ram | 14.5 t; reach 357 mm, 527 mm on the riser; 0.79 MPa on three hardwood sleepers |
| Lowest strength margin | 1.60 on yield, jaw arm tail at the link slot; link pins 1.76; links 1.78 |
| Loads, packed | 15.9, 24.8, 22.0 and 23.7 kg (kit 86.4 kg) |
| Pump | About 228 slow strokes (9 min) for a full stroke under load; about 41 strokes for one cut |
| Cost | Value-engineering target: USD 3,500. Estimated cost of the constructable design: USD 5,895 (USD 2,395 over the target) |

### Requirements not met

None fails on paper. R10 is over the value-engineering target by USD 2,395 (accepted under the pre-approval). R6 is met with only 0.2 kg in hand on the spreader. R5 and R9 are met by specification and depend on ratings confirmed when parts are bought.

### Decisions made under the pre-approval

All dated 2026-10-03, decided by Amish with his quote above, recorded in RBJ-DEC-001:

- RBJ-DDR-001, D1 to D14 (TRL 2 review).
- RBJ-DDR-002, C1 to C14 (design for construction).
- Cost overrun accepted; `budget_usd` left unchanged.
- Appearance model: no geometric deviation from `model.py`; the colours and finish classes (painted orange steel tools, natural aluminium plates, blue cylinders, red pump, black hoses) are a chosen look, decided under the same pre-approval.

### Design changes made for construction (2026-10-03)

1. Spreader frame plates 10 mm instead of 12 mm 7075-T6 (pending edit; margin 1.82 at the pivot bore).
2. Cutter stop bar 60 mm long with two M16 screws in each plate instead of one (pending edit; screw margin 1.29 to 2.59, and the bar cannot turn).
3. Main and link pins 4340 instead of 4140 (link pin margin 1.35 to 1.76).
4. Link slot in the jaw arm tail from 100 mm instead of 95 mm (tail margin 1.50 to 1.60; links clear at nine stroke positions).
5. Fixed blade screws M12 instead of M16: the four M16 heads, 20 mm apart, touched (found by counting the screw solids; a check now guards it).
6. Ram base plate 20 mm S690QL instead of 12 mm S355 (plate margin 0.37 to 2.06).
7. Riser tube 88.9 x 10 instead of 114.3 x 8, so its wall stands over the base ring and under the cylinder base.
8. Earlier in the same TRL 3 pass (from the interrupted run, recorded in RBJ-DDR-002): collar adapters, interleaved pivot with spacers, located ram stack, stud-mounted crosshead and carrier, shear layout, lightening pockets, bolted handles.

### Build plan findings

- The kit's safety case rests on three made parts with the lowest margins (jaw arm tail, link pins, links) and on the base plate on real cribbing; these are the first things to strain-gauge at TRL 4.
- Assembly needs the spreader's crosshead pins fitted before the lower plate (no access from below afterwards), and the main pin pushed up from below with the tool on blocks; the step order reflects this.
- The collar thread is the single load path for the spreader and cutter reactions; the collar's rating must be confirmed from the cylinder maker before any adapter is cut.
- The kit layout used for the concept media is sparse; the overview picture places each tool in its own area so parts do not mix.
- The kit's `drawing.project_views` cannot convert the hose torus edges to SVG; `cad/src/sheets.py` adds a `safe_views` that skips such edges and is used for the concept blueprint and the making sketches. The kit itself was not changed.

### Safety concerns

- 700 bar oil injection, loads of 142 kN, flying fragments when cutting, stored energy in spread loads and bent bar, and collapsed structures that move. Safety sections are in every document that describes the hazard, and the build plan has eight safety stops (heat treatment, welds, first pressure, first load, proof load, lifting, cutting, use outside the bench).
- Nothing is proof-loaded; the strength margins are hand calculations on minimum yield values. No tool may be used before a CalRig proof load at 1.5 times the force at 700 bar and a crack check.
- Single-acting tools give no powered closing force; crews must not expect the spreader to squeeze or pull.
- The kit is not certified to NFPA 1936, NFPA 1960 or EN 13204, and the documents say so.

### Recommended next step

TRL 4 when the portfolio phase allows: buy one cylinder and confirm the collar and plunger threads, have the arms, pins and blades made and heat treated, then proof-test each tool on CalRig with strain gauges at the jaw arm tail, link pins and base plate.

## 2026-10-03: photoreal renders

Rendered with Blender Cycles on Amish's Mac from `cad/src/product_model.py`; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` made with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes and `render.py --check` has no FAIL.
