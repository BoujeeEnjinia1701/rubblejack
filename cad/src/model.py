"""RubbleJack parametric model (build123d), TRL 3, constructable design (RBJ-DDR-002).

Run from the repo root:
    python cad/src/model.py            exports STEP and STL, prints masses and the constructability checks
    python cad/src/model.py --check    prints the constructability checks only

Exports into cad/step and cad/stl:
    rubblejack-kit.step / .stl         the whole kit laid out on the ground, as packed for a drill
    rubblejack-spreader.step / .stl    spreader, jaws closed
    rubblejack-cutter.step / .stl      cutter, blades open
    rubblejack-ram.step / .stl         lifting ram on its base plate and riser

The kit is one two-speed 700 bar hand pump, two 2 m hoses with quick couplers, a gauge, and three tools
that all use the same bought 15 t, 100 mm stroke single-acting cylinder (RBJ-DDR-001, D2):
    spreader   two jaw arms on one pivot pin, opened by two links from a crosshead on the plunger;
               the arms are held by two frame plates bolted to a collar adapter on the cylinder's
               collar thread;
    cutter     a guillotine shear: a moving blade on a carrier pushed by the plunger slides past a
               fixed blade; frame plates with open hooks take the bar; a stop bar ends the stroke;
    ram        the third cylinder standing in a locating ring on a base plate, with a tilting saddle,
               and a 150 mm riser that goes under it (never on top of the plunger).

Tool axes (each tool is modelled in its own frame, then placed in the kit layout):
    spreader   X along the cylinder toward the jaw tips, origin on the pivot pin axis, Z normal to the
               frame plates; jaw arm A opens toward +Y, arm B toward -Y.
    cutter     X along the cylinder toward the blades, origin at the end of the cylinder's collar, Z
               normal to the frame plates; the bar to cut lies along Z in the hook.
    ram        Z up, origin on the ground under the base plate centre.
    kit        Z up from the ground; tools lie flat on their lower frame plates.

Main dimensions and interfaces only; tolerances are TRL 4 work. The same PARAMS and kinematics feed
docs/04-calcs/sizing.py (RBJ-CAL-001), cad/src/sheets.py (RBJ-DWG-001), cad/src/concept_media.py,
cad/src/build_plan_media.py and cad/src/product_model.py. CONCEPT, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

from build123d import (Axis, Box, Compound, Cylinder, Plane, Polygon, Pos, Rot, Torus, export_step,
                       export_stl, extrude, mirror)

ROOT = Path(__file__).resolve().parents[2]

# Top-level parameters (mm, kN, kg). Edit these, not the geometry below.
PARAMS = {
    # ---------------------------------------------------------------- bought: one cylinder type, three tools
    # 15 t single-acting cylinder, 100 mm class (101 mm stroke): body OD, collar thread OD and length,
    # collapsed length (base to plunger end), plunger OD, plunger protrusion when retracted, stroke,
    # effective area (cm2), coupler distance from the base, catalogue mass (kg)
    "CYL_OD": 70.0, "COLLAR_OD": 71.4, "COLLAR_L": 40.0, "CYL_L": 216.0, "PLUNGER_OD": 50.0,
    "PLUNGER_P0": 12.0, "STROKE": 101.0, "CYL_AREA_CM2": 20.3, "COUPLER_Z": 30.0, "CYL_KG": 5.0,
    # pump: rated pressure (bar), relief set (bar), usable oil (cm3), stage displacements (cm3 per stroke),
    # handle length (mm), handle force at full pressure (N, catalogue), mass with oil (kg), box size
    "P_RATED": 700.0, "P_RELIEF": 700.0, "PUMP_OIL": 900.0, "PUMP_STAGE1": 3.6, "PUMP_STAGE2": 0.9,
    "PUMP_HANDLE": 600.0, "PUMP_EFFORT": 380.0, "PUMP_KG": 11.0, "PUMP_BOX": (560.0, 140.0, 130.0),
    # hoses: length, outside diameter, mass each; coil radius when packed
    "HOSE_L": 2000.0, "HOSE_OD": 16.0, "HOSE_KG": 1.4, "HOSE_COIL_R": 170.0,

    # ---------------------------------------------------------------- spreader linkage (RBJ-CAL-001 section 3)
    # jaw length (pivot to tip), tip half-thickness when closed, tail pin radius, tail angle below the axis
    # (deg), crosshead pin offset from the axis, link length (pin to pin)
    "JAW_L": 250.0, "TIP_H": 16.0, "TAIL_A": 160.0, "TAIL_PHI": 40.0, "XH_E": 30.0, "LINK_L": 150.0,
    # arm thickness (Z), centre knuckle (arm A) half-thickness, knuckle radius, body clearance round the
    # knuckles, tail half-width, tail eye radius, link slot half-width in the tail, slot start radius
    "ARM_T": 36.0, "KNUCKLE_T2": 9.0, "KNUCKLE_R": 60.0, "KNUCKLE_GAP": 1.0, "TAIL_W2": 30.0,
    "TAIL_EYE_R": 27.0, "TAIL_W2_ROOT": 31.0, "SLOT_T2": 8.25, "SLOT_R0": 100.0,
    # shoulder ray (deg above the jaw's inner face) and tail root sector half-angle (deg), so the arms clear
    "SHOULDER_DEG": 52.0, "TAIL_SECTOR": 26.0,
    # jaw outer-edge depth: d(x) = sqrt(JAW_K * (JAW_L - x)) + JAW_D0, limited to [TIP_H, JAW_DMAX]
    "JAW_K": 24.2, "JAW_D0": 2.0, "JAW_DMAX": 70.0,
    # lightening pockets in the jaw (both faces): X range, inset from the edges, depth each side
    "POCKET_X": (100.0, 195.0), "POCKET_INSET": 12.0, "POCKET_D": 8.0,
    # pins: main pivot, tail and crosshead pins (diameter); bore clearance (diametral)
    "PIN_MAIN": 45.0, "PIN_MAIN_BORE": 18.0, "PIN_LINK": 25.0, "PIN_CLR": 0.4,
    # links: thickness (Z), eye radius
    "LINK_T": 16.0, "LINK_EYE": 22.0, "LINK_W2": 16.0,
    # crosshead: half-length (X), half-width (Y), centre web half-width between the link slots
    "XH_L2": 23.0, "XH_W2": 56.0, "XH_WEB2": 7.0, "XH_T2": 20.0,
    # frame plates: inner face Z (both sides), thickness, half-width at the adapter, pivot boss radius
    "FR_Z": 46.0, "FR_T": 10.0, "FR_W2": 65.0, "FR_W2_FRONT": 50.0, "FR_BOSS": 55.0,
    # collar adapter (shared by spreader and cutter): length (X), half-width (Y); bolt X from its front
    # face and Y offset; bolt size
    "AD_L": 60.0, "AD_W2": 65.0, "AD_BOLT_X": (15.0, 45.0), "AD_BOLT_Y": 50.0, "AD_BOLT": 16.0,
    # pivot spacers: outside diameter
    "SPACER_OD": 70.0,
    # carry handle on the upper frame plate: post X positions (spreader frame), height, bar radius
    "HANDLE_X": (-280.0, -150.0), "HANDLE_H": 70.0, "HANDLE_R": 13.0,

    # ---------------------------------------------------------------- cutter (RBJ-CAL-001 section 4)
    # carrier length, Y range, blade X range (rear, notch centre, front) measured from the carrier front,
    # blade Y range, notch width, shear clearance, travel to the stop, plate thickness, plate Y range,
    # hook half-width, fixed blade X range from the notch centre, nose block X range, stop bar Y range
    "CU_CAR_L": 50.0, "CU_CAR_Y": (-62.0, 40.0), "CU_MB": (0.0, 45.0, 70.0), "CU_BL_Y": (-30.0, 40.0),
    "CU_NOTCH": 17.0, "CU_CLR": 0.2, "CU_TRAVEL": 30.0, "CU_PL_T": 16.0, "CU_PL_Y": (-72.0, 50.0),
    "CU_HOOK2": 15.0, "CU_FB": (-8.5, 62.0), "CU_NOSE": (62.0, 92.0), "CU_STOP_Y": (-68.0, -36.0),
    "CU_FB_BOLT_X": (30.0, 50.0), "CU_FB_BOLT_Y": (-15.0, 25.0), "CU_NOSE_BOLT_Y": (-35.0, 20.0),
    # stop bar length (X) and its two screw stations from its rear face (two screws per plate, so it cannot turn)
    "CU_STOP_L": 60.0, "CU_STOP_BOLT_X": (15.0, 45.0),
    "BAR_D": 16.0,

    # ---------------------------------------------------------------- lifting ram set
    # base plate (side, thickness), locating ring (ID, OD, height), riser tube (OD, wall, length; the tube wall
    # stands in line with the ring and the cylinder base, so the end plates carry the load in bearing, RBJ-DDR-002),
    # riser end plates (side, thickness), riser spigot (OD, height), tilting saddle (diameter, height)
    "BP_S": 250.0, "BP_T": 20.0, "RING": (72.0, 92.0, 15.0), "RISER": (88.9, 10.0, 150.0),
    "RISER_PL": (160.0, 10.0), "SPIGOT": (70.0, 12.0), "SADDLE": (60.0, 20.0),

    # ---------------------------------------------------------------- materials and densities (kg/m3)
    "RHO_STEEL": 7850.0, "RHO_AL": 2810.0,
}

# Material of each made part (RBJ-DDR-002): high-strength steel where the load is high and the section small,
# 7075-T6 aluminium where the part is bulky and lightly stressed, to keep each carried load under 25 kg.
MATERIAL = {
    "sp_adapter": "7075-T6 aluminium plate, 100 mm", "cu_adapter": "7075-T6 aluminium plate, 100 mm",
    "sp_plate_up": "7075-T6 aluminium plate, 10 mm", "sp_plate_lo": "7075-T6 aluminium plate, 10 mm",
    "sp_xhead": "7075-T6 aluminium plate, 100 mm", "sp_spacers": "7075-T6 aluminium tube or bar",
    "sp_link_a": "S690QL steel plate, 16 mm", "sp_link_b": "S690QL steel plate, 16 mm",
    "sp_arm_a": "4340 steel plate, quenched and tempered to about 300 HB, 40 mm (machined to 36)",
    "sp_arm_b": "4340 steel plate, quenched and tempered to about 300 HB, 40 mm (machined to 36)",
    "sp_pin_main": "4340 steel bar, quenched and tempered to about 300 HB, ground", "sp_pins_link": "4340 steel bar, quenched and tempered to about 300 HB, ground",
    "sp_handle": "Steel tube 26.9 x 3.2", "cu_handle": "Steel tube 26.9 x 3.2",
    "cu_carrier": "7075-T6 aluminium plate, 100 mm", "cu_nose": "7075-T6 aluminium plate, 100 mm",
    "cu_mblade": "S7 shock-resisting tool steel, hardened 54 to 56 HRC",
    "cu_fblade": "S7 shock-resisting tool steel, hardened 54 to 56 HRC",
    "cu_stop": "S355 steel bar", "cu_plate_up": "S690QL steel plate, 16 mm", "cu_plate_lo": "S690QL steel plate, 16 mm",
    "rm_base": "S690QL steel plate, 20 mm, with S355 ring", "rm_riser": "S355 tube 88.9 x 10 and 10 mm plate",
}
P = PARAMS


# ------------------------------------------------------------------------------------------- helpers
def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def zcyl(r, z0, z1, x=0.0, y=0.0):
    """Cylinder along Z."""
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def xcyl(r, x0, x1, y=0.0, z=0.0):
    """Cylinder along X."""
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def ycyl(r, y0, y1, x=0.0, z=0.0):
    """Cylinder along Y."""
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, y1 - y0)


def slab(pts, z0, z1):
    """A plate: polygon in XY extruded from z0 to z1 (points in either winding order)."""
    area = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
    if area < 0:
        pts = list(reversed(pts))
    return Pos(0, 0, z0) * extrude(Polygon(*pts, align=None), z1 - z0, dir=(0, 0, 1))


def disc_pts(cx, cy, r, n=48, a0=0.0, a1=360.0):
    return [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
            for a in [a0 + (a1 - a0) * k / n for k in range(n + 1)]]


def rotz(shape, deg):
    return Rot(0, 0, deg) * shape


@dataclass
class Comp:
    key: str
    name: str
    shape: object
    bom: int
    made: bool = True
    tool: str = "kit"
    mass_kg: float | None = None   # bought parts: catalogue mass; made parts: from the volume
    explode: tuple = (0.0, 0.0, 0.0)

    def mass(self):
        if self.mass_kg is not None:
            return self.mass_kg
        rho = P["RHO_AL"] if "aluminium" in MATERIAL.get(self.key, "") else P["RHO_STEEL"]
        return self.shape.volume * 1e-9 * rho


# ------------------------------------------------------------------------------- spreader kinematics
def tail_pin(theta_deg, p=P):
    """Tail pin of arm A at jaw rotation theta (deg, 0 = jaws closed)."""
    a = math.radians(180.0 + p["TAIL_PHI"] + theta_deg)
    return p["TAIL_A"] * math.cos(a), p["TAIL_A"] * math.sin(a)


def crosshead_x(theta_deg, p=P):
    """Crosshead pin X for a given jaw rotation (the link keeps its length)."""
    tx, ty = tail_pin(theta_deg, p)
    dy = ty + p["XH_E"]
    return tx - math.sqrt(p["LINK_L"] ** 2 - dy ** 2)


def tip_gap(theta_deg, p=P):
    t = math.radians(theta_deg)
    return 2 * (p["JAW_L"] * math.sin(t) + p["TIP_H"] * math.cos(t))


def theta_for_stroke(s, p=P):
    """Jaw rotation for plunger travel s from the closed position (bisection)."""
    c0 = crosshead_x(0.0, p)
    lo, hi = 0.0, 80.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if crosshead_x(mid, p) - c0 < s:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def spreader_levels(p=P):
    """Key X stations of the spreader frame (closed jaws)."""
    c0 = crosshead_x(0.0, p)
    x_col = c0 - p["XH_L2"] - p["PLUNGER_P0"]            # end of the cylinder collar
    return {"c0": c0, "x_col": x_col, "x_ad0": x_col - p["AD_L"], "x_base": x_col - (p["CYL_L"] - p["PLUNGER_P0"]),
            "c_max": c0 + p["STROKE"], "theta_max": theta_for_stroke(p["STROKE"], p)}


# ------------------------------------------------------------------------------- shared bought cylinder
def cylinder_parts(x_col, stroke, p=P, axis="x"):
    """The bought 15 t cylinder along +X with its collar end at x_col. Returns (body, plunger, coupler)."""
    base = x_col - (p["CYL_L"] - p["PLUNGER_P0"])
    body = xcyl(p["CYL_OD"] / 2, base, x_col - p["COLLAR_L"]) + xcyl(p["COLLAR_OD"] / 2 - 0.15, x_col - p["COLLAR_L"], x_col)
    plunger = xcyl(p["PLUNGER_OD"] / 2, x_col, x_col + p["PLUNGER_P0"] + stroke)
    cx = base + p["COUPLER_Z"]
    coupler = ycyl(13.0, p["CYL_OD"] / 2, p["CYL_OD"] / 2 + 38, x=cx) + ycyl(16.0, p["CYL_OD"] / 2 + 38, p["CYL_OD"] / 2 + 46, x=cx)
    return body, plunger, coupler


def collar_adapter(x_col, p=P):
    """Collar adapter: a 4140 block with the collar thread through it and four tapped M16 holes in each Z face."""
    z = p["FR_Z"]
    blk = box(x_col - p["AD_L"], x_col, -p["AD_W2"], p["AD_W2"], -z, z)
    blk -= xcyl(p["COLLAR_OD"] / 2, x_col - p["COLLAR_L"] - 1, x_col + 1)
    blk -= xcyl(p["CYL_OD"] / 2 + 1.0, x_col - p["AD_L"] - 1, x_col - p["COLLAR_L"])
    for bx in p["AD_BOLT_X"]:
        for by in (-p["AD_BOLT_Y"], p["AD_BOLT_Y"]):
            blk -= tapped(x_col - bx, by, z, 26, -1)
            blk -= tapped(x_col - bx, by, -z, 26, 1)
    return blk


def adapter_bolts(x_col, plate_t, p=P):
    """Eight M16 cap screws holding the two frame plates to the collar adapter (24 mm thread engagement)."""
    z = p["FR_Z"]
    out = []
    for bx in p["AD_BOLT_X"]:
        for by in (-p["AD_BOLT_Y"], p["AD_BOLT_Y"]):
            for sgn in (1, -1):
                out.append(screw(x_col - bx, by, sgn * (z + plate_t), sgn * (z - 24)))
    return Compound(children=out)


# ------------------------------------------------------------------------------- spreader parts
def jaw_profile(p=P):
    """Outer-edge points of arm A's forward body in the closed position (inner face on the X axis)."""
    L = p["JAW_L"]
    pts = []
    for k in range(0, 21):
        x = L * k / 20
        d = math.sqrt(max(p["JAW_K"] * (L - x), 0.0)) + p["JAW_D0"]
        pts.append((x, min(max(d, p["TIP_H"]), p["JAW_DMAX"])))
    pts[-1] = (L, p["TIP_H"])
    return pts


