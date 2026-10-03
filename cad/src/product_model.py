"""RubbleJack appearance model for product renders (STANDARDS section 12).

Every shape comes from cad/src/model.py (components(), cutter(), rebar_sample()), so every main
dimension is the constructable design's; this file only adds colour, finish class and grouping,
and places a 1.75 m posed mannequin for scale. Appearance deviations from model.py: none in
geometry; colours and finishes are a proposed look (painted steel tools, natural aluminium plates,
black hoses, red pump), recorded in docs/REVIEW.md.

Groups: shell = spreader, internal = pump, gauge, hoses and lifting ram set, accessory = cutter
with a 16 mm bar in its hook, context = mannequin.
CONCEPT, NOT FOR FABRICATION.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Pos, Rot  # noqa: E402
from model import PARAMS, components, cutter_levels, zcyl  # noqa: E402

TITLE = "RubbleJack: hand-pumped spreading, cutting and lifting kit for rescue crews"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation): the kit laid out as packed for a "
             "drill, two-speed hand pump with gauge and coiled hoses at left, spreader half open at centre, cutter "
             "with a 16 mm bar in its hook behind it and the lifting ram on its base plate and riser at right; "
             "1.75 m person for scale"},
    {"name": "exploded", "groups": ["shell"], "explode": True, "el": 32, "az": -55,
     "note": "Exploded view of the spreader from the front right and above (about 32 deg elevation): cylinder and "
             "collar adapter at rear, crosshead and links, the two jaw arms on the main pivot pin with their spacers, "
             "upper and lower aluminium frame plates, screws and carry handle"},
    {"name": "detail", "groups": ["accessory"], "explode": False, "el": 22, "az": -35,
     "note": "Detail of the cutter from the front right, slightly above (about 22 deg elevation): a 16 mm "
             "reinforcing bar in the open hook between the two steel plates, fixed blade above and moving blade "
             "below, nose block in front and stop bar beneath"},
]

C_TOOL, C_AL, C_STEEL, C_BLADE = "#C2410C", "#C9CED6", "#3F4652", "#2B2F36"
C_CYL, C_PUMP, C_HOSE, C_BLACK, C_BAR = "#1D4ED8", "#B91C1C", "#111827", "#0B0F14", "#8B6F47"
LOOK = {  # BOM line: (colour, material class)
    1: (C_PUMP, "painted"), 2: (C_BLACK, "metal"), 3: (C_HOSE, "rubber"), 4: (C_STEEL, "metal"), 5: (C_CYL, "painted"),
    6: (C_AL, "metal"), 7: (C_AL, "metal"), 8: (C_AL, "metal"), 9: (C_STEEL, "metal"), 10: (C_TOOL, "painted"),
    11: (C_AL, "metal"), 12: (C_STEEL, "metal"), 13: (C_BLACK, "rubber"), 14: (C_TOOL, "painted"), 15: (C_TOOL, "painted"),
    16: (C_BLACK, "metal"), 17: (C_TOOL, "painted"), 18: (C_AL, "metal"), 19: (C_BLADE, "metal"), 20: (C_BLADE, "metal"),
    21: (C_STEEL, "metal"),
}
GROUP = {"spreader": "shell", "cutter": "accessory", "ram": "internal", "pump": "internal", "kit": "internal"}
TOOL = {"spreader": "Spreader", "cutter": "Cutter", "ram": "Ram", "pump": "Pump", "kit": "Kit"}


def product_parts(P=PARAMS):
    out = []
    comps = components(P, spreader_stroke=50.0, cutter_travel=0.0)
    for c in comps:
        col, mat = LOOK[c.bom]
        out.append({"name": f"{TOOL[c.tool]}: {c.name}", "shape": c.shape, "color": col, "material": mat,
                    "bom": c.bom, "group": GROUP[c.tool], "explode": tuple(float(v) for v in c.explode)})
    # the bar to cut, standing up through the cutter's hook (the cutter lies flat at (650, 1150) on its lower plate)
    bar = zcyl(P["BAR_D"] / 2, 0.0, 420.0, x=650 + cutter_levels(P)["xb"], y=1150)
    out.append({"name": "16 mm reinforcing bar (not part of the kit)", "shape": bar, "color": C_BAR, "material": "metal",
                "bom": None, "group": "accessory", "explode": (0, 0, 0)})
    from context_parts import mannequin
    person = Pos(-450, 1150, 0) * Rot(0, 0, -90) * mannequin(1750, "stand")
    out.append({"name": "Person, 1.75 m, for scale", "shape": person, "color": "#D6D3D1", "material": "painted",
                "bom": None, "group": "context", "explode": (0, 0, 0)})
    return out
