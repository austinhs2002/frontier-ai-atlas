"""Build the four downloadable, self-contained editorial figures."""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parent / "graphics"
PAPER, INK, SOFT, LINE = "#F6F3EC", "#222623", "#555D58", "#C7CABF"
CLAY, IRIS, FERN = "#93432D", "#5345A1", "#246444"


def text(x, y, value, size, color=INK, serif=False, bold=False):
    face = "Georgia,serif" if serif else "Segoe UI,Arial,sans-serif"
    weight = 650 if bold else 400
    return (f'<text x="{x}" y="{y}" font-family="{face}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}">{escape(value)}</text>')


def line(x1, y, x2):
    return f'<path d="M{x1} {y} H{x2}" stroke="{LINE}"/>'


def figure(filename, title, intro, columns, rows, foot):
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" '
             'viewBox="0 0 1600 900" role="img">',
             f'<title>{escape(title)}</title>',
             f'<rect width="1600" height="900" fill="{PAPER}"/>',
             text(76, 70, "Frontier AI Atlas", 33, serif=True, bold=True),
             text(1278, 65, "FIELD EDITION  /  NOV 2026", 16, SOFT), line(76, 95, 1524),
             text(76, 198, title, 76, serif=True), text(80, 253, intro, 25, SOFT)]
    for x, label in columns:
        parts.append(text(x, 335, label.upper(), 17, SOFT, bold=True))
    height = min(95, 424 // len(rows))
    for i, (values, accent) in enumerate(rows):
        top = 356 + i * height
        parts.append(line(76, top, 1524))
        for j, ((x, _), value) in enumerate(zip(columns, values)):
            parts.append(text(x, top + height * .64, value, 26 if j < 2 else 23,
                              accent if j == 1 else INK, bold=j == 1))
    parts.extend([line(76, 800, 1524), text(76, 848, foot, 20, SOFT), '</svg>'])
    (OUT / filename).write_text("\n".join(parts), encoding="utf-8")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    figure("01-fanned-capability-lens.svg", "Who gets the job?",
           "Seven assignments from a builder’s November project notes and benchmark comparisons.",
           [(76, "Assignment"), (630, "First pick"), (1080, "Effort")],
           [((job, model, effort), color) for job, model, effort, color in [
               ("Lead the project", "Opus 5.5", "High", CLAY),
               ("Own the code", "Opus 5.5", "High / max", CLAY),
               ("Review security", "Neon", "High", FERN),
               ("Build the hero mesh", "Astra 6.2", "Medium", IRIS),
               ("Repair geometry or texture", "Sol 6.2", "High / medium", IRIS),
               ("Design worlds and systems", "Fable 5.2", "Medium / high", CLAY),
               ("Stretch an API budget", "Sol 6.2", "High / xhigh", IRIS)]],
           "Project picks depend on the brief. The interactive edition gives the rationale and switch condition for each role.")
    figure("02-pareto-and-3d-leap.svg", "Same index. Eighteen times the price.",
           "At index 55, the atlas records a $9.46 difference in benchmark cost per task.",
           [(76, "Configuration"), (670, "API cost / task"), (1090, "AA index v5")],
           [(("Sol high", "$0.56", "55"), IRIS), (("Sonnet max", "$10.02", "55"), CLAY)],
           "Source: Artificial Analysis values recorded in the November atlas. $10.02 divided by $0.56 is approximately 17.9.")
    figure("03-effort-and-drama.svg", "The Gemini gap closes with effort.",
           "Carbon leads by ten AA Index points at low effort. Both reach 60 at high.",
           [(76, "Effort"), (670, "Carbon / index"), (1090, "Neon / index")],
           [(("Low", "54", "44"), FERN), (("Medium", "58", "55"), FERN),
            (("High", "60", "60"), FERN), (("Peak: high / xhigh", "60", "62"), FERN)],
           "Source: AA Intelligence Index v5 values recorded in the November atlas. Peak compares different effort settings.")
    figure("04-tri-lab-routing-cards.svg", "A tie on the terminal.",
           "For a long-horizon assignment, the additional 20-step observation changes the routing decision.",
           [(76, "Model"), (650, "Native Terminal-Bench 4.1"), (1180, "BOBA 20-step")],
           [(("Opus 5.5", "65.8%", "66.8%"), CLAY), (("Fable 5.2", "65.8%", "No result recorded"), CLAY)],
           "Sources: native Terminal-Bench 4.1 and BOBA 20-step as recorded in the atlas. Fable’s long-horizon result is unknown.")
