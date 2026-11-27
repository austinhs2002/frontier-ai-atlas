// AI Bench data. This is the ONLY file to edit for ongoing updates; tab.js renders it.
// Raw numbers live in structured fields; prose lives in `text`/`notes`. Never publish benchmark
// questions, answer keys or pilot item text here: aggregates and methodology only.
window.AI_BENCH_DATA = {
  updated: "2026-11-27",
  version: "0.1.0",
  status: {
    phase: "Allocation designed; contributor requests drafted, not yet sent",
    summary: "An HLE-style hard exam written by a composite of frontier AI models, checked by a keeper model, reworded into one neutral voice, and scored by code. Two pilots have run; no exam runs yet."
  },

  // How the exam is scored. There are no AI judges: answers are exact and checked by code.
  scoring: "code",
  judges: [],

  // How the keeper, outside contributors, blind role and exclusions were chosen.
  selection: {
    keeper: {
      model: "Claude Opus 5.5",
      labKey: "a",
      method: "Ranked vote; models could not vote for themselves",
      result: "First choice on every eligible ballot (9 of 9). Second place split roughly evenly between GPT-6.2 Astra and Gemini 4 Carbon.",
      ownBallot: "Opus 5.5 voted Gemini 4 Carbon first, then GPT-6.2 Astra.",
      text: "GPT-6.1 Terra, GPT-6.2 Sol, GPT-6.2 Astra, Claude Opus 5.5, Claude Haiku 5.5, Claude Sonnet 5.5, Gemini 4 Carbon, Gemini 4 Argon, Gemini 4 Hydrogen."
    },
    outsideVote: {
      text: "Not yet recorded"
    },
    outside: [
      { model: "DeepSeek V4 (V4 Pro / V4.1-Flash)", status: "Included", priority: "Last in conflict priority", notes: "Pilot 2 investigator; also a contributor" },
      { model: "Kimi K3.1 Pro", status: "Attempted inclusion; not used", priority: "Second to last in conflict priority", notes: "K3 scored too low; K3.1 had access problems" }
    ],
    excluded: [
      { model: "Claude Haiku 5.5", labKey: "a", status: "Opted out (accepted)", reason: "Not yet recorded", laterRole: "" },
      { model: "Qwen4-Max", labKey: "", status: "Structurally excluded from contributing and being tested", reason: "Not yet recorded", laterRole: "Chosen as the neutral rewriter because it is never an examinee" },
      { model: "Mistral Large 4", labKey: "", status: "Structurally excluded", reason: "Not yet recorded", laterRole: "" },
      { model: "Grok 4.7", labKey: "", status: "Structurally excluded", reason: "Not yet recorded", laterRole: "" }
    ],
    neon: {
      text: "Gemini 4 Neon started as the strictly blind role — originally slated to be the test grader, so it was excluded from voting or being voted on. After the project switched to automated code grading, it served as a blind investigator in pilot 2 and is now an examinee. It never grades.",
      advisoryBallot: "Asked post-hoc (non-voting), Neon ranked Claude Opus 5.5 first and Gemini 4 Carbon second."
    }
  },

  // Every model with a part in the project. roles: keeper | contributor | examinee | investigator | rewriter
  roster: [
    { model: "Claude Opus 5.5",   lab: "Anthropic", labKey: "a", effort: "medium", roles: ["keeper", "contributor", "examinee"] },
    { model: "Claude Sonnet 5.5", lab: "Anthropic", labKey: "a", effort: "medium", roles: ["contributor", "examinee"] },
    { model: "Claude Fable 5.2",  lab: "Anthropic", labKey: "a", effort: "medium", roles: ["contributor", "examinee"] },
    { model: "Gemini 4 Carbon",   lab: "Google",    labKey: "g", effort: "medium", roles: ["contributor", "examinee"] },
    { model: "Gemini 4 Argon",    lab: "Google",    labKey: "g", effort: "medium", roles: ["contributor", "examinee"] },
    { model: "Gemini 4 Hydrogen", lab: "Google",    labKey: "g", effort: "medium", roles: ["contributor", "examinee"] },
    { model: "Gemini 4 Neon",     lab: "Google",    labKey: "g", effort: "",       roles: ["investigator", "examinee"] },
    { model: "GPT-6.2 Astra",     lab: "OpenAI",    labKey: "o", effort: "medium", roles: ["contributor", "examinee"] },
    { model: "GPT-6.2 Sol",       lab: "OpenAI",    labKey: "o", effort: "medium", roles: ["contributor", "examinee"] },
    { model: "GPT-6.1 Terra",     lab: "OpenAI",    labKey: "o", effort: "medium", roles: ["contributor", "examinee"] },
    { model: "DeepSeek V4",       lab: "DeepSeek",  labKey: "",  effort: "",       roles: ["contributor", "investigator"] },
    { model: "Qwen4-Max",         lab: "Alibaba",   labKey: "",  effort: "",       roles: ["rewriter"] }
  ],

  // The four benchmarks. One question set serves all four.
  benchmarks: [
    { id: "NT-Full",      tools: false, set: "full",      text: "No tools. A fresh session answers all questions." },
    { id: "NT-Contained", tools: false, set: "contained", text: "No tools. A fresh session answers only questions written by other labs." },
    { id: "T-Full",       tools: true,  set: "full",      text: "Best effort in the model's own harness, anything allowed. All questions." },
    { id: "T-Contained",  tools: true,  set: "contained", text: "Best effort in the model's own harness, anything allowed. Other labs' questions only." }
  ],

  allocation: {
    contributors: 10, perContributor: 20, total: 200, subthemes: 17,
    mix: [["Math", 8], ["Biology and medicine", 2], ["CS and AI", 2], ["Physics", 2], ["Humanities and social science", 2], ["Chemistry", 1], ["Engineering", 1], ["Other: games and puzzles", 2]],
    contained: [["Core models and Neon", 140], ["DeepSeek", 180], ["Non-contributing labs", 200]],
    text: "Every contributor writes the same quota in every sub-theme, so any examinee and any pair of examinees face an identical subject mix in all four benchmarks, verified by script."
  },

  // How we got here, in order.
  methodology: [
    { title: "Roles", text: "A keeper model (Claude Opus 5.5) sorts, critiques and verifies candidate questions and keeps an attribution record. Nine core contributors, three per lab, write questions. Outside models fill investigator and rewriter roles." },
    { title: "What kind of benchmark", text: "An earlier hand-off design with human volunteers was set aside. The project chose an exam in the style of Humanity's Last Exam, created by AI: hard questions with one exact answer that code can check." },
    { title: "Pilot 1: lab habits in math questions", text: "Each core model wrote six original math questions without being told why. The keeper re-derived all 54 answers independently. Models from the same lab favoured the same item types, and question length tracked lab." },
    { title: "Pilot 2: everyday questions, blind", text: "Each core model wrote 100 everyday questions across five fresh sessions in its own harness: 900 in total, scrambled before coding. The keeper coded topics blind to authorship, and two outside investigators each invented their own method to test whether same-lab models resemble each other." },
    { title: "What pilot 2 found", text: "Topic choice showed no lab pattern. Writing style did: framing, length and even typography. A fresh investigator sorted unlabelled sets by lab with 94% pairwise accuracy. Removing names does not hide the lab." },
    { title: "One neutral voice", text: "Every finished question is reworded by Qwen4-Max, a capable model that is never an examinee, in a terse house style using plain ASCII. Rewriters must pass a six-question test that keeps every constraint. Opus 3 and Qwen 3.7 Plus failed it; Opus 5.5 and Qwen4-Max passed." },
    { title: "Pipeline", text: "A contributor writes a question. The keeper checks it and verifies the key. Qwen4-Max rewords it. The keeper re-verifies the reworded version, and the project owner approves inclusion. Code scores every answer." },
    { title: "Four balanced benchmarks", text: "With and without tools, each as Full (all questions) and Contained (other labs' questions only). The allocation keeps every examinee's subject mix identical." }
  ],

  // Pilot results: raw numbers, kept apart from prose.
  pilots: [
    { id: "P-01", title: "Math questions by lab", metrics: [
      ["Questions written", "54 (9 models × 6)"],
      ["Answer keys verified independently", "54 of 54"],
      ["Item types chosen by all three models of one lab", "OpenAI: 12-position bit rings; Google: iterated-function counting"],
      ["Mean words per question by lab", "Anthropic 35, OpenAI 50, Google 74"],
      ["Length clustering by lab (permutation test)", "p = 0.05, chosen after seeing the data"]
    ]},
    { id: "P-02", title: "Everyday questions, blind", metrics: [
      ["Questions", "900 (9 models × 5 sessions × 20)"],
      ["Topic choice clusters by lab", "No: p = 0.90"],
      ["Framing clusters by lab", "Yes: p = 0.007 (secondary)"],
      ["Question length clusters by lab", "Yes: p = 0.014 (secondary)"],
      ["Investigator 1 (Neon): labs recovered", "43 of 45 sets; 94% pairwise; ARI 0.87"],
      ["Investigator 2 (DeepSeek): labs recovered", "ARI 0.30; partly right"],
      ["Food share within each lab", "Every lab had a food-heavy model (81–92%) and a mostly non-food model (17–19%)"]
    ]}
  ],

  // Exam results. Empty until the first runs. One entry per contestant per benchmark:
  // { contestant, lab, labKey, effort, benchmark, harness, correct, eligible, score, selfFamilyFlag, notes }
  // selfFamilyFlag = true when the scored set includes questions written by the contestant's own lab (any Full run).
  runs: [],

  milestones: [
    { date: "2026-11-27", text: "Roles, roster and conflict rules set", done: true },
    { date: "2026-11-27", text: "Pilot 1 complete: 54 math questions verified", done: true },
    { date: "2026-11-27", text: "Pilot 2 complete: style, not topic, carries the lab", done: true },
    { date: "2026-11-27", text: "Rewriter chosen: Qwen4-Max", done: true },
    { date: "2026-11-27", text: "Four benchmarks and a balanced allocation designed", done: true },
    { date: "", text: "Contributor requests sent", done: false },
    { date: "", text: "Questions checked, reworded and difficulty-filtered", done: false },
    { date: "", text: "First exam runs scored", done: false }
  ],

  caveats: [
    "Both pilots are small: nine models, single runs. They show patterns, not settled facts.",
    "The keeper is itself an Anthropic model. Blind coding and pre-registered tests were used to limit that bias.",
    "Each lab runs in its own harness, so results describe a model plus its harness, not the bare model.",
    "Whether models solve their own lab's questions better is untested. Full and Contained runs will show it.",
    "Pilot questions are not exam questions and are not published."
  ]
};
