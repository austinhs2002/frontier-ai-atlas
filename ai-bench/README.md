# AI Bench tab

This is the fifth tab of the Frontier AI Atlas: `#ai-bench`. It's a self-contained module.

| File | Purpose | Edit? |
|---|---|---|
| `data.js` | All content: status, methodology, roster, pilots, runs, milestones, caveats | **Yes, the only file to edit for updates** |
| `tab.js` | Renders `window.AI_BENCH_DATA` into `#ai-bench` using the site's existing classes | Rarely |
| `../index.html` | One-time mount: the chapters entry, the empty section and two script tags | **Never again** |

**Never put benchmark questions, answer keys or pilot item text in `data.js`.** This page is public. Use only aggregates and methodology.

## Adding a scored run
Append to `runs` in `data.js`:
```js
{ contestant: "GPT-6.2 Sol", lab: "OpenAI", labKey: "o", effort: "medium", benchmark: "NT-Contained",
  harness: "Codex", correct: 61, eligible: 140, score: null, selfFamilyFlag: false, notes: "" }
```
- `score: null` computes `correct / eligible`.
- `selfFamilyFlag` is `true` for any Full run, because the set includes the contestant's own lab's questions.

Also update `updated`, bump `version`, and tick `milestones`.

## Check and push (one command, from the `Presentation` folder)
```powershell
node --check ai-bench/data.js; if ($?) { node --check ai-bench/tab.js }; if ($?) { git status --short }
```
- Confirm that only `ai-bench/` files are listed, with no changes to `index.html`, `graphics/` or anything else.
- Then commit and push:
```powershell
git add ai-bench; git commit -m "AI Bench: <milestone>"; git push origin main
```
GitHub Pages redeploys to https://austinhs2002.github.io/frontier-ai-atlas/#ai-bench in about 30 seconds.
