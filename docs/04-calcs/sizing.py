"""RubbleJack sizing calculations, RBJ-CAL-001 v0.1 (TRL 3, constructable design RBJ-DDR-002).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md (tags in brackets, for example [B3])
and writes docs/04-calcs/results.csv. PARAMS, the spreader kinematics and the part masses come
from cad/src/model.py, so the numbers here follow the geometry in the STEP files and in drawing
RBJ-DWG-001. Costs come from bom/bom.csv and the value-engineering target from project.yaml.
First-principles paper estimates at the pump's 700 bar relief pressure; nothing here is measured.
CONCEPT, NOT FOR FABRICATION.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
from model import (PARAMS as P, crosshead_x, cutter_levels, jaw_depth, masses, spreader_levels,  # noqa: E402
                   tail_pin, theta_for_stroke, tip_gap)

rows = []


def out(tag, text):
    print(f"[{tag}] {text}")


def res(rid, value, target, status):
    rows.append((rid, value, target, status))


# =============================================================== assumptions
P_BAR = P["P_RELIEF"]               # pump relief, the highest pressure any part can see (bar)
AREA = P["CYL_AREA_CM2"] * 100.0    # mm2
F = AREA * P_BAR * 0.1              # N (1 bar = 0.1 N/mm2)
# Yield strengths (MPa), minimum catalogue values for the stated thickness
FY = {"4340 QT 300 HB": 850.0, "S690QL": 690.0, "7075-T6 thick plate": 430.0, "7075-T6 10 mm plate": 500.0,
"S355": 345.0, "12.9 screw (shear yield)": 0.58 * 1100.0}
SF_MIN = 1.5                        # R11: every made load-bearing part at least 1.5 on yield at 700 bar
REBAR_RM = 650.0                    # MPa, upper tensile strength of B500B and ASTM A615 grade 60 bar
SHEAR_RATIO = 0.8                   # ultimate shear over tensile strength for ductile steel bar
M16_AS, M16_A3 = 157.0, 144.0       # mm2: tensile stress area, minor (root) area
BAG_KG = 0.8                        # carry bag, each (BOM line 23)
STROKE_RATE = 25.0                  # pump strokes a minute a tired person keeps up (estimate)
PUMP_SWITCH_BAR = 14.0              # the two-speed pump changes to its slow stage at about this pressure (estimate)
ETA_PUMP, ETA_CYL, ETA_LINK = 0.85, 0.95, 0.92   # flow-diagram efficiencies (estimates)

sf_rows = []


def margin(part, stress, mat):
    sf = FY[mat] / stress
    sf_rows.append((part, stress, mat, sf))
    return sf


# =============================================================== A. hydraulics
out("A1", f"Cylinder force at {P_BAR:.0f} bar on {AREA:.0f} mm2: {F / 1000:.1f} kN ({F / 9806.65:.1f} t)")
out("A2", f"Oil per full stroke: {AREA * P['STROKE'] / 1000:.0f} cm3; pump usable oil {P['PUMP_OIL']:.0f} cm3")

# =============================================================== B. spreader kinematics and force
lv = spreader_levels(P)
th_max = lv["theta_max"]


def tip_force(s):
    th = theta_for_stroke(s, P) if s > 0 else 0.0
    d = 0.01
    ds = (crosshead_x(th + d, P) - crosshead_x(th, P)) / math.radians(d)
    return th, F * ds / (2 * P["JAW_L"]), ds


table_b = []
for s in (0, 25, 50, 75, P["STROKE"]):
    th, ft, ds = tip_force(s)
    table_b.append((s, th, tip_gap(th, P), ft))
    out("B1", f"stroke {s:5.1f} mm: jaw turn {th:5.1f} deg, tip opening {tip_gap(th, P):5.0f} mm, spreading force at the tips {ft / 1000:5.1f} kN")
ft_min = min(r[3] for r in table_b)
ft_max = max(r[3] for r in table_b)
gap0, gapmax = tip_gap(0.0, P), tip_gap(th_max, P)
out("B2", f"Closed tip thickness {gap0:.0f} mm; full opening {gapmax:.0f} mm at {th_max:.1f} deg; tip force {ft_min / 1000:.1f} to {ft_max / 1000:.1f} kN")
res("R2", f"{ft_min / 1000:.1f} kN (closed) to {ft_max / 1000:.1f} kN (open) at the tips at 700 bar", "40 kN or more at the tips", "Met on paper")
res("R3", f"{gapmax:.0f} mm tip opening at full stroke; tips {gap0:.0f} mm thick closed", "250 mm or more", "Met on paper")

# link force at the worst case (largest link angle)
worst = None
for s in [k * P["STROKE"] / 20 for k in range(21)]:
    th = theta_for_stroke(s, P) if s > 0 else 0.0
    tx, ty = tail_pin(th, P)
    cx = crosshead_x(th, P)
    ang = math.atan2(ty + P["XH_E"], tx - cx)
    fl = (F / 2) / math.cos(ang)
    if worst is None or fl > worst[0]:
        worst = (fl, math.degrees(ang), s)
FL = worst[0]
out("B3", f"Largest link force {FL / 1000:.1f} kN at {worst[1]:.1f} deg to the cylinder axis ({worst[2]:.0f} mm stroke)")

# =============================================================== C. spreader strength
# C1 jaw arm bending at three stations, worst tip force, pockets included
T = P["ARM_T"]
for x in (60.0, 100.0, 150.0):
    d = jaw_depth(x, P)
    I = T * d ** 3 / 12
    if P["POCKET_X"][0] <= x <= P["POCKET_X"][1]:
        h = d - 2 * P["POCKET_INSET"]
        I -= 2 * P["POCKET_D"] * h ** 3 / 12
    sig = ft_max * (P["JAW_L"] - x) / (I / (d / 2))
    sf = margin(f"Jaw arm, {x:.0f} mm from the pivot", sig, "4340 QT 300 HB")
    out("C1", f"Jaw arm at {x:.0f} mm: depth {d:.1f} mm, bending {sig:.0f} MPa, margin {sf:.2f}")
M_root = ft_max * P["JAW_L"]
# C2 tail through the link slot (two cheeks either side of the 16.5 mm slot), at the slot start
r = P["SLOT_R0"]
hw = P["TAIL_W2_ROOT"] + (P["TAIL_EYE_R"] - P["TAIL_W2_ROOT"]) * (r - 63.0) / (P["TAIL_A"] - 63.0)
cheek = (T - 2 * P["SLOT_T2"]) / 2
Zt = 2 * cheek * (2 * hw) ** 2 / 6
sig = M_root * (P["TAIL_A"] - r) / P["TAIL_A"] / Zt
sf = margin("Jaw arm tail at the link slot", sig, "4340 QT 300 HB")
out("C2", f"Tail at the slot start: two cheeks {cheek:.2f} mm by {2 * hw:.0f} mm, bending {sig:.0f} MPa, margin {sf:.2f}")
# C3 knuckle: the arm's moment passes the pivot through the knuckle (18 mm total thickness)
R = P["KNUCKLE_R"]
kt = 2 * P["KNUCKLE_T2"]
Ik = kt * ((2 * R) ** 3 - (P["PIN_MAIN"] + P["PIN_CLR"]) ** 3) / 12
sig = M_root / (Ik / R)
sf = margin("Jaw arm knuckle round the pivot", sig, "4340 QT 300 HB")
out("C3", f"Knuckle ({kt:.0f} mm total) carries {M_root / 1e6:.1f} kN m: {sig:.0f} MPa, margin {sf:.2f}")
# C4 pivot pin: the plunger force comes back through the pin into the plates; simply supported between plate mid-planes
span = 2 * (P["FR_Z"] + P["FR_T"] / 2)
d_o, d_i = P["PIN_MAIN"], P["PIN_MAIN_BORE"]
Zp = math.pi * (d_o ** 4 - d_i ** 4) / (32 * d_o)
sig = F * span / 4 / Zp
sf = margin("Main pivot pin, bending", sig, "4340 QT 300 HB")
out("C4", f"Pivot pin {d_o:.0f} mm (bore {d_i:.0f}), span {span:.0f} mm, bending {sig:.0f} MPa (central point load, conservative), margin {sf:.2f}")
brg_a = (F / 2 + ft_max) / (d_o * kt)
out("C4b", f"Bearing of one arm's knuckle on the pin (half the plunger force plus the tip force): {brg_a:.0f} MPa")
# C5 link pins in double shear and links in compression
A_pin = math.pi * P["PIN_LINK"] ** 2 / 4
tau = FL / (2 * A_pin)
M_lp = FL * (P["LINK_T"] + cheek) / 4
sig_lp = M_lp / (math.pi * P["PIN_LINK"] ** 3 / 32)
sf = margin("Link pins, bending", sig_lp, "4340 QT 300 HB")
out("C5", f"Link pins {P['PIN_LINK']:.0f} mm: double shear {tau:.0f} MPa, bending {sig_lp:.0f} MPa, margin {sf:.2f}")
eye_net = (2 * P["LINK_EYE"] - (P["PIN_LINK"] + P["PIN_CLR"])) * P["LINK_T"]
sig = FL / eye_net
sf = margin("Link, net section at the eye", sig, "S690QL")
I_out = (2 * P["LINK_W2"]) * P["LINK_T"] ** 3 / 12
P_cr = math.pi ** 2 * 210000 * I_out / P["LINK_L"] ** 2
out("C5b", f"Link eye net section {eye_net:.0f} mm2: {sig:.0f} MPa, margin {sf:.2f}; Euler buckling out of plane {P_cr / 1000:.0f} kN against {FL / 1000:.0f} kN")
brg_xh = FL / (P["PIN_LINK"] * (2 * P["XH_T2"] - 2 * P["SLOT_T2"]))
out("C5c", f"Crosshead (7075) bearing on the link pins: {brg_xh:.0f} MPa")
# C6 frame plates: each carries half the plunger force back to the collar adapter, in tension
net_window = (2 * P["FR_W2_FRONT"] - 30.0) * P["FR_T"]
sig = F / 2 / net_window
sf = margin("Spreader frame plate, net section at the window", sig, "7075-T6 10 mm plate")
out("C6", f"Frame plate {P['FR_T']:.0f} mm, net section at the window {net_window:.0f} mm2: {sig:.0f} MPa, margin {sf:.2f}")
net_boss = (2 * P["FR_BOSS"] - (P["PIN_MAIN"] + P["PIN_CLR"])) * P["FR_T"]
sig = 2.5 * F / 2 / net_boss
sf = margin("Spreader frame plate at the pivot bore (stress concentration 2.5)", sig, "7075-T6 10 mm plate")
brg_pl = F / 2 / (P["PIN_MAIN"] * P["FR_T"])
out("C6b", f"Plate at the pivot bore: net {net_boss:.0f} mm2, peak {sig:.0f} MPa with a factor of 2.5, margin {sf:.2f}; pin bearing {brg_pl:.0f} MPa")
# C7 adapter screws: four M16 per plate in shear, collar thread in the 7075 adapter
v = F / 2 / 4
tau = v / M16_A3
sf = margin("Adapter screws M16 12.9, shear on the root area", tau, "12.9 screw (shear yield)")
out("C7", f"Adapter screws: {v / 1000:.1f} kN each, {tau:.0f} MPa on the root area, margin {sf:.2f}; bearing in the 10 mm plate {v / (16 * P['FR_T']):.0f} MPa")
thr = 0.5 * math.pi * P["COLLAR_OD"] * P["COLLAR_L"]
out("C7b", f"Collar thread in the adapter: about {thr:.0f} mm2 of thread shear area, {F / thr:.0f} MPa")

# =============================================================== D. cutter
A_bar = math.pi * P["BAR_D"] ** 2 / 4
F_cut = A_bar * SHEAR_RATIO * REBAR_RM
out("D1", f"Cutting a {P['BAR_D']:.0f} mm bar in single shear: {A_bar:.0f} mm2 x {SHEAR_RATIO * REBAR_RM:.0f} MPa = {F_cut / 1000:.0f} kN; cylinder gives {F / 1000:.0f} kN, ratio {F / F_cut:.2f}")
d_max = math.sqrt(F / (SHEAR_RATIO * REBAR_RM) * 4 / math.pi)
out("D1b", f"Largest bar the cylinder can shear at the upper strength: {d_max:.1f} mm")
p_cut = F_cut / AREA * 10
res("R4", f"16 mm bar needs about {F_cut / 1000:.0f} kN ({p_cut:.0f} bar); cylinder gives {F / 1000:.0f} kN, ratio {F / F_cut:.2f}", "Cut 16 mm reinforcing bar", "Met on paper")
for name, n in (("Stop bar", 4), ("Nose block", 4)):
    v = F / n
    tau = v / M16_A3
    sf = margin(f"{name} screws, four M16 12.9, root area", tau, "12.9 screw (shear yield)")
    out("D2", f"{name}: whole cylinder force on {n} M16 screws, {v / 1000:.1f} kN each, {tau:.0f} MPa, margin {sf:.2f}")
tau_old = F / 2 / M16_A3
out("D2b", f"With one screw per plate (the earlier stop bar) each screw would see {tau_old:.0f} MPa, margin {FY['12.9 screw (shear yield)'] / tau_old:.2f}")
lvc = cutter_levels(P)
net_c = ((P["CU_PL_Y"][1] - P["CU_PL_Y"][0]) - 2 * P["CU_HOOK2"]) * P["CU_PL_T"]
sig = F / 2 / net_c
sf = margin("Cutter plate, net section at the hook", sig, "S690QL")
out("D3", f"Cutter plate {P['CU_PL_T']:.0f} mm, net section at the hook {net_c:.0f} mm2: {sig:.0f} MPa, margin {sf:.2f}")
contact = (P["CU_STOP_Y"][1] - P["CU_CAR_Y"][0]) * (2 * P["FR_Z"] - 1.0)
out("D4", f"Carrier (7075) bearing on the stop bar: {contact:.0f} mm2, {F / contact:.0f} MPa")
v_carry = AREA * (P["BAR_D"] + 2) / 1000
out("D5", f"Oil to close the cut under load: about {v_carry:.0f} cm3, {v_carry / P['PUMP_STAGE2']:.0f} slow-stage strokes, {v_carry / P['PUMP_STAGE2'] / STROKE_RATE:.1f} min a cut")

# =============================================================== E. lifting ram
res("R1", f"{F / 9806.65:.1f} t at 700 bar (cylinder rated 15 t)", "10 t or more", "Met on paper (proof load is TRL 4)")
tod, tw, tl = P["RISER"]
A_r = math.pi / 4 * (tod ** 2 - (tod - 2 * tw) ** 2)
sig = F / A_r
sf = margin("Riser tube, direct compression", sig, "S355")
out("E1", f"Riser tube {tod} x {tw:.0f}: {A_r:.0f} mm2, {sig:.0f} MPa, margin {sf:.2f}; tube wall {tod / 2 - tw:.1f} to {tod / 2:.1f} mm from the axis, ring {P['RING'][0] / 2:.0f} to {P['RING'][1] / 2:.0f} mm")
s_bp = P["BP_S"]
a_eq = math.sqrt(s_bp ** 2 / math.pi)
r0 = P["CYL_OD"] / 2
nu = 0.3
Mbp = F / (4 * math.pi) * ((1 + nu) * math.log(a_eq / r0)) + F * (1 - nu) / (16 * math.pi) * (1 - r0 ** 2 / a_eq ** 2)
for t_, mat in ((12.0, "S355"), (P["BP_T"], "S690QL")):
    sig = 6 * Mbp / t_ ** 2
    out("E2", f"Base plate {t_:.0f} mm {mat}: free circular plate radius {a_eq:.0f} mm on an even reaction, load on {r0:.0f} mm radius: {sig:.0f} MPa, margin {FY[mat] / sig:.2f}")
sf = margin("Ram base plate, 20 mm", 6 * Mbp / P["BP_T"] ** 2, "S690QL")
q = F / s_bp ** 2
out("E3", f"Bearing under the base plate: {q:.2f} MPa; on three 100 mm hardwood sleepers 600 mm long: {F / (3 * 100 * 600):.2f} MPa")
reach = P["CYL_L"] + P["STROKE"] + P["SADDLE"][1] + P["BP_T"]
out("E4", f"Ram reach: closed {P['CYL_L'] + P['SADDLE'][1] + P['BP_T']:.0f} mm, open {reach:.0f} mm; with the riser {reach + 2 * P['RISER_PL'][1] + tl:.0f} mm")

# =============================================================== F. pump
v_full = AREA * P["STROKE"] / 1000
n2 = v_full / P["PUMP_STAGE2"]
n1 = v_full / P["PUMP_STAGE1"]
out("F1", f"Full stroke under load: {n2:.0f} slow-stage strokes, {n2 / STROKE_RATE:.1f} min; with no load {n1:.0f} fast-stage strokes, {n1 / STROKE_RATE:.1f} min")
out("F2", f"Handle effort at 700 bar {P['PUMP_EFFORT']:.0f} N on a {P['PUMP_HANDLE']:.0f} mm handle (catalogue)")
out("F3", f"Oil: three cylinders hold {3 * v_full:.0f} cm3 at full stroke against {P['PUMP_OIL']:.0f} cm3 usable; only one tool is connected at a time")
W_h = P_BAR * 0.1 * v_full                       # J (N/mm2 x cm3 = J)
flow = [round(W_h / ETA_PUMP / 1000, 2), round(W_h / 1000, 2), round(W_h * ETA_CYL / 1000, 2), round(W_h * ETA_CYL * ETA_LINK / 1000, 2)]
out("F4", f"Energy for one full spreader stroke at 700 bar (estimate): handle {flow[0]} kJ, oil {flow[1]} kJ, plunger {flow[2]} kJ, jaw tips {flow[3]} kJ")

# =============================================================== G. masses and loads
m = masses(P)
loads = {"Pump, gauge and hoses": m["pump"] + BAG_KG, "Spreader": m["spreader"] + BAG_KG,
         "Cutter": m["cutter"] + BAG_KG, "Lifting ram set": m["ram"] + BAG_KG}
for k, v in loads.items():
    out("G1", f"{k}: {v:.1f} kg packed (bag {BAG_KG} kg included)")
heaviest = max(loads.items(), key=lambda kv: kv[1])
res("R6", "; ".join(f"{k} {v:.1f} kg" for k, v in loads.items()), "No single load over 25 kg",
    f"Met on paper (heaviest, the {heaviest[0].lower()}, {25 - heaviest[1]:.1f} kg under)")
out("G2", f"Whole kit {sum(loads.values()):.1f} kg in four loads")

# =============================================================== H. cost
bom = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
cost = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom)
target = None
for line in (ROOT / "project.yaml").read_text().splitlines():
    if line.startswith("budget_usd:"):
        target = float(line.split(":")[1].split("#")[0])
made_cost = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom if r["make_buy"] == "make")
out("H1", f"Value-engineering target: USD {target:,.0f}. Estimated cost of the constructable design: USD {cost:,.0f} (USD {cost - target:,.0f} over the target); made parts USD {made_cost:,.0f}, bought USD {cost - made_cost:,.0f}")
res("R10", f"Estimated USD {cost:,.0f} from the BOM", f"Value-engineering target USD {target:,.0f}", f"Over the value-engineering target by USD {cost - target:,.0f}")

# =============================================================== remaining requirements
res("R5", "Pump relief 700 bar; cylinders, couplers, hoses and gauge adapter rated 700 bar; hoses 4 to 1 burst (2,800 bar); gauge reads to 1,000 bar",
    "Every pressurised part at or above relief; hoses 4 to 1", "Met by specification (ratings to confirm when parts are bought)")
res("R7", "Pump, one hose and one tool: two coupler connections, no tools needed; estimated 1 to 2 min from the bags", "Working within 3 min", "Met on paper (timed drill is TRL 4)")
res("R8", "Each tool has its own cylinder; a change is one coupler off and one on, about 20 s (estimate)", "Under 1 min", "Met by design")
res("R9", "Pump, gauge, hoses, couplers, cylinders and saddle are catalogue parts in a class at least two makers offer", "Standard parts from two suppliers", "Met by specification")
worst_sf = min(sf_rows, key=lambda r: r[3])
res("R11", f"Lowest margin {worst_sf[3]:.2f}: {worst_sf[0].lower()}", f"{SF_MIN} or more on yield at 700 bar for every made load-bearing part",
    "Met on paper" if worst_sf[3] >= SF_MIN else "Not met")
res("R12", "Ram base plate 250 x 250 mm; sleeper bearing about 0.8 MPa on three hardwood sleepers; procedure: crib as the load rises",
    "Never lift on bare rubble; base plate on cribbing", "Met by design and procedure")

print()
print("Margins on yield at 700 bar (R11):")
for part, stress, mat, sf in sorted(sf_rows, key=lambda r: r[3]):
    print(f"  {part:62s} {stress:6.0f} MPa  {mat:28s} {sf:6.3f}")

order = ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12"]
rows.sort(key=lambda r: order.index(r[0]))
with (ROOT / "docs/04-calcs/results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "value", "target", "status"])
    w.writerows(rows)
print()
for r in rows:
    print(" | ".join(r))