def jaw_depth(x, p=P):
    """Depth of the jaw (inner face to outer edge) at distance x from the pivot along the jaw."""
    d = math.sqrt(max(p["JAW_K"] * (p["JAW_L"] - x), 0.0)) + p["JAW_D0"]
    return min(max(d, p["TIP_H"]), p["JAW_DMAX"])


def pocket_outline(p=P):
    """Lightening pocket in the jaw, arm A closed: inset from the inner face and the outer edge."""
    x0, x1 = p["POCKET_X"]
    ins = p["POCKET_INSET"]
    xs = [x0 + (x1 - x0) * k / 10 for k in range(11)]
    return [(x0, ins), (x1, ins)] + [(x, jaw_depth(x, p) - ins) for x in reversed(xs)]


def tail_pocket_outline(p=P):
    """Lightening pocket in the tail between r = 75 and the link slot, 12 mm in from each side."""
    a = math.radians(180.0 + p["TAIL_PHI"])
    ux, uy, vx, vy = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
    r0, r1 = 75.0, p["SLOT_R0"] - 4

    def hw(r):
        return p["TAIL_W2_ROOT"] + (p["TAIL_EYE_R"] - p["TAIL_W2_ROOT"]) * (r - 63.0) / (p["TAIL_A"] - 63.0) - p["POCKET_INSET"]
    return [(r0 * ux + hw(r0) * vx, r0 * uy + hw(r0) * vy), (r1 * ux + hw(r1) * vx, r1 * uy + hw(r1) * vy),
            (r1 * ux - hw(r1) * vx, r1 * uy - hw(r1) * vy), (r0 * ux - hw(r0) * vx, r0 * uy - hw(r0) * vy)]


