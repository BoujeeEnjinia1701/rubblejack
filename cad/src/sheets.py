"""RubbleJack general arrangement sheet RBJ-DWG-001, Rev P1 (TRL 3, constructable design RBJ-DDR-002).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/RBJ-DWG-001.svg, .pdf and .png from the parametric model in cad/src/model.py
with .kit/drawing.py: the kit laid out on the ground as packed for a drill (pump with gauge, two
hoses, spreader, cutter and lifting ram set), three views with overall sizes, an isometric view
and the main dimensions of each tool, all taken from PARAMS and the model functions. The concept
blueprint in media/ is RBJ-DWG-010; the making sketches are RBJ-DWG-101 onward.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from build123d import Compound  # noqa: E402
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, components, cutter_levels, spreader_levels, tip_gap  # noqa: E402

DATE = "2026-10-03"


def safe_project_views(part, workdir, line_weight=0.35):
    """Front, top, right and isometric views, edge by edge, so a degenerate projected edge is skipped."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center()
    d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out = {}
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    pass
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    return out


def safe_views(part, workdir, line_weight=0.35, center_lines=True):
    """Same output as drawing.project_views (visible, hidden and centre lines), added edge by edge so a
    projected edge the SVG writer cannot convert (the hose torus) is skipped instead of stopping."""
    import drawing
    from build123d import ExportSVG, LineType, Unit, Edge, Vector
    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center()
    d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    min_r = 0.006 * max(bb.size.X, bb.size.Y, bb.size.Z)
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out = {}
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        ex.add_layer("Center", line_color=0x6B7280, line_type=LineType.ISO_LONG_DASH_DOT, line_weight=line_weight / 2)
        layers = [("Visible", visible)] + ([("Hidden", hidden)] if name != "iso" else [])
        for layer, edges in layers:
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except Exception:
                    pass
        if name != "iso" and center_lines:
            lines = [Edge.make_line(Vector(a[0], a[1], 0), Vector(b_[0], b_[1], 0))
                     for a, b_ in drawing._center_lines(part, name, c, bb, min_r)]
            if lines:
                ex.add_shape(lines, layer="Center")
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    return out


def patch_kit_views():
    """Point the kit's project_views at safe_views for this process (the kit itself is not edited)."""
    import drawing
    drawing.project_views = safe_views


def top_cell(sheet, views):
    """Where add_ortho puts the top view (x, y, w, h), repeating its layout arithmetic (kit 1.7)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab, dl = 14, 12, 11
    fw, fh = _viewbox(Path(views["front"]).read_text())[2:]
    tw, th = _viewbox(Path(views["top"]).read_text())[2:]
    rw, rh = _viewbox(Path(views["right"]).read_text())[2:]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap + dl)) / 2 + dl
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab + dl)) / 2 + dl
    return ax, ay, k * max(fw, tw), k * th


def main():
    comps = components(P, spreader_stroke=0.0, cutter_travel=0.0)
    kit = Compound(children=[c.shape for c in comps])
    work = ROOT / "cad" / "drawings" / "_views"
    views = safe_project_views(kit, work)
    bb = kit.bounding_box()
    s = Sheet(project="RubbleJack", title="Hand-pumped rescue tool kit: general arrangement", dwg_no="RBJ-DWG-001", rev="P1",
              author="Amish Chadha", date=DATE, scale=1 / 15, theme="technical",
              material="Per bom/bom.csv: 4340 and S690QL steel, S7 tool steel, 7075-T6 aluminium, bought 700 bar hydraulics. "
                       "PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "General arrangement of the constructable design (RBJ-DDR-002)", DATE, "AC")])
    s.add_ortho(views)
    x0, y0, w, h = top_cell(s, views)
    k = s.scale
    X = lambda mx: x0 + (mx - bb.min.X) * k   # noqa: E731
    Y = lambda my: y0 + h - (my - bb.min.Y) * k   # noqa: E731
    L = [_t(M + 12, M + 12, "PRELIMINARY, NOT FOR FABRICATION", 3.0, 600, INK)]
    tags = {"pump": "PUMP, GAUGE (1, 2)", "spreader": "SPREADER", "cutter": "CUTTER", "ram": "LIFTING RAM SET"}
    for tool, text in tags.items():
        sb = Compound(children=[c.shape for c in comps if c.tool == tool and c.bom != 3]).bounding_box()
        L.append(_t(X((sb.min.X + sb.max.X) / 2), Y(sb.max.Y) - 2.0, text, 2.0, 600, MUTED, "middle"))
    hb = Compound(children=[c.shape for c in comps if c.bom == 3]).bounding_box()
    L.append(_t(X((hb.min.X + hb.max.X) / 2), Y(hb.min.Y) + 4.0, "HOSES (3)", 2.0, 600, MUTED, "middle"))
    s._layers += L
    s.add_svg(views["iso"], 276, 40, 140, 84, label="Isometric view", sublabel="Not to scale; kit laid out as packed for a drill")
    lv, lc = spreader_levels(P), cutter_levels(P)
    tod, tw_, tl = P["RISER"]
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Cylinder (5), one per tool: 15 t, {P['STROKE']:.0f} stroke, {P['CYL_AREA_CM2']} cm2, 700 bar",
        f"Spreader: jaws {P['JAW_L']:.0f} pivot to tip, {P['ARM_T']:.0f} thick; tips {tip_gap(0.0):.0f} closed,"
        f" {tip_gap(lv['theta_max']):.0f} open",
        f"Spreader frame plates (7) 7075-T6, {P['FR_T']:.0f} thick, {2 * P['FR_Z']:.0f} apart inside",
        f"Pins (12): pivot {P['PIN_MAIN']:.0f}, links {P['PIN_LINK']:.0f}; link centres {P['LINK_L']:.0f}",
        f"Cutter: 16 bar in a {2 * P['CU_HOOK2']:.0f} hook; blade travel {P['CU_TRAVEL']:.0f} to the stop bar",
        f"Cutter plates (17) S690QL {P['CU_PL_T']:.0f}; stop bar {P['CU_STOP_L']:.0f} long, 2 screws each plate",
        f"Ram base (14) {P['BP_S']:.0f} square, {P['BP_T']:.0f} S690QL; riser (15) tube {tod} x {tw_:.0f}, {tl:.0f} long",
        f"Collar adapter (6) {P['AD_L']:.0f} x {2 * P['AD_W2']:.0f} x {2 * P['FR_Z']:.0f}; 8 x M16 12.9 to the plates",
        f"Hoses (3) {P['HOSE_L'] / 1000:.0f} m, 700 bar; pump (1) two-speed, {P['PUMP_OIL']:.0f} cm3 oil",
        "Every pressurised part rated 700 bar; pump relief 700 bar",
        "Third-angle; top view from +Z; (n) = BOM line",
    ], x=276, y=135, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "RBJ-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} at scale 1:{1 / k:g}; kit {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")


if __name__ == "__main__":
    main()
