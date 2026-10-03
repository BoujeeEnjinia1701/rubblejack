"""RubbleJack concept media (TRL 3, constructable design RBJ-DDR-002), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Takes every component of the kit from cad/src/model.py (components(), laid out on the ground as
packed for a drill) and renders the media set with .kit/concept.py: hero with the 1.75 m figure,
blueprint sheet RBJ-DWG-010, 3D viewer, cutaway of the spreader, exploded view with BOM numbers
and the energy flow of one spreader stroke. Figures come from docs/04-calcs/sizing.py
(RBJ-CAL-001). CONCEPT, NOT FOR FABRICATION.

Coordinates in mm, Z up from the ground. The spreader is drawn half open (50 mm of plunger travel).
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from concept import Part, render_all, cutaway_parts, _render  # noqa: E402
from model import PARAMS as P, components  # noqa: E402
from sheets import patch_kit_views  # noqa: E402

patch_kit_views()

COLOR = {1: "#C2410C", 2: "#111827", 3: "#1F2937", 4: "#374151", 5: "#1D4ED8", 6: "#94A3B8", 7: "#CBD5E1",
         8: "#64748B", 9: "#0E7490", 10: "#D4A017", 11: "#A8A29E", 12: "#57534E", 13: "#B91C1C", 14: "#4B5563",
         15: "#6B7280", 16: "#111827", 17: "#0F766E", 18: "#94A3B8", 19: "#B45309", 20: "#B45309", 21: "#78716C"}
# one name per BOM line (from bom/bom.csv), so the exploded view's key has one short line per number
BOM_NAME = {}
for row in csv.DictReader((ROOT / "bom" / "bom.csv").open()):
    n, _, name = row["item"].partition(" ")
    BOM_NAME[int(n)] = name
BOM_NAME[16] = "Cap screws, M16 and M12"

parts, spreader_parts = [], []
for c in components(P, spreader_stroke=50.0, cutter_travel=0.0):
    prt = Part(BOM_NAME[c.bom], c.shape, COLOR[c.bom], c.bom, tuple(c.explode))
    parts.append(prt)
    if c.tool == "spreader":
        spreader_parts.append(prt)

render_all(
    parts, project="RubbleJack", title="Hand-pumped spreading, cutting and lifting kit concept", dwg_no="RBJ-DWG-010",
    key_figures=["One 700 bar hand pump drives three 15 t cylinders: 142 kN each",
                 "Spreader: 49 to 64 kN at the tips, 262 mm opening",
                 "Cutter: 16 mm bar needs about 105 kN, ratio 1.36",
                 "Ram: 14.5 t; reach 357 mm, 527 mm on the riser",
                 "Four loads: 15.9, 24.8, 22.0 and 23.7 kg packed",
                 "Estimated USD 5,895 against a USD 3,500 target",
                 "Not certified rescue equipment (NFPA 1936 and 1960, EN 13204)"],
    cut=False,
    flow={"title": "energy for one full spreader stroke at 700 bar, kJ (RBJ-CAL-001 estimates)",
          "unit": "kJ",
          "stages": [("Work at the pump handle", 16.88), ("Oil at 700 bar", 14.35), ("Plunger push", 13.63),
                     ("Work at the jaw tips", 12.54)],
          "losses": [(0, "Pump friction and leakage (15 %, estimate)", 2.53), (1, "Cylinder seals (5 %, estimate)", 0.72),
                     (2, "Pin friction in the linkage (8 %, estimate)", 1.09)]},
)
# cutaway of the spreader alone (the kit layout would cut through the hoses and pump): the same call render_all makes
_render(cutaway_parts(spreader_parts), ROOT / "media" / "cutaway.png", azim=-90, elev=18, title="RubbleJack: cutaway",
        note="Spreader only, front half removed through the pivot; seen from the front and above, 18 deg elevation")