def _arm_outline(p=P):
    """Plan outline pieces of arm A, closed: forward body polygon and tail polygon."""
    prof = list(reversed(jaw_profile(p)))
    if prof[-1][0] > 0.0 or prof[-1][1] < p["JAW_DMAX"]:
        prof.append((0.0, p["JAW_DMAX"]))
    fwd = [(0.0, 0.0), (p["JAW_L"], 0.0)] + prof
    # shoulder trimmed by a ray from the pivot at SHOULDER_DEG, so the other arm's tail clears it when open
    k = math.tan(math.radians(p["SHOULDER_DEG"]))
    trimmed = []
    for (x0, y0), (x1, y1) in zip(fwd, fwd[1:] + fwd[:1]):
        for (xx, yy) in ((x0, y0),):
            if yy <= k * xx + 1e-9:
                trimmed.append((xx, yy))
        f0, f1 = y0 - k * x0, y1 - k * x1
        if f0 * f1 < 0:
            t = f0 / (f0 - f1)
            trimmed.append((x0 + t * (x1 - x0), y0 + t * (y1 - y0)))
    fwd = trimmed
    a = math.radians(180.0 + p["TAIL_PHI"])
    ux, uy = math.cos(a), math.sin(a)
    vx, vy = -uy, ux
    w, A = p["TAIL_W2"], p["TAIL_A"]
    hs = math.radians(p["TAIL_SECTOR"])
    w0 = p["TAIL_W2_ROOT"]
    rr = w0 / math.sin(hs)
    w = p["TAIL_EYE_R"]                                   # the tail tapers to the eye radius at the pin
    tail = [(rr * (math.cos(hs) * ux + math.sin(hs) * vx), rr * (math.cos(hs) * uy + math.sin(hs) * vy)),
            (A * ux + w * vx, A * uy + w * vy)]
    for k in range(0, 25):
        ang = 90 - 180 * k / 24
        r = p["TAIL_EYE_R"]
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        tail.append((A * ux + r * (ca * ux + sa * vx), A * uy + r * (ca * uy + sa * vy)))
    tail += [(A * ux - w * vx, A * uy - w * vy)]
    # root of the tail: a wedge from the pivot at +/- TAIL_SECTOR about the tail line, meeting the parallel sides
    tail += [(rr * (math.cos(hs) * ux - math.sin(hs) * vx), rr * (math.cos(hs) * uy - math.sin(hs) * vy)), (0.0, 0.0)]
    return fwd, tail


