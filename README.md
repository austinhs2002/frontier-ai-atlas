# Frontier AI Atlas (Nov 2026)

Interactive 5-slide comparison deck and standalone vector plates comparing frontier models across **Anthropic** (Claude Opus 5.5, Fable 5.2, Sonnet 5.5), **OpenAI** (GPT-6.2 Astra, Sol), and **Google DeepMind** (Gemini 4 Neon, Carbon).

- **Live Site (GitHub Pages):** https://austinhs2002.github.io/frontier-ai-atlas/
- **Repository:** https://github.com/austinhs2002/frontier-ai-atlas

## Structure

- `index.html` — Self-contained interactive 5-slide presentation (light/dark toggle, `←`/`→` keyboard navigation, interactive capability matrix, radar, Pareto economics, and effort switchers).
- `build_graphics.py` — Pure Python generator for the 4 standalone `1600×900` vector plates (native SVG `<text>`/`<tspan>`, zero `<foreignObject>`).
- `graphics/01–04*.svg` — Generated vector plates (do not edit by hand; regenerate via `build_graphics.py`).

## Agent / Developer Workflow (Claude Code, Codex, Antigravity)

1. **Edit in sync:** Update both `index.html` and `build_graphics.py` whenever changing data, labels, or palette colors. Never hand-edit `graphics/*.svg`.
2. **Regenerate & verify SVGs:**
   ```bash
   python build_graphics.py
   python -c "import xml.etree.ElementTree as ET, glob; [ET.parse(f) for f in glob.glob('graphics/*.svg')]; print('SVG XML OK')"
   ```
3. **Commit & deploy:**
   ```bash
   git add -A
   git commit -m "Describe change"
   git push
   ```
   GitHub Pages automatically rebuilds and publishes `main` (`/`) to https://austinhs2002.github.io/frontier-ai-atlas/ within ~30 seconds.
