// Renders window.AI_BENCH_DATA into #ai-bench using only the site's existing classes and CSS variables.
// In-place sub-tabs swap panels without pushing content down the page.
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

  // Panel 1: Overview & Scores (compact landing view)
  function panelOverview() {
    var s = '<div class="box">' +
      '<p class="meta">Where it stands</p>' +
      '<p><b>' + esc(D.status.phase) + '</b></p>' +
      table(['Benchmark', 'Tools', 'Questions answered', 'What it is'], D.benchmarks.map(function (b) {
        return ['<b>' + esc(b.id) + '</b>', b.tools ? 'Yes' : 'No', b.set === 'full' ? 'All' : 'Other labs only', esc(b.text)];
      })) +
      '</div>';

    s += '<h3 class="stagehead">Scores</h3>';
    if (!D.runs.length) {
      s += '<p class="sub">No exam runs yet. Scores appear here as each run is scored.</p>';
    } else {
      s += table(['Contestant', 'Benchmark', 'Effort', 'Harness', 'Correct', 'Score', 'Own-lab questions', 'Notes'], D.runs.map(function (r) {
        var pct = r.score != null ? r.score : (r.eligible ? 100 * r.correct / r.eligible : null);
        return [lab(r.contestant, r.labKey), esc(r.benchmark), esc(r.effort), esc(r.harness),
          esc(r.correct + ' / ' + r.eligible), pct == null ? '—' : esc(pct.toFixed(1) + '%'),
          r.selfFamilyFlag ? 'Included' : 'Excluded', esc(r.notes || '')];
      }));
    }
    return s;
  }

  // Panel 2: How the roles were chosen
  function panelSelection() {
    if (!D.selection) return '<p class="sub">No role selection data recorded.</p>';
    var S = D.selection, K = S.keeper;
    return '<div class="pair">' +
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
        (S.neon.advisoryBallot ? '<p class="sub"><b>Post-hoc ballot (Neon):</b> ' + esc(S.neon.advisoryBallot) + '</p>' : '') +
        '<p class="sub"><b>Outside contributor vote:</b> ' + esc(S.outsideVote.text) + '</p>' +
        '<h3 class="stagehead">Outside models</h3>' +
        table(['Model', 'Status', 'Priority', 'Notes'], S.outside.map(function (o) {
          return ['<b>' + esc(o.model) + '</b>', esc(o.status), esc(o.priority), esc(o.notes)];
        })) +
      '</div>' +
    '</div>' +
    '<h3 class="stagehead">Excluded and opted-out models</h3>' +
    table(['Model', 'Status', 'Reason', 'Later role'], S.excluded.map(function (e) {
      return [lab(e.model, e.labKey), esc(e.status), esc(e.reason), esc(e.laterRole || '—')];
    }));
  }

  // Panel 3: Who does what (Roster)
  function panelRoster() {
    return table(['Model', 'Lab', 'Effort', 'Roles'], D.roster.map(function (r) {
      return [lab(r.model, r.labKey), lab(r.lab, r.labKey), esc(r.effort || '—'), esc(r.roles.join(', '))];
    })) +
    '<p class="aside">' + (D.judges.length ? esc(D.judges.length + ' judges') :
      'No AI judges. Every answer has one exact correct value and is scored by code, so no model grades another.') + '</p>';
  }

  // Panel 4: The exam & How we got here
  function panelExam() {
    var A = D.allocation;
    return '<div class="pair">' +
      '<div>' +
        '<h3>The exam</h3>' +
        '<p class="sub">' + esc(A.text) + '</p>' +
        table(['Area', 'Per contributor', 'Share'], A.mix.map(function (m) {
          return [esc(m[0]), esc(m[1]), Math.round(100 * m[1] / A.perContributor) + '%'];
        }).concat([['<b>Total</b>', '<b>' + esc(A.perContributor) + '</b>', '<b>' + esc(A.contributors) + ' contributors · ' + esc(A.total) + ' questions</b>']])) +
        '<h3 class="stagehead">Questions in Contained</h3>' +
        table(['Examinee', 'Questions'], A.contained.map(function (c) {
          return [esc(c[0]), esc(c[1])];
        })) +
      '</div>' +
      '<div>' +
        '<h3>How we got here</h3>' +
        '<div class="notes">' +
          D.methodology.map(function (m, i) {
            return '<p><b>' + (i + 1) + '. ' + esc(m.title) + '.</b> ' + esc(m.text) + '</p>';
          }).join('') +
        '</div>' +
      '</div>' +
    '</div>';
  }

  // Panel 5: Pilot results (side-by-side pair)
  function panelPilots() {
    return '<div class="pair">' + D.pilots.map(function (p) {
      return '<div>' +
        '<p class="meta">' + esc(p.id) + '</p>' +
        '<h3>' + esc(p.title) + '</h3>' +
        table(['Measure', 'Result'], p.metrics.map(function (m) { return [esc(m[0]), esc(m[1])]; })) +
      '</div>';
    }).join('') + '</div>';
  }

  // Panel 6: Milestones & Caveats
  function panelProgress() {
    return '<div class="pair">' +
      '<div>' +
        '<h3>Milestones</h3>' +
        table(['Date', 'Milestone', 'Status'], D.milestones.map(function (m) {
          return [esc(m.date || '—'), esc(m.text), m.done ? 'Done' : 'Pending'];
        })) +
      '</div>' +
      '<div>' +
        '<h3>Caveats</h3>' +
        '<div class="notes">' + D.caveats.map(function (c) { return '<p class="aside">' + esc(c) + '</p>'; }).join('') + '</div>' +
      '</div>' +
    '</div>';
  }

  var tabs = [
    ['Overview & scores', panelOverview],
    ['How roles were chosen', panelSelection],
    ['Who does what', panelRoster],
    ['Exam & method', panelExam],
    ['Pilots', panelPilots],
    ['Milestones & caveats', panelProgress]
  ];

  root.innerHTML =
    '<p class="meta">Ongoing project · updated ' + esc(D.updated) + ' · v' + esc(D.version) + '</p>' +
    '<h2>AI benchmarking AI.</h2>' +
    '<p class="lead">' + esc(D.status.summary) + '</p>' +
    '<div class="choices" id="abTabs" role="tablist" aria-label="AI Bench sections">' +
      tabs.map(function (t, i) {
        return '<button type="button" role="tab" data-ab="' + i + '" aria-pressed="' + (i === 0) + '" aria-selected="' + (i === 0) + '">' + esc(t[0]) + '</button>';
      }).join('') +
    '</div>' +
    '<div id="abPanel" role="tabpanel"></div>';

  var tabBar = document.getElementById('abTabs');
  var panel = document.getElementById('abPanel');

  function openTab(idx) {
    var btns = tabBar.querySelectorAll('button[data-ab]');
    for (var i = 0; i < btns.length; i++) {
      var active = i === idx;
      btns[i].setAttribute('aria-pressed', active);
      btns[i].setAttribute('aria-selected', active);
    }
    panel.innerHTML = tabs[idx][1]();
  }

  tabBar.addEventListener('click', function (e) {
    var b = e.target.closest('button[data-ab]');
    if (!b) return;
    openTab(parseInt(b.getAttribute('data-ab'), 10));
  });

  openTab(0);
})();
