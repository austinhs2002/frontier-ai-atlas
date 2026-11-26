import math
import textwrap
from pathlib import Path

OUT_DIR = Path(__file__).parent / "graphics"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT = "Segoe UI, Inter, -apple-system, BlinkMacSystemFont, sans-serif"
MONO = "Cascadia Code, Consolas, ui-monospace, monospace"

BG = "#11151F"
PANEL = "#171C29"
PANEL_ALT = "#1E2536"
PANEL_TRUNC = "#131824"
BORDER = "#2A3347"
GRID = "#222B3E"
TEXT = "#EEF1F6"
MUTED = "#9AA5B8"
DIM = "#64748B"

# Distinct Lab / Model Colors (clearer separation across Anthropic tiers)
C_OPUS = "#E29B7D"      # Warm Gold
C_FABLE = "#CC8164"     # Deep Coral-Orange
C_SONNET = "#EBB9A2"    # Soft Rose-Terracotta
C_ASTRA = "#72C2A8"     # Emerald
C_SOL = "#A3D9C6"       # Teal-Mint
C_NEON = "#8EB8F0"      # Sky
C_CARBON = "#6695D9"    # Indigo

# Evidence Source Pill Colors
EV_STYLE = {
    "LOGGED": ("#193830", "#8CD4B5"),    # Dark green bg, bright emerald text
    "BENCH": ("#1D2F47", "#9BC8E8"),     # Deep blue bg, sky text
    "UNTESTED": ("#1E293B", "#94A3B8"),  # Slate bg, muted text
}


