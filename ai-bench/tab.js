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
  function lab(name, key) { return key ? '<span class="' + esc(key) + '">' + esc(name) + '</span>' : esc(name); }
  function table(head, rows) {
    return '<div class="scroll"><table><thead><tr>' + head.map(function (h) { return '<th>' + esc(h) + '</th>'; }).join('') +
      '</tr></thead><tbody>' + rows.map(function (r) { return '<tr>' + r.map(function (c) { return '<td>' + c + '</td>'; }).join('') + '</tr>'; }).join('') +
      '</tbody></table></div>';
  }
  function fold(summary, inner, open) {
    return '<details class="fold"' + (open ? ' open' : '') + '><summary>' + esc(summary) + '</summary><div>' + inner + '</div></details>';
  }

  var h = '';
  h += '<p class="meta">Ongoing project · updated ' + esc(D.updated) + ' · v' + esc(D.version) + '</p>';
  h += '<h2>AI benchmarking AI.</h2>';
  h += '<p class="lead">' + esc(D.status.summary) + '</p>';

  h += '<div class="box"><p class="meta">Where it stands</p><p><b>' + esc(D.status.phase) + '</b></p>' +
    table(['Benchmark', 'Tools', 'Questions answered', 'What it is'], D.benchmarks.map(function (b) {
      return [esc(b.id), b.tools ? 'Yes' : 'No', b.set === 'full' ? 'All' : 'Other labs only', esc(b.text)];
    })) + '</div>';

  h += '<h3 class="stagehead">How we got here</h3>';
  D.methodology.forEach(function (m, i) {
    h += '<p><b>' + (i + 1) + '. ' + esc(m.title) + '.</b> ' + esc(m.text) + '</p>';
  });

  var A = D.allocation;
  h += '<h3 class="stagehead">The exam</h3><p class="sub">' + esc(A.text) + '</p>' +
    table(['Area', 'Questions per contributor', 'Share'], A.mix.map(function (m) {
      return [esc(m[0]), esc(m[1]), Math.round(100 * m[1] / A.perContributor) + '%'];
    }).concat([['<b>Total</b>', '<b>' + esc(A.perContributor) + '</b>', '<b>' + esc(A.contributors) + ' contributors · ' + esc(A.total) + ' questions</b>']])) +
    fold('Questions each examinee answers in Contained', table(['Examinee', 'Questions'], A.contained.map(function (c) { return [esc(c[0]), esc(c[1])]; })));

  h += '<h3 class="stagehead">Who does what</h3>' +
    table(['Model', 'Lab', 'Effort', 'Roles'], D.roster.map(function (r) {
      return [lab(r.model, r.labKey), lab(r.lab, r.labKey), esc(r.effort || '—'), esc(r.roles.join(', '))];
    }));
  h += '<p class="aside">' + (D.judges.length ? esc(D.judges.length + ' judges') :
    'No AI judges. Every answer has one exact correct value and is scored by code, so no model grades another.') + '</p>';

  h += '<h3 class="stagehead">Pilot results</h3>';
  D.pilots.forEach(function (p, i) {
    h += fold(p.id + ' · ' + p.title, table(['Measure', 'Result'], p.metrics.map(function (m) { return [esc(m[0]), esc(m[1])]; })), i === D.pilots.length - 1);
  });

  h += '<h3 class="stagehead">Scores</h3>';
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

  h += '<h3 class="stagehead">Milestones</h3>' + table(['Date', 'Milestone', 'Status'], D.milestones.map(function (m) {
    return [esc(m.date || '—'), esc(m.text), m.done ? 'Done' : 'Pending'];
  }));

  h += fold('Caveats', '<ul>' + D.caveats.map(function (c) { return '<li>' + esc(c) + '</li>'; }).join('') + '</ul>', true);

  root.innerHTML = h;
})();