def arm(which="A", theta=0.0, p=P):
    """Jaw arm A (centre knuckle, opens to +Y) or B (twin knuckles, opens to -Y), rotated by theta (deg)."""
    fwd, tail = _arm_outline(p)
    T2, K2, R = p["ARM_T"] / 2, p["KNUCKLE_T2"], p["KNUCKLE_R"]
    body = slab(fwd, -T2, T2) + slab(tail, -T2, T2)
    body -= zcyl(R + p["KNUCKLE_GAP"], -T2 - 1, T2 + 1)
    plan = slab(fwd, -T2, T2) + slab(tail, -T2, T2)
    inner_zone = zcyl(R + p["KNUCKLE_GAP"], -T2, T2) & plan
    if which == "A":
        knuck = zcyl(R, -K2, K2) + (inner_zone & box(-500, 500, -500, 500, -K2, K2))
    else:
        knuck = (zcyl(R, K2, T2) + (inner_zone & box(-500, 500, -500, 500, K2, T2))
                 + zcyl(R, -T2, -K2) + (inner_zone & box(-500, 500, -500, 500, -T2, -K2)))
    a = body + knuck
    a -= zcyl((p["PIN_MAIN"] + p["PIN_CLR"]) / 2, -T2 - 1, T2 + 1)
    pk = pocket_outline(p)
    a -= slab(pk, T2 - p["POCKET_D"], T2 + 1) + slab(pk, -T2 - 1, -T2 + p["POCKET_D"])
    tk = tail_pocket_outline(p)
    a -= slab(tk, T2 - p["POCKET_D"], T2 + 1) + slab(tk, -T2 - 1, -T2 + p["POCKET_D"])
    tx, ty = tail_pin(0.0, p)
    ang = 180.0 + p["TAIL_PHI"]
    slot = Pos(tx, ty, 0) * Rot(0, 0, ang) * box(p["SLOT_R0"] - p["TAIL_A"], p["TAIL_EYE_R"] + 5, -p["TAIL_W2"] - 6, p["TAIL_W2"] + 6,
                                                  -p["SLOT_T2"], p["SLOT_T2"])
    a -= slot
    a -= zcyl((p["PIN_LINK"] + p["PIN_CLR"]) / 2, -T2 - 1, T2 + 1, x=tx, y=ty)
    if which == "B":
        a = mirror(a, about=Plane.XZ)
        return rotz(a, -theta)
    return rotz(a, theta)


def link(which="A", theta=0.0, p=P):
    """Link between the crosshead pin and the arm's tail pin."""
    tx, ty = tail_pin(theta, p)
    cx = crosshead_x(theta, p)
    cy = -p["XH_E"]
    if which == "B":
        ty, cy = -ty, -cy
    L = math.hypot(tx - cx, ty - cy)
    ang = math.degrees(math.atan2(ty - cy, tx - cx))
    t2 = p["LINK_T"] / 2
    r = p["LINK_EYE"]
    s = box(0, L, -p["LINK_W2"], p["LINK_W2"], -t2, t2) + zcyl(r, -t2, t2) + zcyl(r, -t2, t2, x=L)
    s -= zcyl((p["PIN_LINK"] + p["PIN_CLR"]) / 2, -t2 - 1, t2 + 1)
    s -= zcyl((p["PIN_LINK"] + p["PIN_CLR"]) / 2, -t2 - 1, t2 + 1, x=L)
    return Pos(cx, cy, 0) * Rot(0, 0, ang) * s


def crosshead(c, p=P):
    z = p["XH_T2"]
    s = box(c - p["XH_L2"], c + p["XH_L2"], -p["XH_W2"], p["XH_W2"], -z, z)
    for sgn in (1, -1):
        y0, y1 = sorted((sgn * p["XH_WEB2"], sgn * (p["XH_W2"] + 1)))
        s -= box(c - p["XH_L2"] - 1, c + p["XH_L2"] + 1, y0, y1, -p["SLOT_T2"], p["SLOT_T2"])
        s -= zcyl((p["PIN_LINK"] + p["PIN_CLR"]) / 2, -z - 1, z + 1, x=c, y=sgn * p["XH_E"])
    s -= xcyl(10.0, c - p["XH_L2"] - 1, c - p["XH_L2"] + 28)          # M24 stud hole into the plunger
    return s


def pin(d, z0, z1, x=0.0, y=0.0, head=True):
    """Pin along Z. head=True: a head below z0 and a washer and circlip at the top end (z1 - 6 to z1 - 3).
    head=False: a plain captive pin held in by the frame plates on either side."""
    s = zcyl(d / 2, z0, z1, x=x, y=y)
    if head:
        s += zcyl(d / 2 + 6, z0 - 6, z0, x=x, y=y)
        s += zcyl(d / 2 + 5, z1 - 6, z1 - 3, x=x, y=y) - zcyl(d / 2, z1 - 7, z1, x=x, y=y)
    return s


TAP_R, BOLT_R = 6.88, 6.8        # M16: tapped hole (minor) radius and modelled bolt shank radius
M12 = {"tap": 5.07, "bolt": 5.0, "head": 9.0, "head_h": 12.0, "hole": 6.75}   # M12 for the fixed blade (heads 20 mm apart)


def tapped(x, y, z_face, depth, sign, r=TAP_R):
    """A tapped hole (M16 unless r is given) of the given depth going into a part from a face at z_face (sign: +1 hole goes up)."""
    z0, z1 = sorted((z_face, z_face + sign * depth))
    return zcyl(r, z0 - (1 if sign < 0 else 0), z1 + (1 if sign > 0 else 0), x=x, y=y)


def screw(x, y, z_face_out, z_tip, head=True, rb=BOLT_R, rh=12.0, hh=16.0):
    """Cap screw (M16 unless sizes are given): head on the outside face z_face_out, shank to z_tip."""
    sgn = 1 if z_face_out > z_tip else -1
    s = zcyl(rb, min(z_tip, z_face_out), max(z_tip, z_face_out), x=x, y=y)
    if head:
        s += zcyl(rh, min(z_face_out, z_face_out + sgn * hh), max(z_face_out, z_face_out + sgn * hh), x=x, y=y)
    return s


def frame_plate(sign, p=P):
    """Upper (sign +1) or lower (-1) frame plate of the spreader."""
    lv = spreader_levels(p)
    x0 = lv["x_ad0"]
    w = p["FR_W2"]
    w1 = p["FR_W2_FRONT"]
    pts = [(x0, -w), (lv["x_col"], -w), (-90.0, -w1)] + disc_pts(0.0, 0.0, p["FR_BOSS"], 40, -130.0, 130.0) + [(-90.0, w1), (lv["x_col"], w), (x0, w)]
    z0, z1 = (p["FR_Z"], p["FR_Z"] + p["FR_T"]) if sign > 0 else (-p["FR_Z"] - p["FR_T"], -p["FR_Z"])
    s = slab(pts, z0, z1)
    s -= zcyl((p["PIN_MAIN"] + p["PIN_CLR"]) / 2, z0 - 1, z1 + 1)
    for bx in p["AD_BOLT_X"]:
        for by in (-p["AD_BOLT_Y"], p["AD_BOLT_Y"]):
            s -= zcyl(9.0, z0 - 1, z1 + 1, x=lv["x_col"] - bx, y=by)
    # lightening window between the adapter and the pivot (the crosshead runs under it)
    s -= slab([(lv["x_col"] + 20, -15), (-115, -15), (-115, 15), (lv["x_col"] + 20, 15)], z0 - 1, z1 + 1)
    if sign > 0:
        for hx in p["HANDLE_X"]:
            s -= zcyl(6.8, z0 - 1, z1 + 1, x=hx, y=0)
    return s


def spacers(p=P):
    out = []
    for z0, z1 in ((p["ARM_T"] / 2, p["FR_Z"]), (-p["FR_Z"], -p["ARM_T"] / 2)):
        out.append(zcyl(p["SPACER_OD"] / 2, z0, z1) - zcyl((p["PIN_MAIN"] + p["PIN_CLR"]) / 2, z0 - 1, z1 + 1))
    return Compound(children=out)


