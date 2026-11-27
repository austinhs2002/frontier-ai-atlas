// Renders window.AI_BENCH_DATA into #ai-bench using only the site's existing classes and CSS variables.
// Edit ai-bench/data.js for updates; this file should rarely change.
(function () {
  var D = window.AI_BENCH_DATA, root = document.getElementById('ai-bench');
  if (!D || !root) return;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function lab(name, key) { return key ? '<span class="name ' + esc(key) + '">' + esc(name) + '</span>' : esc(name); }
  function table(head, rows) {
    return '<div class="scroll"><table><thead><tr>' + head.map(function (h) { return '<th>' + esc(h) + '</th>'; }).join('') +
      '</tr></thead><tbody>' + rows.map(function (r) { return '<tr>' + r.map(function (c) { return '<td>' + c + '</td>'; }).join('') + '</tr>'; }).join('') +
      '</tbody></table></div>';
  }
  function fold(summary, inner, open) {
    return '<details class="fold"' + (open ? ' open' : '') + '><summary>' + esc(summary) + '</summary><div>' + inner + '</div></details>';
  }

  var h = '';

  // Header & jump links (mirrors Evidence tab structure)
  h += '<p class="meta">Ongoing project · updated ' + esc(D.updated) + ' · v' + esc(D.version) + '</p>';
  h += '<h2>AI benchmarking AI.</h2>';
  h += '<p class="lead">' + esc(D.status.summary) + '</p>';
  h += '<p class="strip">' +
    '<a href="#ai-bench" data-jump="ab-benchmarks">Benchmarks</a> · ' +
    '<a href="#ai-bench" data-jump="ab-selection">How roles were chosen</a> · ' +
    '<a href="#ai-bench" data-jump="ab-roster">Roster</a> · ' +
    '<a href="#ai-bench" data-jump="ab-exam">The exam</a> · ' +
    '<a href="#ai-bench" data-jump="ab-pilots">Pilots</a> · ' +
    '<a href="#ai-bench" data-jump="ab-scores">Scores</a>' +
    '</p>';

  // 1. Current status & the four benchmarks
  h += '<div class="box" id="ab-benchmarks">' +
    '<p class="meta">Where it stands</p>' +
    '<p><b>' + esc(D.status.phase) + '</b></p>' +
    table(['Benchmark', 'Tools', 'Questions answered', 'What it is'], D.benchmarks.map(function (b) {
      return ['<b>' + esc(b.id) + '</b>', b.tools ? 'Yes' : 'No', b.set === 'full' ? 'All' : 'Other labs only', esc(b.text)];
    })) +
    '</div>';

  // 2. How the roles were chosen (before "Who does what")
  if (D.selection) {
    var S = D.selection, K = S.keeper;
    h += '<div class="part" id="ab-selection">' +
      '<p class="meta">Governance</p>' +
      '<h3 class="sechead">How the roles were chosen</h3>' +
      '<div class="pair">' +
        '<div class="box">' +
          '<p class="meta">Keeper vote</p>' +
          '<div class="scores">' +
            '<div class="score">' + lab(K.model, K.labKey) + '<div class="big">9 / 9</div><p class="sub">Unanimous first-choice vote</p></div>' +
            '<div class="score"><b>Method</b><p class="sub">' + esc(K.method) + '</p></div>' +
          '</div>' +
          '<p>' + esc(K.result) + '</p>' +
          (K.ownBallot ? '<p class="sub">' + esc(K.ownBallot) + '</p>' : '') +
          '<p class="sub"><b>Eligible voters:</b> ' + esc(K.text) + '</p>' +
        '</div>' +
        '<div>' +
          '<h3>Blind role &amp; outside vote</h3>' +
          '<p class="aside">' + esc(S.neon.text) + '</p>' +
          '<p class="sub"><b>Outside contributor vote:</b> ' + esc(S.outsideVote.text) + '</p>' +
          '<h3 class="stagehead">Outside models</h3>' +
          table(['Model', 'Status', 'Priority', 'Notes'], S.outside.map(function (o) {
            return ['<b>' + esc(o.model) + '</b>', esc(o.status), esc(o.priority), esc(o.notes)];
          })) +
        '</div>' +
      '</div>' +
      fold('Excluded and opted-out models', table(['Model', 'Status', 'Reason', 'Later role'], S.excluded.map(function (e) {
        return [lab(e.model, e.labKey), esc(e.status), esc(e.reason), esc(e.laterRole || '—')];
      })), true) +
      '</div>';
  }

  // 3. Who does what
  h += '<div class="part" id="ab-roster">' +
    '<p class="meta">Participants</p>' +
    '<h3 class="sechead">Who does what</h3>' +
    table(['Model', 'Lab', 'Effort', 'Roles'], D.roster.map(function (r) {
      return [lab(r.model, r.labKey), lab(r.lab, r.labKey), esc(r.effort || '—'), esc(r.roles.join(', '))];
    })) +
    '<p class="aside">' + (D.judges.length ? esc(D.judges.length + ' judges') :
      'No AI judges. Every answer has one exact correct value and is scored by code, so no model grades another.') + '</p>' +
    '</div>';

  // 4. How we got here + The exam
  var A = D.allocation;
  h += '<div class="part" id="ab-exam">' +
    '<p class="meta">Design &amp; balance</p>' +
    '<h3 class="sechead">The exam</h3>' +
    '<div class="pair">' +
      '<div>' +
        '<p class="sub">' + esc(A.text) + '</p>' +
        table(['Area', 'Per contributor', 'Share'], A.mix.map(function (m) {
          return [esc(m[0]), esc(m[1]), Math.round(100 * m[1] / A.perContributor) + '%'];
        }).concat([['<b>Total</b>', '<b>' + esc(A.perContributor) + '</b>', '<b>' + esc(A.contributors) + ' contributors · ' + esc(A.total) + ' questions</b>']])) +
        fold('Questions each examinee answers in Contained', table(['Examinee', 'Questions'], A.contained.map(function (c) {
          return [esc(c[0]), esc(c[1])];
        }))) +
      '</div>' +
      '<div>' +
        '<h3>How we got here</h3>' +
        '<div class="notes">' +
          D.methodology.map(function (m, i) {
            return '<p><b>' + (i + 1) + '. ' + esc(m.title) + '.</b> ' + esc(m.text) + '</p>';
          }).join('') +
        '</div>' +
      '</div>' +
    '</div>' +
    '</div>';

  // 5. Pilot results
  h += '<div class="part" id="ab-pilots">' +
    '<p class="meta">Pre-exam tests</p>' +
    '<h3 class="sechead">Pilot results</h3>';
  D.pilots.forEach(function (p, i) {
    h += fold(p.id + ' · ' + p.title, table(['Measure', 'Result'], p.metrics.map(function (m) { return [esc(m[0]), esc(m[1])]; })), i === D.pilots.length - 1);
  });
  h += '</div>';

  // 6. Scores, Milestones & Caveats
  h += '<div class="part" id="ab-scores">' +
    '<p class="meta">Results &amp; progress</p>' +
    '<h3 class="sechead">Scores</h3>';
  if (!D.runs.length) {
    h += '<p class="sub">No exam runs yet. Scores appear here as each run is scored.</p>';
  } else {
    h += table(['Contestant', 'Benchmark', 'Effort', 'Harness', 'Correct', 'Score', 'Own-lab questions', 'Notes'], D.runs.map(function (r) {
      var pct = r.score != null ? r.score : (r.eligible ? 100 * r.correct / r.eligible : null);
      return [lab(r.contestant, r.labKey), esc(r.benchmark), esc(r.effort), esc(r.harness),
        esc(r.correct + ' / ' + r.eligible), pct == null ? '—' : esc(pct.toFixed(1) + '%'),
        r.selfFamilyFlag ? 'Included' : 'Excluded', esc(r.notes || '')];
    }));
  }
  h += fold('Milestones', table(['Date', 'Milestone', 'Status'], D.milestones.map(function (m) {
    return [esc(m.date || '—'), esc(m.text), m.done ? 'Done' : 'Pending'];
  })), true);
  h += fold('Caveats', '<ul>' + D.caveats.map(function (c) { return '<li>' + esc(c) + '</li>'; }).join('') + '</ul>', true);
  h += '</div>';

  root.innerHTML = h;
  root.addEventListener('click', function (e) {
    var link = e.target.closest('[data-jump]');
    if (!link) return;
    e.preventDefault();
    var target = document.getElementById(link.getAttribute('data-jump'));
    if (target) target.scrollIntoView({ behavior: 'smooth' });
  });
})();