def esc(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def svg_wrapped_text(x: float, y: float, prefix: str, prefix_col: str, body: str, body_col: str,
                     max_chars: int, font_size: float, line_h: float) -> tuple[str, float]:
    full = f"{prefix} {body}"
    lines = textwrap.wrap(full, width=max_chars)
    out = [f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{font_size}">']
    for idx, ln in enumerate(lines):
        dy = "0" if idx == 0 else f"{line_h}"
        if idx == 0 and ln.startswith(prefix):
            rest = ln[len(prefix):]
            out.append(
                f'<tspan x="{x}" dy="{dy}" fill="{prefix_col}" font-weight="700">{esc(prefix)}</tspan>'
                f'<tspan fill="{body_col}">{esc(rest)}</tspan>'
            )
        else:
            out.append(f'<tspan x="{x}" dy="{dy}" fill="{body_col}">{esc(ln)}</tspan>')
    out.append("</text>")
    return "\n".join(out), y + len(lines) * line_h


def svg_shell(title: str, subtitle: str, tag: str, body: str, footer: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" height="900">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#11151F"/>
      <stop offset="100%" stop-color="#181F30"/>
    </linearGradient>
    <linearGradient id="anthGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#CC8164"/>
      <stop offset="100%" stop-color="#EBB9A2"/>
    </linearGradient>
    <linearGradient id="oaiGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#5FA890"/>
      <stop offset="100%" stop-color="#A3D9C6"/>
    </linearGradient>
    <linearGradient id="googGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#6695D9"/>
      <stop offset="100%" stop-color="#9BC2F5"/>
    </linearGradient>
  </defs>
  <rect width="1600" height="900" fill="url(#bgGrad)"/>

  <!-- Header -->
  <g transform="translate(56, 40)">
    <rect x="0" y="0" width="246" height="25" rx="12.5" fill="#1E293B" stroke="#334155" stroke-width="1"/>
    <text x="123" y="16.5" text-anchor="middle" fill="#CBD5E1" font-family="{MONO}" font-size="11" font-weight="600" letter-spacing="1">{esc(tag)}</text>
    <text x="0" y="58" fill="{TEXT}" font-family="{FONT}" font-size="29" font-weight="700" letter-spacing="-0.5">{esc(title)}</text>
    <text x="0" y="83" fill="{MUTED}" font-family="{FONT}" font-size="14">{esc(subtitle)}</text>

    <!-- Evidence Legend Top-Right -->
    <g transform="translate(1058, 8)">
      <rect x="0" y="0" width="430" height="44" rx="10" fill="{PANEL}" stroke="{BORDER}" stroke-width="1"/>
      <rect x="14" y="12" width="66" height="20" rx="5" fill="#064E3B"/>
      <text x="47" y="26" text-anchor="middle" fill="#8CD4B5" font-family="{MONO}" font-size="10.5" font-weight="700">LOGGED</text>
      <text x="88" y="26" fill="{MUTED}" font-family="{FONT}" font-size="11.5">Real project</text>
      <rect x="166" y="12" width="58" height="20" rx="5" fill="#1E3A5F"/>
      <text x="195" y="26" text-anchor="middle" fill="#7DD3FC" font-family="{MONO}" font-size="10.5" font-weight="700">BENCH</text>
      <text x="232" y="26" fill="{MUTED}" font-family="{FONT}" font-size="11.5">AA / Card only</text>
      <rect x="322" y="12" width="76" height="20" rx="5" fill="#1E293B"/>
      <text x="360" y="26" text-anchor="middle" fill="#94A3B8" font-family="{MONO}" font-size="10.5" font-weight="700">UNTESTED</text>
    </g>
  </g>

  <line x1="56" y1="142" x2="1544" y2="142" stroke="{BORDER}" stroke-width="1"/>

  {body}

  <!-- Footer -->
  <line x1="56" y1="848" x2="1544" y2="848" stroke="{BORDER}" stroke-width="1"/>
  <text x="56" y="875" fill="{DIM}" font-family="{FONT}" font-size="12">{esc(footer)}</text>
  <text x="1544" y="875" text-anchor="end" fill="{DIM}" font-family="{MONO}" font-size="11.5">CALIBRATED FRONTIER ATLAS · NOV 2026</text>
</svg>'''


# ==============================================================================
# PLATE 1: CALIBRATED FOCAL-LENS (Per-Cell Effort + Evidence; Bars ONLY on Numbers)
# ==============================================================================
def build_plate_1():
    # No column-wide effort pairs! Each cell states its exact effort + evidence source.
    models = [
        ("Opus 5.5", "Anthropic", C_OPUS),
        ("Fable 5.2", "Anthropic", C_FABLE),
        ("Sonnet 5.5", "Anthropic", C_SONNET),
        ("Astra 6.2", "OpenAI", C_ASTRA),
        ("Sol 6.2", "OpenAI", C_SOL),
        ("Neon", "Google", C_NEON),
        ("Carbon", "New $20 Pro", C_CARBON),
    ]

    # Cell tuple: (effort, evidence, label, bar_pct, is_bright, is_crown)
    # Two-tier brightness: is_bright=True for measured numbers + user-confirmed rankings; False (~0.32 opacity) for qualitative estimates.
    expanded_rows = [
        ("1. Project Lead", "Holds 30+ step intent, delegates cleanly, stays on track", [
            ("high", "LOGGED", "CROWN · 1797 Elo", 98, True, True),
            ("med", "LOGGED", "#2 lead · 1785 Elo", 93, True, False),
            ("high", "LOGGED", "Sub-lead / installs", 72, False, False),
            ("high", "BENCH", "1643 Elo · terse", 64, True, False),
            ("med", "LOGGED", "Scoped work only", 60, False, False),
            ("high", "BENCH", "1699 Elo · strong", 82, True, False),
            ("high", "BENCH", "1611 Elo", 56, True, False),
        ]),
        ("2. Proficient Coder", "Native T-Bench 4.1 (tbench.ai) + BOBA 20-step", [
            ("hi/max", "LOGGED", "CROWN · 65.8% · BOBA #1", 98, True, True),
            ("xhigh", "BENCH", "65.8% T4.1 (tie) · $14.83", 98, True, False),
            ("high", "LOGGED", "Patches / server", 82, False, False),
            ("max", "BENCH", "62.1% T4.1", 78, True, False),
            ("xhigh", "LOGGED", "61.5% T4.1 · fallback", 80, True, False),
            ("xhigh", "BENCH", "44.4% FC · 61.2% T4.1", 86, True, False),
            ("high", "BENCH", "64.5% T4.1 · 40.6% FC", 82, True, False),
        ]),
        ("3. General Security", "Writes safe code, resists hijacking, finds & fixes flaws", [
            ("high", "LOGGED", "#2 · 74.2% GN / triage", 92, True, False),
            ("high", "BENCH", "75% CWE-v2 · fallback*", 84, True, False),
            ("high", "LOGGED", "Std Opus reviewer", 64, False, False),
            ("xhigh", "LOGGED", "Backup precision", 78, False, False),
            ("xhigh", "BENCH", "66.0% CWE-v2", 70, True, False),
            ("high", "LOGGED", "CROWN · Q68 (t-#2)/sev", 95, True, True),
            ("high", "BENCH", "79.3% AA-LCR · Q64", 86, True, False),
        ]),
        ("4. From-Scratch 3D Assets", "Builds clean 3D models from zero — no image-to-mesh", [
            ("max", "BENCH", "1202 AA-3D", 44, True, False),
            ("max", "BENCH", "1271 AA-3D (bench)", 77, True, False),
            ("high", "UNTESTED", "Untested on 3D", 36, False, False),
            ("med", "LOGGED", "CROWN · max 1318", 100, True, True),
            ("high", "LOGGED", "#2 hero · 1259 max", 90, True, False),
            ("xhigh", "BENCH", "1246 (#4) QA", 66, True, False),
            ("high", "BENCH", "1200 AA-3D", 42, True, False),
        ]),
        ("5. 3D Textures, Rigging & Fixes", "Iterates on meshes, textures, Blender fixes & anim", [
            ("high", "LOGGED", "Strong geo/anim", 84, False, False),
            ("high", "LOGGED", "Cost overkill", 54, False, False),
            ("high", "LOGGED", "Tied anim · trial", 82, False, False),
            ("high", "LOGGED", "High unneeded", 68, False, False),
            ("hi/med", "LOGGED", "CROWN · hi geo/med tx", 95, True, True),
            ("high", "LOGGED", "3D visual QA", 76, False, False),
            ("high", "UNTESTED", "Untested on 3D", 38, False, False),
        ]),
        ("6. Creative & World Design", "Designs cohesive worlds, player feel & systems", [
            ("med", "LOGGED", "Daily place keeper", 86, False, False),
            ("hi/max", "LOGGED", "CROWN · max feel", 98, True, True),
            ("med", "LOGGED", "Flat ground only", 54, False, False),
            ("med", "LOGGED", "Literalist method", 64, False, False),
            ("xhigh", "LOGGED", "Continent build", 66, False, False),
            ("high", "UNTESTED", "Analytical tone", 56, False, False),
            ("low", "LOGGED", "Corpus advice", 72, False, False),
        ]),
        ("7. Output per Dollar", "Finished work per dollar spent — not just token rates", [
            ("high", "LOGGED", "$4/$20 steady", 54, True, False),
            ("med", "LOGGED", "$3.80 · best knee", 48, True, False),
            ("med", "LOGGED", "#2 · $0.78 (hi $1.64)", 78, True, False),
            ("xhigh", "BENCH", "$2.52 · Index 62", 68, True, False),
            ("xhigh", "BENCH", "CROWN · $0.65 (Idx 56)", 99, True, True),
            ("xhigh", "BENCH", "$6.44 · 110 t/s", 58, True, False),
            ("low", "LOGGED", "Saves Fable/Astra", 70, False, False),
        ]),
    ]

    truncated_rows = [
        ("General Knowledge & Advice", "Closed-book recall & low-effort Q&A (Carbon low effort = Gemini’s Fable)",
         [("🥉 ~66%", "BENCH"), ("🥇 79% (low eff)", "LOGGED"), ("Mid", "BENCH"), ("🥈 69%", "BENCH"), ("62%", "BENCH"), ("55 idx", "BENCH"), ("AA 54 (low eff)", "LOGGED")]),
        ("Files, Desktop & Bulk Tasks", "OS automation, file ops & large batch gathering",
         [("🥇 87% OSW", "BENCH"), ("76% Auto", "BENCH"), ("Chores", "LOGGED"), ("No 6.2 OSW", "UNTESTED"), ("🥈 Gathers", "LOGGED"), ("🥉 79% Auto", "BENCH"), ("78% Auto", "BENCH")]),
        ("Science, Health, & Math", "PhD science (GPQA), research physics (CritPt) & proofs",
         [("94% GPQA", "BENCH"), ("🥇 76.5% Crit", "BENCH"), ("Std", "BENCH"), ("🥈 97% GPQA", "BENCH"), ("100% FM", "BENCH"), ("60.5% Crit", "BENCH"), ("🥉 69% Crit", "BENCH")]),
    ]

    parts = []
    left_x = 56
    label_w = 322
    col_w = 166
    table_x = left_x + label_w

    parts.append(f'<rect x="{left_x}" y="156" width="1488" height="462" rx="14" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.2"/>')
    parts.append(f'<rect x="{left_x}" y="156" width="6" height="462" rx="3" fill="{C_OPUS}"/>')
    parts.append(f'<text x="{left_x+20}" y="182" fill="{TEXT}" font-family="{FONT}" font-size="14" font-weight="700">FANNED WORKFLOW CORE (7 AXES · ONE CROWN PER ROW)</text>')
    parts.append(f'<text x="{left_x+20}" y="200" fill="{MUTED}" font-family="{FONT}" font-size="11.2">Bright bar = Measured / Confirmed · Dim bar = Qualitative estimate</text>')

    # Model Column Headers (Lab name only, NO column-wide effort pairs!)
    for m_i, (m_name, m_sub, m_col) in enumerate(models):
        parts.append(f'<g transform="translate({table_x + m_i * col_w + 5}, 164)">')
        parts.append(f'<rect width="{col_w-10}" height="42" rx="8" fill="#0B0F19" stroke="{m_col}" stroke-opacity="0.65" stroke-width="1.3"/>')
        parts.append(f'<text x="{(col_w-10)/2}" y="19" text-anchor="middle" fill="{TEXT}" font-family="{FONT}" font-size="13.5" font-weight="700">{esc(m_name)}</text>')
        parts.append(f'<text x="{(col_w-10)/2}" y="35" text-anchor="middle" fill="{m_col}" font-family="{MONO}" font-size="10.2">{esc(m_sub)}</text>')
        parts.append('</g>')

    row_start_y = 218
    row_h = 56
    for r_i, (r_title, r_sub, cells) in enumerate(expanded_rows):
        ry = row_start_y + r_i * row_h
        if r_i > 0:
            parts.append(f'<line x1="{left_x+16}" y1="{ry-3}" x2="{left_x+1472}" y2="{ry-3}" stroke="{GRID}" stroke-width="1"/>')
        parts.append(f'<text x="{left_x+20}" y="{ry+18}" fill="{TEXT}" font-family="{FONT}" font-size="13.5" font-weight="700">{esc(r_title)}</text>')
        parts.append(f'<text x="{left_x+20}" y="{ry+36}" fill="{MUTED}" font-family="{FONT}" font-size="11">{esc(r_sub)}</text>')

        for c_i, (eff, ev, lbl, bar_pct, is_bright, is_crown) in enumerate(cells):
            m_col = models[c_i][2]
            bx = table_x + c_i * col_w + 6
            bw = col_w - 12
            is_carb_hl = (r_i == 2 and c_i == 6)
            bg_fill = "#17253B" if (is_crown or is_carb_hl) else "#0B0F19"
            stroke_col = m_col if (is_crown or is_carb_hl) else "#1E293B"
            sw = "1.8" if is_crown else ("1.4" if is_carb_hl else "1")
            parts.append(f'<rect x="{bx}" y="{ry+2}" width="{bw}" height="46" rx="7" fill="{bg_fill}" stroke="{stroke_col}" stroke-width="{sw}"/>')

            ev_bg, ev_fg = EV_STYLE[ev]
            parts.append(f'<text x="{bx+8}" y="{ry+16}" fill="{m_col if is_crown else MUTED}" font-family="{MONO}" font-size="10" font-weight="700">{esc(eff)}</text>')
            pill_w = 48 if ev != "UNTESTED" else 58
            parts.append(f'<rect x="{bx+bw-pill_w-6}" y="{ry+6}" width="{pill_w}" height="14" rx="4" fill="{ev_bg}"/>')
            parts.append(f'<text x="{bx+bw-pill_w/2-6}" y="{ry+16}" text-anchor="middle" fill="{ev_fg}" font-family="{MONO}" font-size="8.8" font-weight="700">{ev}</text>')

            bar_w = max(8, (bw - 16) * (bar_pct / 100.0))
            bar_op = "1.0" if is_crown else ("0.88" if is_bright else "0.30")
            parts.append(f'<rect x="{bx+8}" y="{ry+23}" width="{bw-16}" height="6" rx="3" fill="#1E293B"/>')
            parts.append(f'<rect x="{bx+8}" y="{ry+23}" width="{bar_w:.1f}" height="6" rx="3" fill="{m_col}" fill-opacity="{bar_op}"/>')
            txt_col = m_col if is_crown else (TEXT if is_bright else MUTED)
            parts.append(f'<text x="{bx+8}" y="{ry+42}" fill="{txt_col}" font-family="{MONO}" font-size="10.4" font-weight="{"700" if is_crown else ("600" if is_bright else "500")}">{esc(lbl)}</text>')

    ty_box = 634
    parts.append(f'<rect x="{left_x}" y="{ty_box}" width="1488" height="196" rx="14" fill="{PANEL_TRUNC}" stroke="#1E293B" stroke-width="1.2" stroke-dasharray="6 4"/>')
    parts.append(f'<rect x="{left_x}" y="{ty_box}" width="6" height="196" rx="3" fill="#475569"/>')
    parts.append(f'<text x="{left_x+20}" y="{ty_box+25}" fill="#CBD5E1" font-family="{MONO}" font-size="11.5" font-weight="700" letter-spacing="0.8">TRUNCATED PERIPHERAL BUCKETS (NON-CORE GENERALIST CAPABILITIES COMPRESSED)</text>')

    t_start_y = ty_box + 40
    for r_i, (r_title, r_sub, cells) in enumerate(truncated_rows):
        ry = t_start_y + r_i * 49
        if r_i > 0:
            parts.append(f'<line x1="{left_x+16}" y1="{ry-4}" x2="{left_x+1472}" y2="{ry-4}" stroke="#172033" stroke-width="1"/>')
        parts.append(f'<text x="{left_x+20}" y="{ry+15}" fill="#CBD5E1" font-family="{FONT}" font-size="12.5" font-weight="600">{esc(r_title)}</text>')
        parts.append(f'<text x="{left_x+20}" y="{ry+31}" fill="{DIM}" font-family="{FONT}" font-size="10.8">{esc(r_sub)}</text>')

        for c_i, (note, ev) in enumerate(cells):
            bx = table_x + c_i * col_w + 6
            bw = col_w - 12
            ev_bg, ev_fg = EV_STYLE[ev]
            parts.append(f'<rect x="{bx}" y="{ry+4}" width="{bw}" height="30" rx="6" fill="#0B0F19" stroke="#1E293B" stroke-width="1"/>')
            parts.append(f'<text x="{bx+10}" y="{ry+23}" fill="#CBD5E1" font-family="{MONO}" font-size="11">{esc(note)}</text>')
            parts.append(f'<text x="{bx+bw-8}" y="{ry+23}" text-anchor="end" fill="{ev_fg}" font-family="{MONO}" font-size="9" font-weight="700">{ev}</text>')

    return svg_shell(
        "Calibrated Capability Lens — Per-Cell Effort, Evidence & True Crowns",
        "80% spread across your 7 active workflow axes (strictly one crown/row); bars shown ONLY on measured metrics",
        "PLATE 01 · FOCAL-LENS MATRIX",
        "\n".join(parts),
        "Calibrated against Models.md + Nov 24 $20 Pro Carbon unlock. Neon’s Row 3 crown explicitly requires Claude severity triage; Fable coding is benchmark-only.",
    )


# ==============================================================================
# PLATE 2: PARETO ECONOMICS (NO COLLISIONS + MEASURED VS EST) & 3D ASSET LEAP
# ==============================================================================
def build_plate_2():
    parts = []

    px, py, pw, ph = 96, 186, 820, 610
    c_min, c_max = 0.50, 35.0
    y_min, y_max = 53.0, 66.5

    def x_of(cost):
        t = (math.log10(cost) - math.log10(c_min)) / (math.log10(c_max) - math.log10(c_min))
        return px + t * pw

    gy = py + 26
    gh = ph - 36
    def y_of(score):
        return gy + gh - ((score - y_min) / (y_max - y_min)) * gh

    parts.append(f'<rect x="{px-40}" y="{py-20}" width="{pw+64}" height="{ph+72}" rx="14" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.2"/>')
    parts.append(f'<text x="{px-16}" y="{py+8}" fill="{TEXT}" font-family="{FONT}" font-size="18" font-weight="700">A. True Per-Task Economics (AA Index v5 vs. USD / Task)</text>')

    parts.append(f'<circle cx="{px+pw-248}" cy="{py+3}" r="5.5" fill="{TEXT}"/>')
    parts.append(f'<text x="{px+pw-237}" y="{py+7}" fill="{MUTED}" font-family="{MONO}" font-size="11">Measured AA</text>')
    parts.append(f'<circle cx="{px+pw-138}" cy="{py+3}" r="5.5" fill="#0B0F19" stroke="{TEXT}" stroke-width="2" stroke-dasharray="2 1"/>')
    parts.append(f'<text x="{px+pw-127}" y="{py+7}" fill="{MUTED}" font-family="{MONO}" font-size="11">Est. Effort Tier</text>')

    parts.append(f'<rect x="{px}" y="{gy}" width="{pw}" height="{gh}" rx="8" fill="#0B0F19" stroke="{GRID}"/>')

    for cost_tick in [1, 2, 3, 5, 10, 25]:
        cx = x_of(cost_tick)
        parts.append(f'<line x1="{cx:.1f}" y1="{gy}" x2="{cx:.1f}" y2="{gy+gh}" stroke="{GRID}" stroke-dasharray="4 4"/>')
        parts.append(f'<text x="{cx:.1f}" y="{gy+gh+22}" text-anchor="middle" fill="{MUTED}" font-family="{MONO}" font-size="12">${cost_tick}</text>')

    parts.append(f'<text x="{px+pw/2}" y="{gy+gh+44}" text-anchor="middle" fill="{MUTED}" font-family="{FONT}" font-size="12.5" font-weight="600">Weighted API Cost per Completed Task (Log USD — Sol $1.01 vs Sonnet med &lt;$1)</text>')

    for y_tick in range(54, 67, 2):
        cy = y_of(y_tick)
        parts.append(f'<line x1="{px}" y1="{cy:.1f}" x2="{px+pw}" y2="{cy:.1f}" stroke="{GRID}"/>')
        parts.append(f'<text x="{px-10}" y="{cy+4:.1f}" text-anchor="end" fill="{MUTED}" font-family="{MONO}" font-size="12">{y_tick}</text>')

    pareto_pts = [(0.56, 55.0), (0.65, 56.0), (1.01, 57.0), (2.52, 62.0), (9.08, 63.5), (26.54, 65.0)]
    parts.append(f'<polyline points="{" ".join(f"{x_of(c):.1f},{y_of(s):.1f}" for c,s in pareto_pts)}" fill="none" stroke="#475569" stroke-width="2.2" stroke-dasharray="7 5"/>')

    pts = [
        ("Sol 6.2 (xhigh)", "$0.65 · Index 56 (ROI Crown)", 0.65, 56.0, C_SOL, 11.0, True, 16, 12, "start", False),
        ("Sol 6.2 (max)", "$1.01 · Index 57 · ECI 169", 1.01, 57.0, C_SOL, 9.5, True, 16, -6, "start", False),
        ("Astra 6.2 (xhigh)", "$2.52 · Index 62 Peak", 2.52, 62.0, C_ASTRA, 11.0, True, 16, -8, "start", False),
        ("Neon (high)", "~$3.90 (est.) · 110 tok/s", 3.90, 60.0, C_NEON, 9.0, False, -18, -14, "end", True),
        ("Fable 5.2 (med)", "$3.80 · Best Fable Knee", 3.80, 61.5, C_FABLE, 9.5, False, 16, -24, "start", True),
        ("Carbon (med)", "~$4.60 (est.) · Index 58", 4.60, 58.0, C_CARBON, 8.5, False, -18, 18, "end", True),
        ("Neon (xhigh)", "$6.44 · Index 61 · #1 Agent", 6.44, 61.0, C_NEON, 10.5, True, -18, -32, "end", True),
        ("Opus 5.5 (hi/max)", "~$6.80 (est.) · #1 Lead", 6.80, 59.0, C_OPUS, 11.0, False, -18, 36, "end", True),
        ("Carbon (high)", "$7.76 · CritPt 69% · ECI 170", 7.76, 60.0, C_CARBON, 10.0, True, 24, 16, "start", True),
        ("Sonnet 5.5 (max)", "$10.02 · Idx 55 (18× Sol hi)", 10.02, 55.0, "#EF4444", 8.5, True, 15, 4, "start", False),
        ("Fable 5.2 (high)", "$9.08 · 49.1% FC (bench)", 9.08, 63.5, C_FABLE, 10.5, True, 18, -12, "start", False),
        ("Fable 5.2 (max)", "$26.54 · Index 65 Ceiling", 26.54, 65.0, C_FABLE, 12.0, True, -18, 4, "end", False),
    ]

    for name, sub, c, s, col, r, meas, dx, dy, anc, leader in pts:
        cx, cy = x_of(c), y_of(s)
        tx, ty = cx + dx, cy + dy
        if leader:
            lx_end = tx + (6 if anc == "end" else -6)
            parts.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{lx_end:.1f}" y2="{ty-2:.1f}" stroke="{col}" stroke-opacity="0.55" stroke-width="1.3"/>')
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r+4}" fill="{col}" fill-opacity="0.14"/>')
        if meas:
            parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{col}" stroke="#0B0F19" stroke-width="2"/>')
        else:
            parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="#0B0F19" stroke="{col}" stroke-width="2.6" stroke-dasharray="3 2"/>')
        parts.append(f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anc}" fill="{TEXT}" font-family="{FONT}" font-size="12.2" font-weight="700">{esc(name)}</text>')
        parts.append(f'<text x="{tx:.1f}" y="{ty+14:.1f}" text-anchor="{anc}" fill="{MUTED}" font-family="{FONT}" font-size="10.8">{esc(sub)}</text>')

    rx, ry, rw, rh = 960, 166, 584, 662
    parts.append(f'<g transform="translate({rx}, {ry})">')
    parts.append(f'<rect width="{rw}" height="{rh}" rx="14" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.2"/>')
    parts.append(f'<text x="26" y="36" fill="{TEXT}" font-family="{FONT}" font-size="18.5" font-weight="700">B. Proof Scaling Isn’t Capped: The 3D Asset Jump</text>')
    parts.append(f'<text x="26" y="57" fill="{MUTED}" font-family="{FONT}" font-size="12.5">AA-3D Elo (bench ceiling): closed-loop spatial RL obsoleted Meshy</text>')

    bars_3d = [
        ("GPT-6.2 Astra (max bench)", 1318, C_ASTRA, "Start at medium for hero assets (max overkill)", True),
        ("Claude Fable 5.2 (max)", 1271, C_FABLE, "#2 AA-3D · strong creative composition", False),
        ("GPT-6.2 Sol (max bench)", 1259, C_SOL, "#3 AA-3D · high for geometry, med for texture", True),
        ("Gemini 4 Neon (xhigh)", 1246, C_NEON, "#4 AA-3D · strong 3D visual review", False),
        ("Claude Opus 5.5 (max)", 1202, C_OPUS, "Stronger on rig/code fixes than raw mesh gen", False),
        ("Gemini 4 Carbon (high)", 1200, C_CARBON, "Built for causal depth, not 3D topology", False),
        ("GPT-6 Astra (prior 6.0)", 1168, "#475569", "Needed 2D image → Meshy (+150 Elo jump in 6.2)", False),
        ("GPT-6 Sol (prior 6.0)", 1131, "#334155", "Pre-6.2 spatial baseline (+128 Elo jump in 6.2)", False),
    ]

    by0 = 84
    for idx, (b_name, elo, col, note, hi) in enumerate(bars_3d):
        by = by0 + idx * 56
        parts.append(f'<text x="26" y="{by+14}" fill="{TEXT if hi else "#CBD5E1"}" font-family="{FONT}" font-size="13" font-weight="{"700" if hi else "500"}">{esc(b_name)}</text>')
        parts.append(f'<text x="{rw-26}" y="{by+14}" text-anchor="end" fill="{col if hi else MUTED}" font-family="{MONO}" font-size="13" font-weight="700">{elo} Elo</text>')
        parts.append(f'<rect x="26" y="{by+21}" width="{rw-52}" height="12" rx="6" fill="#0B0F19" stroke="#1E293B"/>')
        w_bar = ((elo - 1080) / (1350 - 1080)) * (rw - 52)
        parts.append(f'<rect x="26" y="{by+21}" width="{w_bar:.1f}" height="12" rx="6" fill="{col}"/>')
        parts.append(f'<text x="26" y="{by+46}" fill="{DIM if elo < 1180 else MUTED}" font-family="{FONT}" font-size="11">{esc(note)}</text>')

    parts.append(f'''<rect x="24" y="544" width="{rw-48}" height="96" rx="10" fill="{PANEL_ALT}" stroke="{BORDER}"/>
      <text x="40" y="568" fill="{C_SOL}" font-family="{FONT}" font-size="13" font-weight="700">Why 2024 “Text Pre-Training Wall” Takes Miss This:</text>
      <text x="40" y="589" fill="{MUTED}" font-family="{FONT}" font-size="12">Web-text scraping plateaued in late 2024, so labs moved compute into</text>
      <text x="40" y="607" fill="{MUTED}" font-family="{FONT}" font-size="12">build → render → inspect RL loops. Jumping +150 Elo from 6.0 to 6.2</text>
      <text x="40" y="625" fill="{MUTED}" font-family="{FONT}" font-size="12">put real 3D topology inside the weights—impossible for Haiku swarms.</text>''')
    parts.append('</g>')

    return svg_shell(
        "Unit Economics & The Spatial 3D Phase Transition",
        "Measured AA API costs (solid) vs. effort estimates (hollow rings)—paired with the 6.0 → 6.2 spatial 3D jump",
        "PLATE 02 · ECONOMICS & 3D LEAP",
        "\n".join(parts),
        "Sources: Artificial Analysis v5.0.1 task cost telemetry (solid) & effort estimates (hollow); AA-3D Elo leaderboard (Nov 2026).",
    )


# ==============================================================================
# PLATE 3: EFFORT SCALING (CARBON vs NEON) & 30-STEP MECHANICAL DRAMA
# ==============================================================================
def build_plate_3():
    parts = []

    lx, ly, lw, lh = 56, 172, 724, 650
    parts.append(f'<g transform="translate({lx}, {ly})">')
    parts.append(f'<rect width="{lw}" height="{lh}" rx="14" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.2"/>')
    parts.append(f'<text x="28" y="36" fill="{TEXT}" font-family="{FONT}" font-size="19.5" font-weight="700">A. Carbon vs. Neon Across Effort Tiers (AA Index v5)</text>')
    parts.append(f'<text x="28" y="58" fill="{MUTED}" font-family="{FONT}" font-size="13">Carbon’s heavy base weights carry low/medium; Neon needs xhigh chains to win</text>')

    gx, gy, gw, gh = 76, 92, 596, 400
    parts.append(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="8" fill="#0B0F19" stroke="{GRID}"/>')

    tiers = ["low", "medium", "high", "xhigh"]
    xs = [gx + 68 + i * ((gw - 136) / 3) for i in range(4)]

    def y_idx(val):
        return gy + gh - ((val - 42.0) / (63.0 - 42.0)) * gh

    for tick in [44, 48, 52, 56, 60, 62]:
        ty = y_idx(tick)
        parts.append(f'<line x1="{gx}" y1="{ty:.1f}" x2="{gx+gw}" y2="{ty:.1f}" stroke="{GRID}"/>')
        parts.append(f'<text x="{gx-12}" y="{ty+4:.1f}" text-anchor="end" fill="{MUTED}" font-family="{MONO}" font-size="12">{tick}</text>')

    for i, tname in enumerate(tiers):
        tx = xs[i]
        parts.append(f'<line x1="{tx:.1f}" y1="{gy}" x2="{tx:.1f}" y2="{gy+gh}" stroke="{GRID}" stroke-dasharray="4 4"/>')
        parts.append(f'<text x="{tx:.1f}" y="{gy+gh+24}" text-anchor="middle" fill="{TEXT}" font-family="{MONO}" font-size="13" font-weight="600">{tname}</text>')

    neon_vals = [44, 55, 60, 61]
    carb_vals = [54, 58, 60]
    parts.append(f'<polyline points="{" ".join(f"{xs[i]:.1f},{y_idx(v):.1f}" for i,v in enumerate(neon_vals))}" fill="none" stroke="{C_NEON}" stroke-width="3.5"/>')
    parts.append(f'<polyline points="{" ".join(f"{xs[i]:.1f},{y_idx(v):.1f}" for i,v in enumerate(carb_vals))}" fill="none" stroke="{C_CARBON}" stroke-width="3.5"/>')

    y_opus = y_idx(59)
    parts.append(f'<line x1="{gx}" y1="{y_opus:.1f}" x2="{gx+gw}" y2="{y_opus:.1f}" stroke="{C_OPUS}" stroke-width="1.4" stroke-dasharray="6 4"/>')
    parts.append(f'<text x="{gx+gw-12}" y="{y_opus-8:.1f}" text-anchor="end" fill="{C_OPUS}" font-family="{MONO}" font-size="11">Opus 5.5 max (59)</text>')

    parts.append(f'<line x1="{xs[0]:.1f}" y1="{y_idx(54)+10:.1f}" x2="{xs[0]:.1f}" y2="{y_idx(44)-10:.1f}" stroke="#F43F5E" stroke-width="2" stroke-dasharray="3 3"/>')
    parts.append(f'<rect x="{xs[0]+14:.1f}" y="{(y_idx(54)+y_idx(44))/2 - 13:.1f}" width="132" height="25" rx="6" fill="#1E1B4B" stroke="{C_CARBON}"/>')
    parts.append(f'<text x="{xs[0]+80:.1f}" y="{(y_idx(54)+y_idx(44))/2 + 4:.1f}" text-anchor="middle" fill="#E0E7FF" font-family="{MONO}" font-size="11.5" font-weight="700">Carbon +10 pts</text>')

    parts.append(f'<rect x="{xs[1]+14:.1f}" y="{y_idx(56.5)-12:.1f}" width="122" height="25" rx="6" fill="#1E1B4B" stroke="{C_CARBON}"/>')
    parts.append(f'<text x="{xs[1]+75:.1f}" y="{y_idx(56.5)+5:.1f}" text-anchor="middle" fill="#E0E7FF" font-family="{MONO}" font-size="11.5" font-weight="700">Carbon +3 pts</text>')

    for i, v in enumerate(neon_vals):
        cx, cy = xs[i], y_idx(v)
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7" fill="{C_NEON}" stroke="#0B0F19" stroke-width="2"/>')
        dy = 23 if i < 3 else -14
        parts.append(f'<text x="{cx:.1f}" y="{cy+dy:.1f}" text-anchor="middle" fill="{C_NEON}" font-family="{MONO}" font-size="12.5" font-weight="700">Neon {v}</text>')

    for i, v in enumerate(carb_vals):
        cx, cy = xs[i], y_idx(v)
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7" fill="{C_CARBON}" stroke="#0B0F19" stroke-width="2"/>')
        parts.append(f'<text x="{cx:.1f}" y="{cy-14:.1f}" text-anchor="middle" fill="{C_CARBON}" font-family="{MONO}" font-size="12.5" font-weight="700">Carbon {v}</text>')

    parts.append(f'''<rect x="28" y="534" width="{lw-56}" height="92" rx="10" fill="{PANEL_ALT}" stroke="{BORDER}"/>
      <text x="44" y="558" fill="{TEXT}" font-family="{FONT}" font-size="13.5" font-weight="700">Where Carbon Still Beats Neon Peak-for-Peak (Benchmarks):</text>
      <text x="44" y="580" fill="{MUTED}" font-family="{FONT}" font-size="12.2">• CritPt v2 Hard: 69.0% vs. 60.5% (+8.5 pts) · Terminal-Bench 4.1: 64.5% vs. 61.2% (+3.3 pts)</text>
      <text x="44" y="601" fill="{MUTED}" font-family="{FONT}" font-size="12.2">• AA-LCR 100k Synthesis: 79.3% vs. 74.7% (+4.6 pts) · Base weights hold AA 54 at low (+10 pts)</text>''')
    parts.append('</g>')

    rx, ry, rw, rh = 804, 172, 740, 650
    parts.append(f'<g transform="translate({rx}, {ry})">')
    parts.append(f'<rect width="{rw}" height="{rh}" rx="14" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.2"/>')
    parts.append(f'<text x="28" y="36" fill="{TEXT}" font-family="{FONT}" font-size="19.5" font-weight="700">B. Cutting Out “Mechanical Drama” Over 30 Steps</text>')
    parts.append(f'<text x="28" y="58" fill="{MUTED}" font-family="{FONT}" font-size="13">Why Opus 5.5 (Index 59) beats higher single-shot IQs across multi-session builds</text>')

    gx2, gy2, gw2, gh2 = 72, 92, 628, 400
    parts.append(f'<rect x="{gx2}" y="{gy2}" width="{gw2}" height="{gh2}" rx="8" fill="#0B0F19" stroke="{GRID}"/>')

    def x_step(step):
        return gx2 + (step / 30.0) * gw2

    def y_coh(pct):
        return gy2 + gh2 - (pct / 100.0) * gh2

    for pct in [20, 40, 60, 80, 100]:
        py_line = y_coh(pct)
        parts.append(f'<line x1="{gx2}" y1="{py_line:.1f}" x2="{gx2+gw2}" y2="{py_line:.1f}" stroke="{GRID}"/>')
        parts.append(f'<text x="{gx2-10}" y="{py_line+4:.1f}" text-anchor="end" fill="{MUTED}" font-family="{MONO}" font-size="12">{pct}%</text>')

    for st in [0, 5, 10, 15, 20, 25, 30]:
        sx = x_step(st)
        parts.append(f'<line x1="{sx:.1f}" y1="{gy2}" x2="{sx:.1f}" y2="{gy2+gh2}" stroke="{GRID}" stroke-dasharray="4 4"/>')
        parts.append(f'<text x="{sx:.1f}" y="{gy2+gh2+24}" text-anchor="middle" fill="{TEXT}" font-family="{MONO}" font-size="12">Step {st}</text>')

    curves = [
        ("Opus 5.5 (high) — ~0.5% noise/step (Quiet Idiom Lock)", 0.005, C_OPUS, "3.6", -10),
        ("Scoped Sol / Astra / Neon w/ Opus Triage (~1.8% noise)", 0.018, C_ASTRA, "2.8", -10),
        ("Unguided High-IQ Agent (~3.8% parallel bloat / false alarms)", 0.038, C_NEON, "2.6", -10),
        ("Hyperagent Haiku / Fast Wrapper Swarm (~7.5% seam drift)", 0.075, "#F43F5E", "2.6", 18),
    ]
    for label, rate, col, sw, ldy in curves:
        pts = [f"{x_step(st):.1f},{y_coh(100.0 * ((1.0 - rate) ** st)):.1f}" for st in range(31)]
        parts.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="{sw}"/>')
        end_coh = 100.0 * ((1.0 - rate) ** 30)
        parts.append(f'<circle cx="{x_step(30):.1f}" cy="{y_coh(end_coh):.1f}" r="5.5" fill="{col}"/>')
        parts.append(f'<text x="{x_step(29.4):.1f}" y="{y_coh(end_coh)+ldy:.1f}" text-anchor="end" fill="{col}" font-family="{FONT}" font-size="12" font-weight="700">{esc(label)} → {end_coh:.0f}%</text>')

    parts.append(f'''<rect x="28" y="534" width="{rw-56}" height="92" rx="10" fill="{PANEL_ALT}" stroke="{BORDER}"/>
      <text x="44" y="558" fill="{TEXT}" font-family="{FONT}" font-size="13.5" font-weight="700">The Four Flavors of Mechanical Drama:</text>
      <text x="44" y="580" fill="{MUTED}" font-family="{FONT}" font-size="12.2">• Performative smartness (inventing parallel helpers) · Crying wolf on non-bugs (Neon severity)</text>
      <text x="44" y="601" fill="{MUTED}" font-family="{FONT}" font-size="12.2">• Literalist method obedience over visual quality (Sol/Astra) · Swarm seam blindness (Haiku DAGs)</text>''')
    parts.append('</g>')

    return svg_shell(
        "Effort Curves & Why Quiet Restraint Wins Long Horizons",
        "Left: Carbon’s base-weight floor vs. Neon’s xhigh loop. Right: compounding alignment retention (1 − noise)^steps",
        "PLATE 03 · EFFORT & DRAMA",
        "\n".join(parts),
        "Sources: Artificial Analysis v5 thinking-tier telemetry (left) & compounding step-coherence model aligned with AA-Briefcase v1.1 Elo rankings (right).",
    )


# ==============================================================================
# PLATE 4: TRI-LAB ROUTING CARDS (100% NATIVE SVG, UPDATED SOL GEO/TEX & CARBON)
# ==============================================================================
def build_plate_4():
    labs = [
        {
            "lab": "ANTHROPIC",
            "tag": "Lead Coordinator, Repo Coding & Creative Ceiling",
            "accent": C_OPUS,
            "grad": "url(#anthGrad)",
            "Wave": "Next wave: Q1 2027 Fable 5.2 → Opus/Sonnet distillation (Project Rainier)",
            "models": [
                ("Claude Opus 5.5", "high (lead & coding) · med (floor) · xhigh/max (wide)",
                 "AA 59 · #1 Briefcase (1797) · #1 Native T4.1 (65.8%) & BOBA (66.8%)",
                 "Project lead, owns coding, security triage, composing places, rig/geo fixes with zero mechanical drama.",
                 "Trails on scratch 3D (1202) & 1M graph walks (66.8%); don't relay ownership from memory."),
                ("Claude Fable 5.2", "med ($3.80 knee) · high ($9.08 design) · low (Q&A)",
                 "#1 AA (65) · #1 ECI (173) · 49.1% FC (bench only)",
                 "Unmatched human-relation & system design; med is best efficiency knee ($3.80); high jumps clearly while xhigh ($14.83) plateaus.",
                 "2× Opus token rate; not routed for coding; ends early at low/med; cyber flags drop to fallback."),
                ("Sonnet 5.5 & Haiku 5.5", "Sonnet med (<$1 crown) / high · Haiku high/xhigh",
                 "Sonnet: allowance & install workhorse · Haiku: 36% Omniscience",
                 "Sonnet med wins budget efficiency; Sonnet high reviews Opus & runs installs; Haiku xhigh for 2nd-angle search.",
                 "Skip Sonnet max ($10.02 trap); Haiku swarms cannot design coupled system seams."),
            ],
        },
        {
            "lab": "OPENAI",
            "tag": "3D Asset Construction, Geometry/Texture & Fallback Code",
            "accent": C_ASTRA,
            "grad": "url(#oaiGrad)",
            "Wave": "Next wave: Riding 6.2 ROI while gating 'Bel' / GPT-7 behind RSI Control Rooms",
            "models": [
                ("GPT-6.2 Sol", "high (#2 hero 3D & geo) · med (tex/gathers) · xhigh (continent)",
                 "AA 57 · ECI 169 · $1.01 AA API · #3 AA-3D (1259)",
                 "High puts Sol #2 on scoped 3D hero assets & handles Blender geometry; med owns texture/gathers; xhigh continent/code.",
                 "xhigh degrades on focused single hero assets; tight ChatGPT cap; brief strict scope + open method; never Sol max for code."),
                ("GPT-6.2 Astra", "medium (hero 3D assets) · xhigh ($2.52 Index 62)",
                 "AA 62 · #1 ECI (173 tie) · #1 AA-3D (1318 at max)",
                 "From-scratch 3D hero assets starting at medium (obsoletes Meshy); backup precision reviewer at high/xhigh.",
                 "Astra max is overkill for game dev; plateaued on multi-file repo idiom fit (44.2% FC)."),
            ],
        },
        {
            "lab": "GOOGLE DEEPMIND",
            "tag": "1M Forensic Verification, Speed & Newly Unlocked Carbon",
            "accent": C_NEON,
            "grad": "url(#googGrad)",
            "Wave": "Next wave: Fastest iterative TPU element/Flash drops; Gemini 5 mid/late 2027",
            "models": [
                ("Gemini 4 Neon", "high (reviews/UI) · xhigh (audits) · med (default)",
                 "AA 61 · ~110 tok/s · #1 Coding Agent · ~1389 Design Elo",
                 "Outside cross-family security reviewer, pre-install live-vs-candidate forensic diff, and 3D visual QA (1246).",
                 "Overstates severity & re-opens settled decisions—Claude must triage findings; collapses at low (AA 44)."),
                ("Gemini 4 Carbon", "low (corpus advice — Fable of Gemini) · high (AA-LCR/CritPt)",
                 "AA 54 at low (+10 vs Neon) · #3 ECI (170) · 79.3% AA-LCR",
                 "General corpus-contained advice on low (saves Fable/Astra caps); beats Neon on CritPt (+8.5%), T-Bench 4.1 (64.5%), & AA-LCR.",
                 "Half Neon’s speed (~55 tok/s), weaker 3D (1200), and heavy base weights burn $20 Pro quota fast at high."),
            ],
        },
    ]

    parts = []
    col_w, col_h = 478, 658
    gap = 27
    sx, sy = 56, 168

    for i, lab in enumerate(labs):
        x = sx + i * (col_w + gap)
        parts.append(f'<g transform="translate({x}, {sy})">')
        parts.append(f'<rect width="{col_w}" height="{col_h}" rx="14" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.2"/>')
        parts.append(f'<rect width="{col_w}" height="7" rx="3.5" fill="{lab["grad"]}"/>')
        parts.append(f'<text x="22" y="34" fill="{lab["accent"]}" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="1.2">{esc(lab["lab"])}</text>')
        parts.append(f'<text x="22" y="55" fill="{TEXT}" font-family="{FONT}" font-size="15.5" font-weight="700">{esc(lab["tag"])}</text>')
        parts.append(f'<text x="22" y="73" fill="{DIM}" font-family="{FONT}" font-size="11">{esc(lab["Wave"])}</text>')
        parts.append(f'<line x1="22" y1="84" x2="{col_w-22}" y2="84" stroke="{GRID}"/>')

        n_m = len(lab["models"])
        card_h = 176 if n_m == 3 else 268
        step_y = 186 if n_m == 3 else 280
        fsize = 11.4 if n_m == 3 else 12.4
        lh = 15.5 if n_m == 3 else 18.2
        wrap_w = 60 if n_m == 3 else 56

        for m_i, (m_name, m_eff, m_met, m_pro, m_con) in enumerate(lab["models"]):
            my = 96 + m_i * step_y
            parts.append(f'<g transform="translate(18, {my})">')
            parts.append(f'<rect width="{col_w-36}" height="{card_h}" rx="10" fill="{PANEL_ALT}" stroke="{BORDER}"/>')
            parts.append(f'<text x="16" y="24" fill="{TEXT}" font-family="{FONT}" font-size="15.5" font-weight="700">{esc(m_name)}</text>')
            parts.append(f'<text x="16" y="42" fill="{lab["accent"]}" font-family="{MONO}" font-size="10.8" font-weight="600">{esc(m_eff)}</text>')
            parts.append(f'<text x="16" y="59" fill="#CBD5E1" font-family="{MONO}" font-size="10.4">{esc(m_met)}</text>')

            pro_svg, next_y = svg_wrapped_text(16, 80, "+ Best at:", "#8CD4B5", m_pro, "#E2E8F0", wrap_w, fsize, lh)
            con_svg, _ = svg_wrapped_text(16, next_y + 7, "− Watch:", "#E29B7D", m_con, "#94A3B8", wrap_w, fsize, lh)
            parts.append(pro_svg)
            parts.append(con_svg)
            parts.append('</g>')

        parts.append('</g>')

    return svg_shell(
        "Tri-Lab Seat & Effort Routing — Calibrated to Models.md",
        "Pure native vector cards: Opus owns coding, Sol high for geometry / med for texture, Neon findings triaged by Claude",
        "PLATE 04 · SEAT ROUTING PLAYBOOK",
        "\n".join(parts),
        "Scope-not-method for OpenAI · File/line proof + Opus triage for Neon · Carbon newly unlocked on $20 Pro (untested in project).",
    )


def main():
    plates = {
        "01-fanned-capability-lens.svg": build_plate_1(),
        "02-pareto-and-3d-leap.svg": build_plate_2(),
        "03-effort-and-drama.svg": build_plate_3(),
        "04-tri-lab-routing-cards.svg": build_plate_4(),
    }
    for fname, content in plates.items():
        out = OUT_DIR / fname
        out.write_text(content, encoding="utf-8")
        print(f"Wrote {out} ({len(content)} bytes)")


if __name__ == "__main__":
    main()