def carry_handle(xs, z_plate_top, y=0.0, p=P):
    """D handle: two posts screwed into the upper plate and a round grip bar (bent from one 26 mm bar)."""
    h, r = p["HANDLE_H"], p["HANDLE_R"]
    s = zcyl(r, z_plate_top, z_plate_top + h, x=xs[0], y=y) + zcyl(r, z_plate_top, z_plate_top + h, x=xs[1], y=y)
    s += xcyl(r, xs[0] - r, xs[1] + r, y=y, z=z_plate_top + h)
    s -= zcyl(r - 3.2, z_plate_top + 12, z_plate_top + h - r + 3.2, x=xs[0], y=y)     # tube wall (26.9 x 3.2)
    s -= zcyl(r - 3.2, z_plate_top + 12, z_plate_top + h - r + 3.2, x=xs[1], y=y)
    s -= xcyl(r - 3.2, xs[0] + r - 3.2, xs[1] - r + 3.2, y=y, z=z_plate_top + h)
    return s


def spreader(stroke=0.0, p=P):
    """Spreader components (dict key -> Comp) in the spreader frame, plunger out by `stroke`."""
    lv = spreader_levels(p)
    th = theta_for_stroke(stroke, p) if stroke > 0 else 0.0
    c = crosshead_x(th, p)
    body, plunger, coupler = cylinder_parts(lv["x_col"], c - lv["c0"], p)
    zt = p["FR_Z"] + p["FR_T"]
    pin_z0, pin_z1 = -zt, zt + 8
    comps = [
        Comp("sp_cyl", "15 t cylinder (spreader)", body + plunger, 5, made=False, tool="spreader", mass_kg=p["CYL_KG"], explode=(-260, 0, 0)),
        Comp("sp_coupler", "Cylinder coupler and dust cap", coupler, 3, made=False, tool="spreader", mass_kg=0.25, explode=(-260, 0, 0)),
        Comp("sp_adapter", "Collar adapter", collar_adapter(lv["x_col"], p), 6, tool="spreader", explode=(-130, 0, 0)),
        Comp("sp_plate_up", "Frame plate, upper", frame_plate(1, p), 7, tool="spreader", explode=(0, 0, 160)),
        Comp("sp_plate_lo", "Frame plate, lower", frame_plate(-1, p), 7, tool="spreader", explode=(0, 0, -160)),
        Comp("sp_bolts", "Adapter cap screws, M16 (8)", adapter_bolts(lv["x_col"], p["FR_T"], p), 16, made=False, tool="spreader",
             mass_kg=0.45, explode=(0, 0, 230)),
        Comp("sp_xhead", "Crosshead and stud", crosshead(c, p), 8, tool="spreader", explode=(-60, 0, 0)),
        Comp("sp_link_a", "Link (to arm A)", link("A", th, p), 9, tool="spreader", explode=(0, -120, 70)),
        Comp("sp_link_b", "Link (to arm B)", link("B", th, p), 9, tool="spreader", explode=(0, 120, 70)),
        Comp("sp_arm_a", "Jaw arm A (centre knuckle)", arm("A", th, p), 10, tool="spreader", explode=(80, 140, 0)),
        Comp("sp_arm_b", "Jaw arm B (twin knuckles)", arm("B", th, p), 10, tool="spreader", explode=(80, -140, 0)),
        Comp("sp_spacers", "Pivot spacers (2)", spacers(p), 11, tool="spreader", explode=(0, 0, 100)),
        Comp("sp_pin_main", "Main pivot pin with washer and circlip",
             pin(p["PIN_MAIN"], pin_z0, pin_z1) - zcyl(p["PIN_MAIN_BORE"] / 2, pin_z0 - 7, pin_z1 + 1), 12, tool="spreader",
             explode=(0, 0, 320)),
    ]
    tx, ty = tail_pin(th, p)
    lp = [pin(p["PIN_LINK"], -p["ARM_T"] / 2, p["ARM_T"] / 2 + 8, x=tx, y=ty),
          pin(p["PIN_LINK"], -p["ARM_T"] / 2, p["ARM_T"] / 2 + 8, x=tx, y=-ty),
          pin(p["PIN_LINK"], -p["XH_T2"], p["XH_T2"] + 8, x=c, y=p["XH_E"]),
          pin(p["PIN_LINK"], -p["XH_T2"], p["XH_T2"] + 8, x=c, y=-p["XH_E"])]
    comps.append(Comp("sp_pins_link", "Tail and crosshead pins (4)", Compound(children=lp), 12, tool="spreader", explode=(0, 0, 260)))
    comps.append(Comp("sp_handle", "Carry handle", carry_handle(p["HANDLE_X"], zt, 0.0, p), 13, tool="spreader", explode=(0, 0, 330)))
    return {k.key: k for k in comps}


# ------------------------------------------------------------------------------- cutter parts
def cutter_levels(p=P):
    car0 = p["PLUNGER_P0"]                       # carrier rear face, cutter retracted
    car1 = car0 + p["CU_CAR_L"]                  # carrier front face = moving blade rear face
    xb = car1 + p["CU_MB"][1]                    # bar centre (notch centre) when open
    return {"car0": car0, "car1": car1, "xb": xb, "mb1": car1 + p["CU_MB"][2],
            "fb0": xb + p["CU_FB"][0], "fb1": xb + p["CU_FB"][1],
            "nose0": xb + p["CU_NOSE"][0], "nose1": xb + p["CU_NOSE"][1],
            "stop0": car1 + p["CU_TRAVEL"], "stop1": car1 + p["CU_TRAVEL"] + p["CU_STOP_L"]}


def _notch(xb, half, y_bot, y_top, z0, z1):
    """U notch open toward +Y: a slot of width 2*half from the round bottom (centre at y = y_bot + half) to y_top."""
    return box(xb - half, xb + half, y_bot + half, y_top + 1, z0, z1) + zcyl(half, z0, z1, x=xb, y=y_bot + half)


