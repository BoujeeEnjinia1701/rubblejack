"""RubbleJack prototype build plan pictures (RBJ-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py, so the
pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/RBJ-DWG-101 to 118        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
A sheet or step can be drawn alone: "sheets:105" or "steps:7".
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build123d as b  # noqa: E402
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from sheets import patch_kit_views  # noqa: E402
from model import (PARAMS as P, arm, components, crosshead, cutter, cutter_levels, frame_plate, link, pin, pump_set,  # noqa: E402
                   ram_set, spreader, spreader_levels, tail_pin, zcyl, hose_coil)

patch_kit_views()
OUT = ROOT / "docs" / "05-build-plan"
DATE = "2026-10-03"
SP, CU, RM, PU = spreader(0.0), cutter(0.0), ram_set(0.0, True), pump_set()
LV, LC = spreader_levels(), cutter_levels()

COL = {"cyl": "#1D4ED8", "adapter": "#94A3B8", "plate": "#7FA7D1", "xhead": "#64748B", "link": "#0E7490",
       "arm_a": "#D4A017", "arm_b": "#B45309", "spacer": "#A8A29E", "pin": "#57534E", "handle": "#B91C1C",
       "screw": "#111827", "carrier": "#94A3B8", "blade": "#C2410C", "nose": "#78716C", "stop": "#4B5563",
       "cplate": "#0F766E", "base": "#4B5563", "riser": "#6B7280", "saddle": "#374151", "pump": "#C2410C",
       "gauge": "#111827", "hose": "#1F2937", "bar": "#9CA3AF"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def win(shape, x0, x1, y0, y1, z0, z1):
    return shape & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0))


def sp(key, name=None, color=None, e=(0, 0, 0)):
    c = SP[key]
    return part(name or c.name, c.shape, color or COL.get(key.split("_", 1)[1], "#9CA3AF"), e)


def cu(key, name=None, color=None, e=(0, 0, 0)):
    c = CU[key]
    return part(name or c.name, c.shape, color or "#9CA3AF", e)


def split(shape):
    return list(shape.solids())


def comp(solids):
    return b.Compound(children=list(solids))


# ----------------------------------------------------------------- overview
def overview():
    order = ["sp_adapter", "sp_plate_up", "sp_plate_lo", "sp_xhead", "sp_link_a", "sp_link_b", "sp_arm_a", "sp_arm_b",
             "sp_spacers", "sp_pin_main", "sp_pins_link", "sp_handle", "cu_adapter", "cu_carrier", "cu_mblade", "cu_fblade",
             "cu_nose", "cu_stop", "cu_plate_up", "cu_plate_lo", "cu_handle", "rm_base", "rm_riser",
             "sp_cyl", "cu_cyl", "rm_cyl", "rm_saddle", "sp_bolts", "cu_bolts", "cu_mbolts", "pu_pump", "pu_gauge", "hoses"]
    names = {"sp_adapter": "Spreader collar adapter", "sp_plate_up": "Spreader frame plate, upper",
             "sp_plate_lo": "Spreader frame plate, lower", "sp_xhead": "Crosshead", "sp_link_a": "Link to arm A",
             "sp_link_b": "Link to arm B", "sp_arm_a": "Jaw arm A (centre knuckle)", "sp_arm_b": "Jaw arm B (twin knuckles)",
             "sp_spacers": "Pivot spacers (2)", "sp_pin_main": "Main pivot pin", "sp_pins_link": "Link pins (4)",
             "sp_handle": "Spreader carry handle", "cu_adapter": "Cutter collar adapter", "cu_carrier": "Blade carrier",
             "cu_mblade": "Moving blade", "cu_fblade": "Fixed blade", "cu_nose": "Nose block", "cu_stop": "Stop bar",
             "cu_plate_up": "Cutter plate, upper", "cu_plate_lo": "Cutter plate, lower", "cu_handle": "Cutter carry handle",
             "rm_base": "Ram base plate", "rm_riser": "Riser block", "sp_cyl": "Cylinder, spreader (bought)",
             "cu_cyl": "Cylinder, cutter (bought)", "rm_cyl": "Cylinder, lifting ram (bought)", "rm_saddle": "Tilting saddle (bought)",
             "sp_bolts": "Spreader screws (bought)", "cu_bolts": "Cutter screws (bought)", "cu_mbolts": "Moving blade screws (bought)",
             "pu_pump": "Hand pump (bought)", "pu_gauge": "Gauge and adapter (bought)", "hoses": "Hoses with couplers (bought)"}
    colors = {"sp_adapter": COL["adapter"], "sp_plate_up": COL["plate"], "sp_plate_lo": COL["plate"], "sp_xhead": COL["xhead"],
              "sp_link_a": COL["link"], "sp_link_b": COL["link"], "sp_arm_a": COL["arm_a"], "sp_arm_b": COL["arm_b"],
              "sp_spacers": COL["spacer"], "sp_pin_main": COL["pin"], "sp_pins_link": COL["pin"], "sp_handle": COL["handle"],
              "cu_adapter": COL["adapter"], "cu_carrier": COL["carrier"], "cu_mblade": COL["blade"], "cu_fblade": COL["blade"],
              "cu_nose": COL["nose"], "cu_stop": COL["stop"], "cu_plate_up": COL["cplate"], "cu_plate_lo": COL["cplate"],
              "cu_handle": COL["handle"], "rm_base": COL["base"], "rm_riser": COL["riser"], "sp_cyl": COL["cyl"],
              "cu_cyl": COL["cyl"], "rm_cyl": COL["cyl"], "rm_saddle": COL["saddle"], "sp_bolts": COL["screw"],
              "cu_bolts": COL["screw"], "cu_mbolts": COL["screw"], "pu_pump": COL["pump"], "pu_gauge": COL["gauge"],
              "hoses": COL["hose"]}
    # each tool in its own frame, set well apart so the pulled-apart parts of one tool never mix with another's
    allc = {}
    for d, at in ((SP, (0, 0, 0)), (CU, (-150, 1300, 0)), (RM, (1000, 1300, 0)), (PU, (-650, -1100, 0))):
        for k, c in d.items():
            allc[k] = (b.Pos(*at) * c.shape, c.explode)
    allc["hoses"] = (hose_coil(500, -1100), (0, 0, 0))
    parts = []
    for k in order:
        shape, ex = allc[k]
        e = tuple(1.6 * v for v in ex)
        parts.append(part(names[k], shape, colors[k], e))
    return bv.overview(parts, OUT / "overview.png", "RubbleJack prototype kit: every component, pulled apart",
                       subtitle="Numbered in build order: spreader 1 to 12, cutter 13 to 21, ram 22 to 23, then the bought parts",
                       elev=38, azim=-62, size=(12, 8.5), dpi=150, key=True)


def link_flat():
    """The link laid along X, for its three views."""
    t2, r = P["LINK_T"] / 2, P["LINK_EYE"]
    L = P["LINK_L"]
    s = (b.Pos(L / 2, 0, 0) * b.Box(L, 2 * P["LINK_W2"], P["LINK_T"])) + zcyl(r, -t2, t2) + zcyl(r, -t2, t2, x=L)
    for x in (0.0, L):
        s -= zcyl((P["PIN_LINK"] + P["PIN_CLR"]) / 2, -t2 - 1, t2 + 1, x=x)
    return s


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    out = []
    base = dict(project="RubbleJack", date=DATE)
    x_back = LV["x_ad0"]
    tx, ty = tail_pin(0.0)

    def sheet(no, prt, neighbours, title, material, notes, **kw):
        if only and no not in only:
            return
        out.append(bv.component_sheet(prt, neighbours, dwg_no=f"RBJ-DWG-{no}", title=f"RubbleJack {title}: making sketch",
                                      material=material, notes=notes, **base, **kw))

    plate_lo = sp("sp_plate_lo", color=COL["plate"])
    cyl = sp("sp_cyl", color=COL["cyl"])
    # 101 collar adapter
    sheet(101, sp("sp_adapter", "Collar adapter", COL["adapter"]), [cyl, plate_lo, sp("sp_plate_up", color=COL["plate"])],
          "collar adapter (make 2)", "7075-T6 aluminium plate, 100 mm",
          ["Make two the same: one for the spreader, one for the cutter.",
           f"Block {P['AD_L']:.0f} long x {2 * P['AD_W2']:.0f} wide x {2 * P['FR_Z']:.0f} tall, faces square",
           "  and parallel: the two 130 x 60 faces carry the frame plates.",
           f"Bore through on the long axis: {P['CYL_OD'] + 2:.0f} mm for the cylinder body.",
           f"From the front face, cut the cylinder's collar thread ({P['COLLAR_OD']} mm,",
           f"  12 UN class) {P['COLLAR_L']:.0f} mm deep. Check the thread on the bought",
           "  cylinder first and cut to match it.",
           "Each 130 x 60 face: four M16 holes, drill 14 mm, tap 24 mm full",
           f"  thread, at 15 and 45 mm from the front face, {P['AD_BOLT_Y']:.0f} mm each side.",
           "Break every edge 1 mm.",
           "Fit: screws onto the collar until the collar end is flush with",
           "  the front face; the plates sit flat on the 130 x 60 faces.",
           "Check: plates lie flat with no rock; all eight screws start by hand."],
          inset_view=(28, -50))
    # 102 frame plate
    sheet(102, sp("sp_plate_up", "Spreader frame plate", COL["plate"]), [sp("sp_adapter", color=COL["adapter"]),
          sp("sp_arm_a", color=COL["arm_a"]), sp("sp_arm_b", color=COL["arm_b"]), cyl],
          "spreader frame plate (make 2)", "7075-T6 aluminium plate, 10 mm",
          [f"Make two from 10 mm plate (waterjet or saw and file); lengths from the back edge.",
           f"Profile: {-x_back + P['FR_BOSS']:.0f} long; {2 * P['FR_W2']:.0f} wide for the first {LV['x_col'] - x_back:.0f} mm,",
           f"  tapering to {2 * P['FR_W2_FRONT']:.0f} wide at {-90 - x_back:.0f} mm, ending in a {P['FR_BOSS']:.0f} mm radius round the pivot.",
           f"Pivot bore {P['PIN_MAIN'] + P['PIN_CLR']:.1f} mm, {-x_back:.0f} mm from the back edge, on the centre line.",
           "Four 18 mm holes for the adapter screws, 15 and 45 mm from the",
           f"  back edge, {P['AD_BOLT_Y']:.0f} mm each side of the centre line.",
           f"Window 30 mm wide from {LV['x_col'] + 20 - x_back:.0f} to {-115 - x_back:.0f} mm from the back edge.",
           f"Upper plate only: two 13.6 mm handle holes on the centre line at",
           f"  {P['HANDLE_X'][0] - x_back:.0f} and {P['HANDLE_X'][1] - x_back:.0f} mm from the back edge.",
           "Bore the two pivot holes with the plates clamped together.",
           "Deburr; round the outside corners about 3 mm.",
           "Check: a 45 mm pin goes through both pivot bores clamped together."],
          inset_view=(30, -60))
    # 103 crosshead
    xh = crosshead(LV["c0"])
    sheet(103, part("Crosshead", xh, COL["xhead"]), [cyl, sp("sp_link_a", color=COL["link"]), sp("sp_link_b", color=COL["link"])],
          "crosshead", "7075-T6 aluminium plate, 100 mm",
          [f"Block {2 * P['XH_L2']:.0f} long (along the cylinder) x {2 * P['XH_W2']:.0f} wide x {2 * P['XH_T2']:.0f} tall.",
           f"Two slots {2 * P['SLOT_T2']:.1f} wide, centred in the height, from {P['XH_WEB2']:.0f} mm",
           "  either side of the centre line out to each side face: the links",
           "  go in these. Mill or saw and file; keep the slot sides square.",
           f"Pin bores {P['PIN_LINK'] + P['PIN_CLR']:.1f} mm through the top and bottom,",
           f"  {P['XH_E']:.0f} mm each side of the centre line, at the middle of the length.",
           "Back face: tap M24 to suit the plunger stud (drill 21 mm,",
           "  25 mm deep) on the centre; the back face sits on the plunger end.",
           "Check: a link slides into each slot with 0.5 mm play in all."],
          inset_view=(30, -40))
    # 104 link
    lk = link("A", 0.0)
    sheet(104, part("Link", lk, COL["link"]), [part("Crosshead", xh, COL["xhead"]), sp("sp_arm_a", color=COL["arm_a"])],
          "link (make 2)", "S690QL steel plate, 16 mm",
          [f"Two the same, {P['LINK_T']:.0f} mm plate, laser or waterjet cut.",
           f"Bore centres {P['LINK_L']:.0f} mm apart; eyes {2 * P['LINK_EYE']:.0f} mm across round each bore;",
           f"  body {2 * P['LINK_W2']:.0f} wide between the eyes.",
           f"Bores {P['PIN_LINK'] + P['PIN_CLR']:.1f} mm, reamed; drill the two links clamped",
           "  together so the centres match.",
           "Deburr the edges; no notches or scratches across the body.",
           "Check: both links on two 25 mm pins at once, with no bind."],
          view_shape=link_flat(), inset_view=(35, -50))
    # 105 and 106 jaw arms
    for no, which, col, knuck in ((105, "A", COL["arm_a"], "A centre knuckle 18 mm thick: face 9 mm off each side within a 61 mm radius of the pivot."),
                                  (106, "B", COL["arm_b"], "B twin knuckles 9 mm thick: cut an 18 mm wide groove, centred, within a 61 mm radius of the pivot.")):
        other = "sp_arm_b" if which == "A" else "sp_arm_a"
        sheet(no, part(f"Jaw arm {which}", arm(which, 0.0), col), [sp(other, color="#9CA3AF"), plate_lo, sp("sp_pins_link")],
              f"jaw arm {which}", "4340 steel plate 40 mm, quenched and tempered to about 300 HB",
              [f"Cut the profile from 40 mm plate (waterjet), then mill both faces to {P['ARM_T']:.0f} mm.",
               f"Jaw: {P['JAW_L']:.0f} mm from the pivot to the tip; straight inner face; outer edge",
               f"  {P['JAW_DMAX']:.0f} deep near the pivot, curving to {P['TIP_H']:.0f} deep at the tip.",
               f"Tail: pin bore {P['PIN_LINK'] + P['PIN_CLR']:.1f} mm, {P['TAIL_A']:.0f} mm from the pivot, {180 - P['TAIL_PHI']:.0f} deg round",
               "  from the jaw's inner face, behind the pivot.",
               f"Link slot {2 * P['SLOT_T2']:.1f} wide, centred in the thickness, from {P['SLOT_R0']:.0f} mm out to the tail end.",
               f"Pivot bore {P['PIN_MAIN'] + P['PIN_CLR']:.1f} mm, reamed.",
               knuck,
               f"Pockets {P['POCKET_D']:.0f} deep both faces, {P['POCKET_INSET']:.0f} in from the edges, in the jaw and tail.",
               "Serrate the tip's outer face (2 mm teeth across) for grip.",
               "Make A and B as a pair; break every edge 1 mm; no tool marks",
               "  across the jaw near the pivot. Crack-check after heat treatment.",
               "Check: A's knuckle slides into B's groove; the bores line up."],
              inset_view=(40, -60))
    # 107 spacer
    spc = zcyl(P["SPACER_OD"] / 2, 0, P["FR_Z"] - P["ARM_T"] / 2) - zcyl((P["PIN_MAIN"] + P["PIN_CLR"]) / 2, -1, P["FR_Z"])
    sheet(107, part("Pivot spacer", spc, COL["spacer"]), [plate_lo, sp("sp_arm_a", color=COL["arm_a"])],
          "pivot spacer (make 2)", "7075-T6 aluminium bar or tube",
          [f"Two rings: {P['SPACER_OD']:.0f} mm outside, {P['PIN_MAIN'] + P['PIN_CLR']:.1f} mm bore,",
           f"  {P['FR_Z'] - P['ARM_T'] / 2:.0f} mm long, ends faced square and parallel.",
           "One goes above the arms and one below; they fill the gap",
           "  between the arm faces and the frame plates.",
           "Check: arms plus spacers measure 92 mm, the gap between plates."],
          inset_view=(35, -60))
    # 108 main pin
    zt = P["FR_Z"] + P["FR_T"]
    mp = pin(P["PIN_MAIN"], -zt, zt + 8) - zcyl(P["PIN_MAIN_BORE"] / 2, -zt - 7, zt + 9)
    sheet(108, part("Main pivot pin", mp, COL["pin"]), [plate_lo, sp("sp_spacers", color=COL["spacer"])],
          "main pivot pin", "4340 steel bar, quenched and tempered to about 300 HB",
          [f"Turn from bar: {P['PIN_MAIN']:.0f} mm ground, {2 * zt + 8:.0f} mm long under the head;",
           f"  head {P['PIN_MAIN'] + 12:.0f} mm across and 6 mm thick.",
           f"Bore {P['PIN_MAIN_BORE']:.0f} mm through on the axis (saves weight).",
           "Circlip groove for a 45 mm external circlip, 3 to 6 mm from the",
           "  plain end; washer under the circlip.",
           "Chamfer the plain end 2 mm so it finds the bores.",
           "Check: slides through both plates, spacers and knuckles by hand."],
          inset_view=(25, -60))
    # 109 link pins
    lp = pin(P["PIN_LINK"], -P["XH_T2"], P["XH_T2"] + 8)
    sheet(109, part("Link pin", lp, COL["pin"]), [part("Crosshead", xh, COL["xhead"]), sp("sp_link_a", color=COL["link"])],
          "link pin (make 4)", "4340 steel bar, quenched and tempered to about 300 HB",
          [f"Four pins {P['PIN_LINK']:.0f} mm ground, each with a {P['PIN_LINK'] + 12:.0f} mm head 6 mm thick.",
           f"Two for the crosshead: {2 * P['XH_T2'] + 8:.0f} mm under the head (drawn).",
           f"Two for the arm tails: {P['ARM_T'] + 8:.0f} mm under the head.",
           "Circlip groove for a 25 mm external circlip, 3 to 6 mm from",
           "  the plain end; washer under each circlip.",
           "Chamfer the plain end 1 mm.",
           "Check: each pin passes its link and bores with no force."],
          inset_view=(25, -60))
    # 110 handle
    sheet(110, sp("sp_handle", "Carry handle", COL["handle"]), [sp("sp_plate_up", color=COL["plate"])],
          "carry handle (make 2)", "Steel tube 26.9 x 3.2 mm",
          [f"Bend one tube to a D: two posts {P['HANDLE_H']:.0f} mm tall and a grip bar.",
           f"Spreader handle: posts {P['HANDLE_X'][1] - P['HANDLE_X'][0]:.0f} mm apart (drawn). Cutter: 110 mm apart.",
           "Weld an M12 threaded plug into each post foot, faced flat.",
           "Fit: M12 cap screw up through the plate's 13.6 mm hole into",
           "  each plug, with a spring washer under the head.",
           "Check: lift the finished tool by it; no movement at the feet."],
          inset_view=(35, -60))
    # cutter parts
    cpl = cu("cu_plate_lo", color=COL["cplate"])
    ccyl = cu("cu_cyl", color=COL["cyl"])
    xb = LC["xb"]
    sheet(111, cu("cu_carrier", "Blade carrier", COL["carrier"]), [ccyl, cu("cu_mblade", color=COL["blade"]), cpl],
          "blade carrier", "7075-T6 aluminium plate, 100 mm",
          [f"Block {P['CU_CAR_L']:.0f} long x {P['CU_CAR_Y'][1] - P['CU_CAR_Y'][0]:.0f} wide x {2 * P['FR_Z'] - 1:.0f} tall; it slides between the plates.",
           "Back face: tap M24 for the plunger stud (drill 21, 25 deep), on",
           f"  the cylinder axis, {-P['CU_CAR_Y'][0]:.0f} mm from the lower long edge.",
           "Two 17 mm holes through, front to back, for the blade screws:",
           f"  {P['FR_Z'] / 2:.0f} mm below the middle of the height, at 25 mm and 30 mm",
           "  either side of the axis; counterbore 25 mm, 16 deep, at the back.",
           "Check: slides between two 92 mm spaced plates with 0.5 to 1 mm play."],
          inset_view=(30, -50))
    sheet(112, cu("cu_mblade", "Moving blade", COL["blade"]), [cu("cu_carrier", color=COL["carrier"]), cu("cu_fblade", color="#9CA3AF")],
          "moving blade", "S7 shock-resisting tool steel, hardened 54 to 56 HRC",
          [f"Block 70 long x 70 wide x {P['FR_Z'] - 0.5:.1f} tall (the lower half of the shear).",
           f"U notch {P['CU_NOTCH']:.0f} wide, its round bottom centred {P['CU_MB'][1]:.0f} mm from the back face,",
           "  open to the top long edge. The notch's back wall pushes the bar.",
           "Back face: two M16 holes, 28 deep, matching the carrier's holes.",
           "Machine soft, heat treat, then grind the top face flat and the",
           "  notch edges sharp and square: this face slides past the fixed blade.",
           "Check: top face flat to 0.05 mm on a surface plate."],
          inset_view=(30, -50))
    sheet(113, cu("cu_fblade", "Fixed blade", COL["blade"]), [cu("cu_plate_up", color=COL["cplate"]), cu("cu_nose", color=COL["nose"])],
          "fixed blade", "S7 shock-resisting tool steel, hardened 54 to 56 HRC",
          [f"Block {LC['fb1'] - LC['fb0']:.1f} long x 70 wide x {P['FR_Z'] - P['CU_CLR']:.1f} tall (the upper half).",
           f"U notch {P['CU_NOTCH']:.0f} wide, its round bottom {-P['CU_FB'][0]:.1f} mm from the back face,",
           "  in line with the moving blade's notch.",
           "Top face: four M12 holes 20 deep at 30 and 50 mm in front of the",
           "  notch centre, 15 mm toward the lower edge and 25 mm toward the upper.",
           "Grind the bottom face flat and the notch edges sharp; the front",
           "  face bears on the nose block and must be square.",
           f"Fit: {P['CU_CLR']:.1f} mm above the moving blade; shim under the upper plate if needed."],
          inset_view=(30, -50))
    sheet(114, cu("cu_nose", "Nose block", COL["nose"]), [cu("cu_fblade", color=COL["blade"]), cpl],
          "nose block", "7075-T6 aluminium plate, 100 mm",
          [f"Block 30 long x 90 wide x {2 * P['FR_Z']:.0f} tall, faces square and parallel.",
           "Each 90 x 30 face: two M16 holes 26 deep, on the middle of the",
           "  30 mm length, 35 mm below and 20 mm above the cylinder axis.",
           "Its back face takes the push of the fixed blade.",
           "Check: stands square between the plates with no gap at either."],
          inset_view=(30, -50))
    sheet(115, cu("cu_stop", "Stop bar", COL["stop"]), [cu("cu_carrier", color=COL["carrier"]), cpl],
          "stop bar", "S355 steel bar",
          [f"Bar {P['CU_STOP_L']:.0f} long x {P['CU_STOP_Y'][1] - P['CU_STOP_Y'][0]:.0f} wide x {2 * P['FR_Z']:.0f} tall, ends square.",
           "Each 60 x 32 face: two M16 holes, drill 14, tap 24 deep,",
           f"  at {P['CU_STOP_BOLT_X'][0]:.0f} and {P['CU_STOP_BOLT_X'][1]:.0f} mm from the back end, on the width centre.",
           "Two screws in each plate stop the bar turning when the carrier",
           "  hits it at full pump pressure.",
           "Check: the back end is square to the faces (the carrier lands on it)."],
          inset_view=(30, -50))
    sheet(116, cu("cu_plate_up", "Cutter plate", COL["cplate"]), [cu("cu_adapter", color=COL["adapter"]), cu("cu_fblade", color=COL["blade"]),
          cu("cu_nose", color=COL["nose"]), cu("cu_stop", color=COL["stop"])],
          "cutter plate (make 2)", "S690QL steel plate, 16 mm",
          [f"Two plates {LC['nose1'] + P['AD_L']:.0f} x {P['CU_PL_Y'][1] - P['CU_PL_Y'][0]:.0f}, 16 mm, laser cut. Sizes from the back edge.",
           f"Hook {2 * P['CU_HOOK2']:.0f} wide, centred {xb + P['AD_L']:.0f} mm from the back edge; its round",
           f"  bottom {-P['CU_PL_Y'][0] - P['CU_HOOK2']:.0f} mm up from the lower edge; open to the upper edge.",
           "18 mm holes: adapter 15 and 45 from the back, 50 each side of",
           f"  the axis ({-P['CU_PL_Y'][0]:.0f} up from the lower edge); nose at {LC['nose0'] + 15 + P['AD_L']:.0f};",
           f"  stop at {LC['stop0'] + 15 + P['AD_L']:.0f} and {LC['stop0'] + 45 + P['AD_L']:.0f}, 20 up from the lower edge.",
           "Upper plate only: four 13.5 mm fixed blade holes and two 13.6 mm",
           "  handle holes (drawn); the lower plate has neither.",
           "Drill the shared holes with both plates clamped together.",
           "Check: hooks line up when the plates are stacked."],
          inset_view=(35, -55))
    sheet(117, part("Ram base plate", RM["rm_base"].shape, COL["base"]), [part("Cylinder", RM["rm_cyl"].shape, COL["cyl"])],
          "ram base plate", "S690QL steel plate, 20 mm; S355 ring",
          [f"Plate {P['BP_S']:.0f} x {P['BP_S']:.0f} x {P['BP_T']:.0f}, high-strength steel (do not swap to mild steel).",
           "Two hand slots 24 x 90, centred 30 mm in from two opposite edges.",
           f"Ring {P['RING'][1]:.0f} outside, {P['RING'][0]:.0f} inside, {P['RING'][2]:.0f} tall, on the centre.",
           "Weld the ring with a 6 mm fillet all round, low-hydrogen rods,",
           "  preheat as the plate maker's sheet says; let it cool slowly.",
           "Check: plate flat to 1 mm after welding; cylinder base drops in."],
          inset_view=(35, -55))
    sheet(118, part("Riser block", RM["rm_riser"].shape, COL["riser"]), [part("Base plate", RM["rm_base"].shape, COL["base"])],
          "riser block", "S355 tube 88.9 x 10 and 10 mm plate",
          [f"Tube {P['RISER'][0]} x {P['RISER'][1]:.0f}, {P['RISER'][2]:.0f} long, ends square.",
           f"Two end plates {P['RISER_PL'][0]:.0f} x {P['RISER_PL'][0]:.0f} x {P['RISER_PL'][1]:.0f}, tube centred, fillet welded all round.",
           f"Under the bottom plate: a {P['SPIGOT'][0]:.0f} mm spigot, {P['SPIGOT'][1]:.0f} mm tall, welded on the centre;",
           "  it locates in the base plate's ring.",
           f"On the top plate: a ring {P['RING'][1]:.0f} / {P['RING'][0]:.0f}, {P['RING'][2]:.0f} tall, like the base plate's.",
           "The tube wall sits right over the ring and under the cylinder",
           "  base, so the plates carry the load straight down.",
           "Check: the end plates are parallel to 0.5 mm; it stands without rocking."],
          inset_view=(30, -55))
    return out


# ----------------------------------------------------------------- joints
def joints():
    out = []

    def j(n, parts, title, sub, **kw):
        out.append(bv.joint(parts, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, **kw))

    xc = LV["x_col"]
    box_ = (xc - 120, xc + 25, -80, 80, -80, 80)
    j(1, [part("Cylinder collar (bought)", win(SP["sp_cyl"].shape, *box_), COL["cyl"]),
          part("Collar adapter", win(SP["sp_adapter"].shape, *box_), COL["adapter"]),
          part("Frame plates", win(SP["sp_plate_up"].shape + SP["sp_plate_lo"].shape, *box_), COL["plate"]),
          part("M16 cap screws, 4 each plate", win(SP["sp_bolts"].shape, *box_), COL["screw"])],
      "collar adapter between the frame plates", "Cut on the cylinder axis. The adapter screws onto the collar thread; the plates bolt flat to it",
      cut="+Y", elev=20, azim=-60, size=(8, 6))
    c0 = LV["c0"]
    box_ = (c0 - 60, c0 + 50, -80, 80, -30, 40)
    j(2, [part("Plunger (bought)", win(SP["sp_cyl"].shape, *box_), COL["cyl"]),
          part("Crosshead on the M24 stud", win(SP["sp_xhead"].shape, *box_), COL["xhead"]),
          part("Links", win(SP["sp_link_a"].shape + SP["sp_link_b"].shape, *box_), COL["link"]),
          part("Link pins, heads below, circlips on top", win(SP["sp_pins_link"].shape, *box_), COL["pin"])],
      "crosshead, links and pins", "Upper plate off. Each link sits in a slot in the crosshead; one pin through each",
      elev=45, azim=-70, size=(8, 6))
    tx, ty = tail_pin(0.0)
    box_ = (tx - 45, tx + 45, ty - 45, ty + 45, -30, 30)
    j(3, [part("Jaw arm A tail", win(SP["sp_arm_a"].shape, *box_), COL["arm_a"]),
          part("Link in the tail slot", win(SP["sp_link_a"].shape, *box_), COL["link"]),
          part("Link pin", win(SP["sp_pins_link"].shape, *box_), COL["pin"])],
      "link in the arm's tail", "Cut through the pin. The link sits in a 16.5 mm slot; the pin carries it in double shear",
      cut="+X", elev=25, azim=-40, size=(8, 6))
    box_ = (-70, 70, -70, 70, -80, 80)
    j(4, [part("Frame plates", win(SP["sp_plate_up"].shape + SP["sp_plate_lo"].shape, *box_), COL["plate"]),
          part("Pivot spacers", win(SP["sp_spacers"].shape, *box_), COL["spacer"]),
          part("Arm A, centre knuckle", win(SP["sp_arm_a"].shape, *box_), COL["arm_a"]),
          part("Arm B, twin knuckles", win(SP["sp_arm_b"].shape, *box_), COL["arm_b"]),
          part("Main pin, head below, circlip on top", win(SP["sp_pin_main"].shape, *box_), COL["pin"])],
      "the pivot stack", "Cut through the pin. Plate, spacer, B, A, B, spacer, plate: 92 mm between the plates",
      cut="+Y", elev=15, azim=-70, size=(8, 6))
    hx = P["HANDLE_X"]
    box_ = (hx[0] - 40, hx[1] + 40, -60, 60, 30, 150)
    j(5, [part("Upper frame plate", win(SP["sp_plate_up"].shape, *box_), COL["plate"]),
          part("Carry handle, M12 screw into each foot", win(SP["sp_handle"].shape, *box_), COL["handle"])],
      "carry handle on the upper plate", "One M12 cap screw from under the plate into the plug in each post foot",
      cut="+Y", elev=25, azim=-60, size=(8, 6))
    box_ = (-10, 140, -70, 50, -50, 10)
    j(6, [part("Plunger (bought)", win(CU["cu_cyl"].shape, *box_), COL["cyl"]),
          part("Blade carrier", win(CU["cu_carrier"].shape, *box_), COL["carrier"]),
          part("Moving blade", win(CU["cu_mblade"].shape, *box_), COL["blade"]),
          part("Two M16 screws from the back", win(CU["cu_mbolts"].shape, *box_), COL["screw"])],
      "moving blade on the carrier", "Lower half shown. Two screws from the carrier's counterbores hold the blade",
      elev=40, azim=-60, size=(8, 6))
    box_ = (85, 205, -75, 55, -70, 70)
    bar = zcyl(P["BAR_D"] / 2, -150, 150, x=LC["xb"])
    j(7, [part("Cutter plates", win(CU["cu_plate_up"].shape + CU["cu_plate_lo"].shape, *box_), COL["cplate"]),
          part("Fixed blade (upper half)", win(CU["cu_fblade"].shape, *box_), COL["blade"]),
          part("Moving blade (lower half)", win(CU["cu_mblade"].shape, *box_), COL["blade"]),
          part("Nose block", win(CU["cu_nose"].shape, *box_), COL["nose"]),
          part("16 mm bar in the hook", win(bar, *box_), COL["bar"])],
      "blades, nose block and the bar", "Cut through the hook. The bar crosses both notches; the fixed blade bears on the nose block",
      cut="+Y", elev=20, azim=-60, size=(8, 6))
    box_ = (50, 170, -80, 0, -85, 85)
    j(8, [part("Cutter plates", win(CU["cu_plate_up"].shape + CU["cu_plate_lo"].shape, *box_), COL["cplate"]),
          part("Stop bar", win(CU["cu_stop"].shape, *box_), COL["stop"]),
          part("Blade carrier at the stop", win(cutter(P["CU_TRAVEL"])["cu_carrier"].shape, *box_), COL["carrier"]),
          part("Two M16 screws in each plate", win(CU["cu_bolts"].shape, *box_), COL["screw"])],
      "stop bar between the plates", "The carrier lands on the stop bar after the cut; four screws hold it",
      elev=30, azim=-120, size=(8, 6))
    box_ = (-90, 90, -90, 90, 0, 460)
    j(9, [part("Base plate and ring", RM["rm_base"].shape, COL["base"]),
          part("Riser block", RM["rm_riser"].shape, COL["riser"]),
          part("Cylinder base (bought)", win(RM["rm_cyl"].shape, -60, 60, -60, 60, 0, 300), COL["cyl"]),
          part("Tilting saddle (bought)", RM["rm_saddle"].shape, COL["saddle"])],
      "the lifting ram stack", "Cut on the axis. Riser spigot in the base ring; cylinder base in the riser's ring; saddle on the plunger",
      cut="+Y", elev=12, azim=-60, size=(7, 7))
    return out


# ----------------------------------------------------------------- steps
def steps(only=None):
    out = []

    def st(n, done, new, title, sub, **kw):
        if only and n not in only:
            return
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    cyl = sp("sp_cyl", "Spreader cylinder", COL["cyl"])
    ad = sp("sp_adapter", "Collar adapter", COL["adapter"])
    xh = sp("sp_xhead", "Crosshead", COL["xhead"])
    links = part("Links", SP["sp_link_a"].shape + SP["sp_link_b"].shape, COL["link"])
    lp = split(SP["sp_pins_link"].shape)
    xpins = part("Crosshead pins", comp(q for q in lp if q.bounding_box().center().X < -200), COL["pin"])
    tpins = part("Tail pins", comp(q for q in lp if q.bounding_box().center().X > -200), COL["pin"])
    plo = sp("sp_plate_lo", "Lower frame plate", COL["plate"])
    pup = sp("sp_plate_up", "Upper frame plate", COL["plate"])
    bolts = split(SP["sp_bolts"].shape)
    lo_b = part("4 x M16 screws", b.Compound(children=[s for s in bolts if s.bounding_box().center().Z < 0]), COL["screw"])
    up_b = part("4 x M16 screws", b.Compound(children=[s for s in bolts if s.bounding_box().center().Z > 0]), COL["screw"])
    aa = sp("sp_arm_a", "Jaw arm A", COL["arm_a"])
    ab = sp("sp_arm_b", "Jaw arm B", COL["arm_b"])
    spc = split(SP["sp_spacers"].shape)
    s_up = part("Upper spacer", [q for q in spc if q.bounding_box().center().Z > 0][0], COL["spacer"])
    s_lo = part("Lower spacer", [q for q in spc if q.bounding_box().center().Z < 0][0], COL["spacer"])
    mpin = sp("sp_pin_main", "Main pin", COL["pin"])
    hd = sp("sp_handle", "Carry handle", COL["handle"])

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)

    st(1, [cyl], [mv(ad, (160, 0, 0))], "collar adapter onto the spreader cylinder",
       "Screw it on by hand until the collar end is flush with the adapter's front face", elev=25, azim=-50)
    st(2, [cyl, ad], [mv(xh, (120, 0, 0))], "crosshead onto the plunger",
       "M24 stud into the plunger with thread-locker; screw the crosshead on until it seats on the plunger end", elev=25, azim=-50)
    st(3, [cyl, ad, xh], [mv(links, (0, 0, 90)), mv(xpins, (0, 0, -110))], "links onto the crosshead",
       "Link ends into the slots; pins up from below; washer and circlip on top of each", elev=30, azim=-60)
    st(4, [cyl, ad, xh, links, xpins], [mv(plo, (0, 0, -150)), mv(lo_b, (0, 0, -260))], "lower frame plate onto the adapter",
       "Four M16 screws from below with hardened washers; snug only until step 7", elev=-25, azim=-60)
    st(5, [ab], [mv(aa, (0, 260, 0))], "pair the jaw arms",
       "Slide arm A's centre knuckle sideways into arm B's groove until the pivot bores line up", elev=35, azim=-70)
    st(6, [cyl, ad, xh, links, xpins, plo, lo_b], [mv(s_lo, (0, 0, 120)), mv(part("Paired jaw arms", aa.shape + ab.shape, COL["arm_a"]), (0, 0, 220)),
                                                     mv(tpins, (0, 0, -150))],
       "spacer and jaw arms onto the lower plate", "Spacer on the pivot bore, arms on it, link ends into the tail slots; tail pins up from below, circlips on top",
       elev=30, azim=-60, label_done=False)
    done6 = [cyl, ad, xh, links, xpins, plo, lo_b, s_lo, aa, ab, tpins]
    st(7, done6, [mv(s_up, (0, 0, 120)), mv(pup, (0, 0, 220)), mv(up_b, (0, 0, 300)), mv(mpin, (0, 0, -250))],
       "upper spacer, upper plate and main pin", "Upper spacer and plate on; four screws; pin up from below through everything; washer and circlip on top; torque all eight screws",
       elev=25, azim=-60, label_done=False)
    st(8, done6 + [s_up, pup, up_b, mpin], [mv(hd, (0, 0, 160))], "carry handle onto the spreader",
       "Two M12 cap screws from under the upper plate into the handle feet", elev=30, azim=-60, label_done=False)
    # cutter
    ccyl = cu("cu_cyl", "Cutter cylinder", COL["cyl"])
    cad_ = cu("cu_adapter", "Collar adapter", COL["adapter"])
    car = part("Carrier with moving blade", CU["cu_carrier"].shape + CU["cu_mblade"].shape + CU["cu_mbolts"].shape, COL["carrier"])
    cplo = cu("cu_plate_lo", "Lower cutter plate", COL["cplate"])
    cpup = cu("cu_plate_up", "Upper cutter plate", COL["cplate"])
    cb = split(CU["cu_bolts"].shape)
    adb = [q for q in cb if q.bounding_box().center().X < 0]
    ad_lo = part("4 x M16 screws", comp(q for q in adb if q.bounding_box().center().Z < 0), COL["screw"])
    rest_lo = [q for q in cb if q.bounding_box().center().X > 0 and q.bounding_box().center().Z < 0]
    rest_up = [q for q in cb if q.bounding_box().center().X > 0 and q.bounding_box().center().Z > 0]
    up_all = part("12 screws, M16 and M12", comp([q for q in adb if q.bounding_box().center().Z > 0] + rest_up), COL["screw"])
    fb = cu("cu_fblade", "Fixed blade", COL["blade"])
    nose = cu("cu_nose", "Nose block", COL["nose"])
    stop = cu("cu_stop", "Stop bar", COL["stop"])
    ch = cu("cu_handle", "Carry handle", COL["handle"])
    st(9, [ccyl], [mv(cad_, (160, 0, 0))], "collar adapter onto the cutter cylinder",
       "As step 1: by hand until the collar end is flush with the front face", elev=25, azim=-50)
    st(10, [ccyl, cad_], [mv(car, (160, 0, 0))], "blade carrier onto the plunger",
       "Moving blade on the carrier first (two M16 from the back, thread-locker); stud into the plunger; carrier on until it seats",
       elev=25, azim=-50)
    st(11, [ccyl, cad_, car], [mv(cplo, (0, 0, -150)), mv(ad_lo, (0, 0, -250))], "lower cutter plate onto the adapter",
       "Four M16 screws from below; snug only", elev=-25, azim=-60, label_done=False)
    st(12, [ccyl, cad_, car, cplo, ad_lo], [mv(fb, (0, 0, 160)), mv(nose, (0, 0, 160)), mv(stop, (0, 0, 160)),
                                            mv(part("4 x M16 screws", b.Compound(children=rest_lo), COL["screw"]), (0, 0, -200))],
       "fixed blade, nose block and stop bar", "Stand them on the lower plate; nose and stop screws up from below; fixed blade rests on the moving blade",
       elev=30, azim=-60, label_done=False)
    done12 = [ccyl, cad_, car, cplo, ad_lo, fb, nose, stop, part("Lower screws", b.Compound(children=rest_lo), COL["screw"])]
    st(13, done12, [mv(cpup, (0, 0, 180)), mv(up_all, (0, 0, 280))], "upper cutter plate",
       "Eight M16 (adapter, nose, stop) and four M12 (fixed blade); torque all twenty; check the 0.2 mm blade gap", elev=30, azim=-60,
       label_done=False)
    st(14, done12 + [cpup, up_all], [mv(ch, (0, 0, 160))], "carry handle onto the cutter",
       "Two M12 cap screws from under the upper plate into the handle feet", elev=30, azim=-60, label_done=False)
    # ram
    rb = part("Base plate", RM["rm_base"].shape, COL["base"])
    rr = part("Riser block (when needed)", RM["rm_riser"].shape, COL["riser"])
    rc = part("Ram cylinder", RM["rm_cyl"].shape + RM["rm_coupler"].shape, COL["cyl"])
    rs = part("Tilting saddle", RM["rm_saddle"].shape, COL["saddle"])
    st(15, [rb], [mv(rr, (0, 0, 180)), mv(rc, (0, 0, 380)), mv(rs, (0, 0, 520))], "the lifting ram stack",
       "Riser spigot into the base ring; cylinder base into the riser ring; saddle stem into the plunger. Never a riser on the plunger",
       elev=18, azim=-55)
    # pump
    pump = part("Hand pump", PU["pu_pump"].shape, COL["pump"])
    gauge = part("Gauge and adapter", PU["pu_gauge"].shape, COL["gauge"])
    hose = part("Hose with couplers", hose_coil(P["PUMP_BOX"][0] + 330, -260), COL["hose"])
    st(16, [pump], [mv(gauge, (180, 0, 0)), mv(hose, (0, -250, 0))], "gauge and hose onto the pump",
       "Gauge adapter on the pump outlet with thread sealant; hose coupler on the adapter; dust caps on every open coupler",
       elev=30, azim=-60)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "joints", "steps"]
    fns = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps}
    for w in what:
        name, _, sel = w.partition(":")
        if sel:
            r = fns[name]([int(s) for s in sel.split(",")])
        else:
            r = fns[name]()
        print(w, "->", r)