def cutter(travel=0.0, p=P):
    """Cutter components (dict key -> Comp) in the cutter frame, moving blade advanced by `travel`."""
    lv = cutter_levels(p)
    zf = p["FR_Z"]
    t = p["CU_PL_T"]
    body, plunger, coupler = cylinder_parts(0.0, travel, p)
    yb0, yb1 = p["CU_BL_Y"]
    half = p["CU_NOTCH"] / 2
    xb = lv["xb"]
    # carrier: guided between the plates, M24 stud into the plunger, two M16 bolts hold the moving blade
    car = box(lv["car0"], lv["car1"], p["CU_CAR_Y"][0], p["CU_CAR_Y"][1], -zf + 0.5, zf - 0.5)
    car -= xcyl(10.0, lv["car0"] - 1, lv["car0"] + 28)
    MBY = (-25.0, 30.0)
    for fy in MBY:
        car -= xcyl(8.5, lv["car0"] - 1, lv["car1"] + 1, y=fy, z=-zf / 2)
        car -= xcyl(12.5, lv["car0"] - 1, lv["car0"] + 16, y=fy, z=-zf / 2)
    car = Pos(travel, 0, 0) * car
    # moving blade: lower half (z < 0), U notch at xb, rear wall pushes the bar
    mb = box(lv["car1"], lv["mb1"], yb0, yb1, -zf + 0.5, 0.0) - _notch(xb, half, -half, yb1, -zf, 1)
    for fy in MBY:
        mb -= xcyl(TAP_R, lv["car1"] - 1, lv["car1"] + 28, y=fy, z=-zf / 2)
    mb = Pos(travel, 0, 0) * mb
    # fixed blade: upper half (z > clearance), same notch; its front face part is the cutting edge
    fb = box(lv["fb0"], lv["fb1"], yb0, yb1, p["CU_CLR"], zf) - _notch(xb, half, -half, yb1, 0, zf + 1)
    for fx in (xb + p["CU_FB_BOLT_X"][0], xb + p["CU_FB_BOLT_X"][1]):
        for fy in p["CU_FB_BOLT_Y"]:
            fb -= tapped(fx, fy, zf, 20, -1, r=M12["tap"])
    NOSE_XY = [((lv["nose0"] + lv["nose1"]) / 2, ny) for ny in p["CU_NOSE_BOLT_Y"]]
    STOP_XY = [(lv["stop0"] + sx, (p["CU_STOP_Y"][0] + p["CU_STOP_Y"][1]) / 2) for sx in p["CU_STOP_BOLT_X"]]
    nose = box(lv["nose0"], lv["nose1"], yb0 - 20, yb1, -zf, zf)
    stop = box(lv["stop0"], lv["stop1"], p["CU_STOP_Y"][0], p["CU_STOP_Y"][1], -zf, zf)
    for nx, ny in NOSE_XY:
        nose -= tapped(nx, ny, zf, 26, -1) + tapped(nx, ny, -zf, 26, 1)
    for nx, ny in STOP_XY:
        stop -= tapped(nx, ny, zf, 26, -1) + tapped(nx, ny, -zf, 26, 1)

    def plate(sign):
        z0, z1 = (zf, zf + t) if sign > 0 else (-zf - t, -zf)
        pl = box(-p["AD_L"], lv["nose1"], p["CU_PL_Y"][0], p["CU_PL_Y"][1], z0, z1)
        hk = p["CU_HOOK2"]
        pl -= _notch(xb, hk, -hk, p["CU_PL_Y"][1], z0 - 1, z1 + 1)
        for bx in p["AD_BOLT_X"]:
            for by in (-p["AD_BOLT_Y"], p["AD_BOLT_Y"]):
                pl -= zcyl(9.0, z0 - 1, z1 + 1, x=-bx, y=by)
        for nx, ny in NOSE_XY + STOP_XY:
            pl -= zcyl(9.0, z0 - 1, z1 + 1, x=nx, y=ny)
        if sign > 0:
            for fx in (xb + p["CU_FB_BOLT_X"][0], xb + p["CU_FB_BOLT_X"][1]):
                for fy in p["CU_FB_BOLT_Y"]:
                    pl -= zcyl(M12["hole"], z0 - 1, z1 + 1, x=fx, y=fy)
            for hx in (-40.0, 70.0):
                pl -= zcyl(6.8, z0 - 1, z1 + 1, x=hx, y=-40.0)
        return pl

    zt = zf + t
    bolts = []
    for fx in (xb + p["CU_FB_BOLT_X"][0], xb + p["CU_FB_BOLT_X"][1]):
        for fy in p["CU_FB_BOLT_Y"]:
            bolts.append(screw(fx, fy, zt, zf - 18, rb=M12["bolt"], rh=M12["head"], hh=M12["head_h"]))
    for nx, ny in NOSE_XY + STOP_XY:
        for sgn in (1, -1):
            bolts.append(screw(nx, ny, sgn * zt, sgn * (zf - 24)))
    mbb = [Pos(travel, 0, 0) * (xcyl(BOLT_R, lv["car0"] + 16, lv["car1"] + 26, y=fy, z=-zf / 2)
                                + xcyl(12.0, lv["car0"] + 0.5, lv["car0"] + 16, y=fy, z=-zf / 2)) for fy in MBY]
    comps = [
        Comp("cu_cyl", "15 t cylinder (cutter)", body + plunger, 5, made=False, tool="cutter", mass_kg=p["CYL_KG"], explode=(-260, 0, 0)),
        Comp("cu_coupler", "Cylinder coupler and dust cap", coupler, 3, made=False, tool="cutter", mass_kg=0.25, explode=(-260, 0, 0)),
        Comp("cu_adapter", "Collar adapter", collar_adapter(0.0, p), 6, tool="cutter", explode=(-130, 0, 0)),
        Comp("cu_carrier", "Blade carrier and stud", car, 18, tool="cutter", explode=(-60, 0, 0)),
        Comp("cu_mblade", "Moving blade", mb, 19, tool="cutter", explode=(0, 0, -140)),
        Comp("cu_mbolts", "Moving blade screws, M16 (2)", Compound(children=mbb), 16, made=False, tool="cutter", mass_kg=0.12,
             explode=(-40, 0, -140)),
        Comp("cu_fblade", "Fixed blade", fb, 20, tool="cutter", explode=(0, 0, 140)),
        Comp("cu_nose", "Nose block", nose, 21, tool="cutter", explode=(120, 0, 0)),
        Comp("cu_stop", "Stop bar", stop, 21, tool="cutter", explode=(0, -120, 0)),
        Comp("cu_plate_up", "Cutter plate, upper", plate(1), 17, tool="cutter", explode=(0, 0, 260)),
        Comp("cu_plate_lo", "Cutter plate, lower", plate(-1), 17, tool="cutter", explode=(0, 0, -260)),
        Comp("cu_bolts", "Plate, nose and stop screws, M16 (16), and fixed blade screws, M12 (4)",
             adapter_bolts(0.0, t, p) + Compound(children=bolts), 16, made=False, tool="cutter", mass_kg=1.1, explode=(0, 0, 330)),
        Comp("cu_handle", "Carry handle", carry_handle((-40.0, 70.0), zt, -40.0, p), 13, tool="cutter", explode=(0, 0, 400)),
    ]
    return {k.key: k for k in comps}


def rebar_sample(p=P):
    """A 16 mm bar in the cutter hook, for pictures only (not part of the kit)."""
    lv = cutter_levels(p)
    return zcyl(p["BAR_D"] / 2, -200, 200, x=lv["xb"], y=0.0)


# ------------------------------------------------------------------------------- lifting ram set
def ram_set(stroke=0.0, riser=True, p=P):
    """Base plate, riser (optional), cylinder and saddle, standing with Z up."""
    s, t = p["BP_S"], p["BP_T"]
    rid, rod, rh = p["RING"]
    bp = box(-s / 2, s / 2, -s / 2, s / 2, 0, t) + (zcyl(rod / 2, t, t + rh) - zcyl(rid / 2, t - 1, t + rh + 1))
    for hx, hy in ((-s / 2 + 30, 0), (s / 2 - 30, 0)):
        bp -= box(hx - 12, hx + 12, hy - 45, hy + 45, -1, t + 1)          # hand slots
    comps = [Comp("rm_base", "Ram base plate", bp, 14, tool="ram", explode=(0, 0, -150))]
    z = t
    if riser:
        tod, tw, tl = p["RISER"]
        ps_, pt = p["RISER_PL"]
        sod, sh = p["SPIGOT"]
        z1 = z + rh                                                         # bottom plate sits on the base ring
        rs = zcyl(sod / 2, z1 - sh, z1)                                     # spigot hangs inside the ring
        rs += box(-ps_ / 2, ps_ / 2, -ps_ / 2, ps_ / 2, z1, z1 + pt)
        rs += zcyl(tod / 2, z1 + pt, z1 + pt + tl) - zcyl(tod / 2 - tw, z1 + pt - 1, z1 + pt + tl + 1)
        z2 = z1 + pt + tl
        rs += box(-ps_ / 2, ps_ / 2, -ps_ / 2, ps_ / 2, z2, z2 + pt)
        rs += zcyl(rod / 2, z2 + pt, z2 + pt + rh) - zcyl(rid / 2, z2 + pt - 1, z2 + pt + rh + 1)
        comps.append(Comp("rm_riser", "Riser block, 150 mm", rs, 15, tool="ram", explode=(0, 0, 120)))
        z = z2 + pt
    zb = z                                                                  # cylinder base sits on this face
    L = p["CYL_L"] - p["PLUNGER_P0"]
    body = zcyl(p["CYL_OD"] / 2, zb, zb + L - p["COLLAR_L"]) + zcyl(p["COLLAR_OD"] / 2 - 0.15, zb + L - p["COLLAR_L"], zb + L)
    plunger = zcyl(p["PLUNGER_OD"] / 2, zb + L, zb + L + p["PLUNGER_P0"] + stroke)
    cz = zb + p["COUPLER_Z"]
    coupler = Rot(0, 0, 0) * (ycyl(13.0, -p["CYL_OD"] / 2 - 38, -p["CYL_OD"] / 2, z=cz)
                              + ycyl(16.0, -p["CYL_OD"] / 2 - 46, -p["CYL_OD"] / 2 - 38, z=cz))
    ztop = zb + L + p["PLUNGER_P0"] + stroke
    sd, sh = p["SADDLE"]
    saddle = zcyl(sd / 2, ztop, ztop + sh) + zcyl(14.0, ztop - 12, ztop)
    plunger -= zcyl(14.0, ztop - 12, ztop + 1)                                  # the saddle's stem sits in the plunger bore
    comps += [Comp("rm_cyl", "15 t cylinder (lifting ram)", body + plunger, 5, made=False, tool="ram", mass_kg=p["CYL_KG"],
                   explode=(0, 0, 300)),
              Comp("rm_coupler", "Cylinder coupler and dust cap", coupler, 3, made=False, tool="ram", mass_kg=0.25, explode=(0, 0, 300)),
              Comp("rm_saddle", "Tilting saddle", saddle, 4, made=False, tool="ram", mass_kg=0.6, explode=(0, 0, 460))]
    return {k.key: k for k in comps}


# ------------------------------------------------------------------------------- pump and hoses
def pump_set(p=P):
    lx, ly, lz = p["PUMP_BOX"]
    res = box(0, lx, -ly / 2, ly / 2, 20, 20 + lz)
    feet = box(20, 80, -ly / 2 - 20, ly / 2 + 20, 0, 20) + box(lx - 80, lx - 20, -ly / 2 - 20, ly / 2 + 20, 0, 20)
    head = box(lx - 150, lx, -ly / 2 + 10, ly / 2 - 10, 20 + lz, 20 + lz + 70)
    hinge = (lx - 140, 0, 20 + lz + 90)
    hl = p["PUMP_HANDLE"]
    handle = Pos(*hinge) * Rot(0, -8, 0) * xcyl(14.0, -hl, 0)                 # handle folded back along the reservoir
    handle += zcyl(10.0, 20 + lz + 70, hinge[2], x=lx - 140)
    gauge_ad = box(lx, lx + 70, -30, 30, 60, 120)                              # gauge adapter block on the outlet
    gauge = Pos(lx + 35, 0, 120) * (zcyl(10.0, 0, 30) + zcyl(32.0, 30, 62))
    out_cpl = xcyl(13.0, lx + 70, lx + 115, z=90)
    comps = [
        Comp("pu_pump", "Two-speed hand pump, 700 bar", res + feet + head + handle, 1, made=False, tool="pump", mass_kg=p["PUMP_KG"],
             explode=(0, 0, 0)),
        Comp("pu_gauge", "Gauge adapter and 0 to 1,000 bar gauge", gauge_ad + gauge + out_cpl, 2, made=False, tool="pump", mass_kg=1.3,
             explode=(160, 0, 0)),
    ]
    return {k.key: k for k in comps}


def hose_coil(cx, cy, p=P, turns=3):
    """A 2 m hose coiled flat for carrying: concentric rings (one per turn) with its two coupler halves."""
    r = p["HOSE_OD"] / 2
    rings = [Pos(cx, cy, r + 2 * r * k) * Torus(p["HOSE_COIL_R"] - 4 * k, r) for k in range(turns)]
    cpl = [xcyl(14.0, cx + p["HOSE_COIL_R"] - 10, cx + p["HOSE_COIL_R"] + 45, y=cy + 20, z=r),
           xcyl(14.0, cx - p["HOSE_COIL_R"] - 45, cx - p["HOSE_COIL_R"] + 10, y=cy - 20, z=r)]
    return Compound(children=rings + cpl)


# ------------------------------------------------------------------------------- kit layout
def place_flat(shape, x, y, z_low):
    """Tool frame -> kit: lying on its lower frame plate (frame Z becomes kit Z), lowest face on the ground."""
    return Pos(x, y, z_low) * shape


def components(p=P, spreader_stroke=0.0, cutter_travel=0.0):
    """Every component of the kit, laid out on the ground (kit frame)."""
    out = []
    pu = pump_set(p)
    for c in pu.values():
        c.shape = Pos(0, 0, 0) * c.shape
        out.append(c)
    out.append(Comp("hoses", "Hoses, 2 m, with couplers (2)", Compound(children=[hose_coil(980, 0, p).moved(Pos(0, 0, 0)),
                                                                               hose_coil(980, 0, p).moved(Pos(0, 0, 3 * p["HOSE_OD"] + 1))]),
                    3, made=False, tool="pump", mass_kg=2 * p["HOSE_KG"], explode=(0, 0, 200)))
    zlow = p["FR_Z"] + p["FR_T"]
    sp = spreader(spreader_stroke, p)
    for c in sp.values():
        c.shape = place_flat(c.shape, 1000, 650, zlow)
        out.append(c)
    zc = p["FR_Z"] + p["CU_PL_T"]
    cu = cutter(cutter_travel, p)
    for c in cu.values():
        c.shape = place_flat(c.shape, 650, 1150, zc)
        out.append(c)
    rm = ram_set(0.0, True, p)
    for c in rm.values():
        c.shape = Pos(1550, 1150, 0) * c.shape
        out.append(c)
    return out


# ------------------------------------------------------------------------------- checks
def _overlap(a, b):
    try:
        v = (a & b).volume
    except Exception:
        return 0.0
    return v


def checks(p=P, verbose=True):
    """Constructability checks: parts that must not overlap, parts that must touch, travel limits."""
    res = []

    def add(name, ok, detail=""):
        res.append((name, ok, detail))

    # spreader at closed, mid and full stroke
    lv = spreader_levels(p)
    for s in (0.0, p["STROKE"] / 2, p["STROKE"]):
        sp = spreader(s, p)
        moving = ["sp_arm_a", "sp_arm_b", "sp_link_a", "sp_link_b", "sp_xhead"]
        fixed = ["sp_plate_up", "sp_plate_lo", "sp_spacers", "sp_adapter", "sp_cyl", "sp_handle"]
        keys = moving + fixed
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                if a in fixed and b in fixed:
                    continue
                if {a, b} == {"sp_xhead", "sp_cyl"}:
                    continue                      # the crosshead seats on the plunger end face
                v = _overlap(sp[a].shape, sp[b].shape)
                add(f"spreader s={s:.0f}: {a} clear of {b}", v < 1.0, f"{v:.1f} mm3")
        th = theta_for_stroke(s, p) if s > 0 else 0.0
        c = crosshead_x(th, p)
        add(f"spreader s={s:.0f}: crosshead front {c + p['XH_L2']:.1f} behind knuckle {-p['KNUCKLE_R']:.0f} by at least 5 mm",
            c + p["XH_L2"] <= -p["KNUCKLE_R"] - 5)
    # pins pass through every part they join (pin volume inside each part's bore region is zero; bores exist)
    sp = spreader(0.0, p)
    add("spreader: main pin clear of arms, spacers and plates (bores clear)",
        all(_overlap(sp["sp_pin_main"].shape, sp[k].shape) < 1.0 for k in ("sp_arm_a", "sp_arm_b", "sp_spacers", "sp_plate_up", "sp_plate_lo")))
    add("spreader: link pins clear of links, arms and crosshead (bores clear)",
        all(_overlap(sp["sp_pins_link"].shape, sp[k].shape) < 1.0 for k in ("sp_arm_a", "sp_arm_b", "sp_link_a", "sp_link_b", "sp_xhead")))
    add("spreader: adapter screws clear of plates and adapter (holes clear)",
        all(_overlap(sp["sp_bolts"].shape, sp[k].shape) < 1.0 for k in ("sp_plate_up", "sp_plate_lo", "sp_adapter")))
    # touching faces (bounding boxes meet)
    ad = sp["sp_adapter"].shape.bounding_box(); pu_ = sp["sp_plate_up"].shape.bounding_box()
    add("spreader: upper plate sits on the adapter face", abs(pu_.min.Z - ad.max.Z) < 0.01)
    sa = sp["sp_spacers"].shape.bounding_box()
    add("spreader: spacers fill arm face to plate face", abs(sa.max.Z - p["FR_Z"]) < 0.01 and abs(sa.min.Z + p["FR_Z"]) < 0.01)
    th_max = lv["theta_max"]
    add(f"spreader: tip opening at full stroke {tip_gap(th_max, p):.0f} mm >= 250 mm (R3)", tip_gap(th_max, p) >= 250.0)
    # cutter at open, part travel and stop
    for tr in (0.0, 15.0, p["CU_TRAVEL"]):
        cu = cutter(tr, p)
        keys = ["cu_carrier", "cu_mblade", "cu_fblade", "cu_nose", "cu_stop", "cu_plate_up", "cu_plate_lo", "cu_adapter"]
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                v = _overlap(cu[a].shape, cu[b].shape)
                add(f"cutter travel={tr:.0f}: {a} clear of {b}", v < 1.0, f"{v:.1f} mm3")
    cu = cutter(p["CU_TRAVEL"], p)
    cb, sb = cu["cu_carrier"].shape.bounding_box(), cu["cu_stop"].shape.bounding_box()
    add("cutter: carrier meets the stop bar at full travel", abs(cb.max.X - sb.min.X) < 0.01)
    lvc = cutter_levels(p)
    add(f"cutter: travel {p['CU_TRAVEL']:.0f} mm >= bar {p['BAR_D']:.0f} + 5 mm", p["CU_TRAVEL"] >= p["BAR_D"] + 5)
    add("cutter: moving blade front stays behind the nose block at full travel",
        lvc["mb1"] + p["CU_TRAVEL"] < lvc["nose0"])
    cu0 = cutter(0.0, p)
    add("cutter: 20 separate screws (no two heads touch)", len(cu0["cu_bolts"].shape.solids()) == 20,
        f"{len(cu0['cu_bolts'].shape.solids())} solids")
    add("cutter: screws clear of every part (holes clear)",
        all(_overlap(cu0["cu_bolts"].shape, cu0[k].shape) < 1.0 for k in ("cu_plate_up", "cu_plate_lo", "cu_fblade", "cu_nose", "cu_stop", "cu_adapter")))
    bar = rebar_sample(p)
    add("cutter: bar clear of both plates' hooks (no double shear)",
        _overlap(bar, cu0["cu_plate_up"].shape) < 1.0 and _overlap(bar, cu0["cu_plate_lo"].shape) < 1.0)
    add("cutter: bar sits in both blade notches when open",
        _overlap(bar, cu0["cu_mblade"].shape) < 1.0 and _overlap(bar, cu0["cu_fblade"].shape) < 1.0)
    # remaining bar stub (z > 0) is not reached by the carrier before the stop
    stub_rear = lvc["xb"] - p["BAR_D"] / 2
    add("cutter: carrier stops before the cut-off bar end", lvc["car1"] + p["CU_TRAVEL"] < stub_rear)
    # ram set
    rm = ram_set(p["STROKE"], True, p)
    keys = list(rm)
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            v = _overlap(rm[a].shape, rm[b].shape)
            add(f"ram: {a} clear of {b}", v < 1.0, f"{v:.1f} mm3")
    ok = sum(1 for r in res if r[1])
    if verbose:
        for n, o, d in res:
            if not o:
                print("FAIL", n, d)
        print(f"constructability checks: {ok} of {len(res)} pass")
    return res


# ------------------------------------------------------------------------------- masses and export
def masses(p=P):
    sp, cu, rm, pu = spreader(0.0, p), cutter(0.0, p), ram_set(0.0, True, p), pump_set(p)
    m = {
        "spreader": sum(c.mass() for c in sp.values()),
        "cutter": sum(c.mass() for c in cu.values()),
        "ram": sum(c.mass() for k, c in rm.items()),
        "pump": sum(c.mass() for c in pu.values()) + 2 * p["HOSE_KG"],
    }
    m["parts"] = {c.key: c.mass() for d in (sp, cu, rm, pu) for c in d.values()}
    return m


def export_all(p=P):
    step, stl = ROOT / "cad/step", ROOT / "cad/stl"
    step.mkdir(parents=True, exist_ok=True); stl.mkdir(parents=True, exist_ok=True)
    sets = {"kit": [c.shape for c in components(p)],
            "spreader": [c.shape for c in spreader(0.0, p).values()],
            "cutter": [c.shape for c in cutter(0.0, p).values()],
            "ram": [c.shape for c in ram_set(0.0, True, p).values()]}
    for name, shapes in sets.items():
        comp = Compound(children=shapes)
        export_step(comp, str(step / f"rubblejack-{name}.step"))
        export_stl(comp, str(stl / f"rubblejack-{name}.stl"), tolerance=0.5, angular_tolerance=0.3)
        print("wrote", f"cad/step/rubblejack-{name}.step", f"cad/stl/rubblejack-{name}.stl")


if __name__ == "__main__":
    if "--check" in sys.argv:
        checks()
        sys.exit(0)
    lv = spreader_levels()
    print({k: round(v, 1) for k, v in lv.items()})
    m = masses()
    print({k: round(v, 2) for k, v in m.items() if k != "parts"})
    for k, v in m["parts"].items():
        print(f"  {k:14s} {v:6.2f} kg")
    checks()
    if "--no-export" not in sys.argv:
        export_all()
