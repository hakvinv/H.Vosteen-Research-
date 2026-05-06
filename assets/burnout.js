// Interactive playground for the Burnout v2 paper.
// Three panels mirror the three figures in code/burnout/figures.py:
//   1. Observer-relative split  (rho^P vs rho^F)
//   2. Drift dynamic            (rho(t) trajectory + steady state)
//   3. Population sigmoid B(t)  (heterogeneous drift + threshold)

// ---- math helpers --------------------------------------------------

function erf(x) {
  // Abramowitz & Stegun 7.1.26
  const sign = x < 0 ? -1 : 1;
  x = Math.abs(x);
  const a1 = 0.254829592, a2 = -0.284496736, a3 = 1.421413741,
        a4 = -1.453152027, a5 = 1.061405429, p = 0.3275911;
  const t = 1.0 / (1.0 + p * x);
  const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1)
                  * t * Math.exp(-x * x);
  return sign * y;
}
function phi(x) { return 0.5 * (1 + erf(x / Math.SQRT2)); }

// ---- canvas helpers ------------------------------------------------

function colors() {
  const cs = getComputedStyle(document.documentElement);
  return {
    text:    cs.getPropertyValue('--text').trim(),
    dim:     cs.getPropertyValue('--text-dim').trim(),
    accent:  cs.getPropertyValue('--accent').trim(),
    accent2: cs.getPropertyValue('--accent-2').trim(),
    border:  cs.getPropertyValue('--border').trim(),
    danger:  cs.getPropertyValue('--danger').trim(),
  };
}

function fmt(v) {
  if (!isFinite(v)) return '∞';
  if (Math.abs(v) >= 100) return v.toFixed(0);
  if (Math.abs(v) >= 10)  return v.toFixed(1);
  return v.toFixed(2);
}

function drawAxes(ctx, w, h, pad, xR, yR, xLabel, yLabel) {
  const c = colors();
  ctx.clearRect(0, 0, w, h);
  ctx.strokeStyle = c.border;
  ctx.fillStyle = c.dim;
  ctx.font = '11px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
  ctx.lineWidth = 1;

  ctx.beginPath();
  ctx.moveTo(pad.l, pad.t);
  ctx.lineTo(pad.l, h - pad.b);
  ctx.lineTo(w - pad.r, h - pad.b);
  ctx.stroke();

  const xTicks = 5, yTicks = 4;
  ctx.textAlign = 'center'; ctx.textBaseline = 'top';
  for (let i = 0; i <= xTicks; i++) {
    const t = i / xTicks;
    const x = pad.l + t * (w - pad.l - pad.r);
    const xv = xR[0] + t * (xR[1] - xR[0]);
    ctx.fillText(fmt(xv), x, h - pad.b + 4);
  }
  ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
  for (let i = 0; i <= yTicks; i++) {
    const t = i / yTicks;
    const y = h - pad.b - t * (h - pad.t - pad.b);
    const yv = yR[0] + t * (yR[1] - yR[0]);
    ctx.fillText(fmt(yv), pad.l - 6, y);
  }

  ctx.fillStyle = c.text;
  ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
  ctx.fillText(xLabel, pad.l + (w - pad.l - pad.r) / 2, h - 2);
  ctx.save();
  ctx.translate(12, pad.t + (h - pad.t - pad.b) / 2);
  ctx.rotate(-Math.PI / 2);
  ctx.textAlign = 'center';
  ctx.fillText(yLabel, 0, 0);
  ctx.restore();
}

function plotLine(ctx, w, h, pad, xR, yR, xs, ys, color, lw) {
  ctx.strokeStyle = color;
  ctx.lineWidth = lw || 2;
  ctx.beginPath();
  for (let i = 0; i < xs.length; i++) {
    const x = pad.l + ((xs[i] - xR[0]) / (xR[1] - xR[0])) * (w - pad.l - pad.r);
    const y = h - pad.b - ((ys[i] - yR[0]) / (yR[1] - yR[0])) * (h - pad.t - pad.b);
    if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  }
  ctx.stroke();
}

function hLine(ctx, w, h, pad, xR, yR, yVal, color, label) {
  ctx.strokeStyle = color;
  ctx.lineWidth = 1;
  ctx.setLineDash([4, 4]);
  ctx.beginPath();
  const y = h - pad.b - ((yVal - yR[0]) / (yR[1] - yR[0])) * (h - pad.t - pad.b);
  ctx.moveTo(pad.l, y);
  ctx.lineTo(w - pad.r, y);
  ctx.stroke();
  ctx.setLineDash([]);
  if (label) {
    ctx.fillStyle = color;
    ctx.textAlign = 'left'; ctx.textBaseline = 'bottom';
    ctx.font = '11px -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif';
    ctx.fillText(label, pad.l + 6, y - 2);
  }
}

// ---- panel 1: observer-relative split -----------------------------

function setupObserver() {
  const $ = id => document.getElementById(id);
  const aEl = $('obs-a'), bEl = $('obs-b'), fEl = $('obs-f');
  const ctx = $('obs-canvas').getContext('2d');
  const W = $('obs-canvas').width, H = $('obs-canvas').height;

  function update() {
    let a = +aEl.value, b = +bEl.value, f = +fEl.value;
    if (f > a) { f = a; fEl.value = a; }
    $('obs-a-val').textContent = a.toFixed(0);
    $('obs-b-val').textContent = b.toFixed(0);
    $('obs-f-val').textContent = f.toFixed(0);

    const p  = a / b;
    const fr = (a - f) / (b + f);
    $('obs-rhoP').textContent = p.toFixed(2);
    $('obs-rhoF').textContent = fr.toFixed(2);
    $('obs-gap').textContent  = (p - fr).toFixed(2);

    const status = $('obs-status');
    status.classList.remove('ok', 'warn', 'danger');
    if (p > 1.0 && fr <= 1.0) {
      status.textContent = 'Person past collapse threshold; firm dashboard reads green.';
      status.classList.add('warn');
    } else if (p > 1.0) {
      status.textContent = 'Both accountings flag burnout.';
      status.classList.add('danger');
    } else {
      status.textContent = 'Both accountings show healthy.';
      status.classList.add('ok');
    }

    // Bar chart
    const c = colors();
    const pad = { l: 50, r: 20, t: 20, b: 50 };
    const yMax = 2.5;
    drawAxes(ctx, W, H, pad, [0, 1], [0, yMax], '', 'ρ');
    hLine(ctx, W, H, pad, [0, 1], [0, yMax], 1.0, c.dim, 'ρ* = 1');

    const plotH = H - pad.t - pad.b;
    const plotW = W - pad.l - pad.r;
    const barW = plotW * 0.22;
    const xL = pad.l + plotW * 0.22;
    const xR = pad.l + plotW * 0.58;
    const drawBar = (x, val, color, label) => {
      const v = Math.min(val, yMax);
      const barH = (v / yMax) * plotH;
      ctx.fillStyle = color;
      ctx.fillRect(x, H - pad.b - barH, barW, barH);
      ctx.fillStyle = c.text;
      ctx.textAlign = 'center'; ctx.textBaseline = 'top';
      ctx.font = '11px -apple-system, BlinkMacSystemFont, sans-serif';
      ctx.fillText(label, x + barW / 2, H - pad.b + 18);
      ctx.font = '12px ui-monospace, Menlo, monospace';
      ctx.textBaseline = 'bottom';
      ctx.fillText(val.toFixed(2), x + barW / 2, H - pad.b - barH - 4);
    };
    drawBar(xL, p,  c.accent2, 'ρᴾ (person)');
    drawBar(xR, fr, c.accent,  'ρᶠ (firm)');
  }

  aEl.addEventListener('input', update);
  bEl.addEventListener('input', update);
  fEl.addEventListener('input', update);
  update();
}

// ---- panel 2: trajectory ------------------------------------------

function setupTrajectory() {
  const $ = id => document.getElementById(id);
  const aEl = $('tr-alpha'), bEl = $('tr-beta'), rEl = $('tr-r');
  const r0El = $('tr-r0'), rsEl = $('tr-rstar');
  const ctx = $('tr-canvas').getContext('2d');
  const W = $('tr-canvas').width, H = $('tr-canvas').height;

  function update() {
    const alpha = +aEl.value, beta = +bEl.value, r = +rEl.value;
    const rho0 = +r0El.value, rhoStar = +rsEl.value;
    $('tr-alpha-val').textContent = alpha.toFixed(2);
    $('tr-beta-val').textContent  = beta.toFixed(2);
    $('tr-r-val').textContent     = r.toFixed(2);
    $('tr-r0-val').textContent    = rho0.toFixed(2);
    $('tr-rstar-val').textContent = rhoStar.toFixed(2);

    const k = beta * r;
    const rhoSS = k > 1e-9 ? alpha / k : Infinity;
    const tau   = k > 1e-9 ? 1 / k     : Infinity;
    $('tr-ss').textContent  = isFinite(rhoSS) ? rhoSS.toFixed(2) : '∞';
    $('tr-tau').textContent = isFinite(tau)   ? tau.toFixed(1) + ' wk' : '∞';

    const collapseEl = $('tr-collapse');
    const collapseDiv = collapseEl.parentElement;
    collapseDiv.classList.remove('warn', 'danger');
    let tCol = NaN;
    if (rho0 >= rhoStar) {
      collapseEl.textContent = 'already past';
      collapseDiv.classList.add('danger');
    } else if (isFinite(rhoSS) && rhoSS > rhoStar) {
      tCol = -tau * Math.log((rhoStar - rhoSS) / (rho0 - rhoSS));
      collapseEl.textContent = isFinite(tCol) ? tCol.toFixed(1) + ' wk' : '—';
      collapseDiv.classList.add('warn');
    } else if (!isFinite(rhoSS) && alpha > 0) {
      // no recovery, linear growth
      tCol = (rhoStar - rho0) / alpha;
      collapseEl.textContent = isFinite(tCol) && tCol > 0 ? tCol.toFixed(1) + ' wk' : '—';
      collapseDiv.classList.add('warn');
    } else {
      collapseEl.textContent = 'never (ρ_ss ≤ ρ*)';
    }

    // Trajectory: rho(t) = rho_ss + (rho0 - rho_ss) * exp(-t/tau)
    // Fallback (k=0): rho(t) = rho0 + alpha * t (linear)
    const tMax = 100;
    const N = 240;
    const xs = [], ys = [];
    let yMax = 2.5;
    for (let i = 0; i <= N; i++) {
      const t = (i / N) * tMax;
      let rho;
      if (isFinite(rhoSS)) rho = rhoSS + (rho0 - rhoSS) * Math.exp(-t / tau);
      else rho = rho0 + alpha * t;
      xs.push(t); ys.push(rho);
      if (rho > yMax) yMax = rho;
    }
    yMax = Math.min(yMax * 1.05, 6);

    const c = colors();
    const pad = { l: 50, r: 20, t: 20, b: 40 };
    drawAxes(ctx, W, H, pad, [0, tMax], [0, yMax], 't (weeks)', 'ρ(t)');
    hLine(ctx, W, H, pad, [0, tMax], [0, yMax], rhoStar, c.danger, 'ρ* = ' + rhoStar.toFixed(2));
    if (isFinite(rhoSS) && rhoSS > 0 && rhoSS < yMax) {
      hLine(ctx, W, H, pad, [0, tMax], [0, yMax], rhoSS, c.dim, 'ρ_ss = ' + rhoSS.toFixed(2));
    }
    plotLine(ctx, W, H, pad, [0, tMax], [0, yMax], xs, ys, c.accent, 2);

    if (isFinite(tCol) && tCol > 0 && tCol < tMax) {
      const xPx = pad.l + (tCol / tMax) * (W - pad.l - pad.r);
      const yPx = H - pad.b - (rhoStar / yMax) * (H - pad.t - pad.b);
      ctx.fillStyle = c.danger;
      ctx.beginPath(); ctx.arc(xPx, yPx, 5, 0, Math.PI * 2); ctx.fill();
    }
  }

  for (const el of [aEl, bEl, rEl, r0El, rsEl]) el.addEventListener('input', update);
  update();
}

// ---- panel 3: population sigmoid B(t) -----------------------------

function setupPopulation() {
  const $ = id => document.getElementById(id);
  const m0El = $('pop-mu0'),     dEl  = $('pop-delta');
  const msEl = $('pop-mustar'),  sEl  = $('pop-sigma'), ssEl = $('pop-sigmastar');
  const tEl  = $('pop-t');
  const ctx  = $('pop-canvas').getContext('2d');
  const W = $('pop-canvas').width, H = $('pop-canvas').height;

  function update() {
    const mu0 = +m0El.value, delta = +dEl.value, muStar = +msEl.value;
    const sigma = +sEl.value, sigmaStar = +ssEl.value, t = +tEl.value;
    $('pop-mu0-val').textContent       = mu0.toFixed(2);
    $('pop-delta-val').textContent     = delta.toFixed(3);
    $('pop-mustar-val').textContent    = muStar.toFixed(2);
    $('pop-sigma-val').textContent     = sigma.toFixed(2);
    $('pop-sigmastar-val').textContent = sigmaStar.toFixed(2);
    $('pop-t-val').textContent         = t.toFixed(0);

    const denom = Math.sqrt(sigma * sigma + sigmaStar * sigmaStar);
    const B = phi((mu0 + delta * t - muStar) / denom);
    $('pop-b').textContent = (B * 100).toFixed(1) + '%';

    const tInf = Math.abs(delta) > 1e-9 ? (muStar - mu0) / delta : NaN;
    $('pop-tinf').textContent = isFinite(tInf) && tInf >= 0
      ? tInf.toFixed(0) + ' wk' : '—';

    const peak = delta / Math.sqrt(2 * Math.PI * (sigma * sigma + sigmaStar * sigmaStar));
    $('pop-slope').textContent = (peak * 100).toFixed(2) + ' %/wk';

    const c = colors();
    const pad = { l: 50, r: 20, t: 20, b: 40 };
    const tMax = 200;
    const N = 300;
    const xs = [], ys = [];
    for (let i = 0; i <= N; i++) {
      const ti = (i / N) * tMax;
      xs.push(ti);
      ys.push(phi((mu0 + delta * ti - muStar) / denom));
    }
    drawAxes(ctx, W, H, pad, [0, tMax], [0, 1], 't (weeks)', 'B(t)');
    hLine(ctx, W, H, pad, [0, tMax], [0, 1], 0.5, c.dim, 'B = 0.5');
    plotLine(ctx, W, H, pad, [0, tMax], [0, 1], xs, ys, c.accent, 2);

    const xPx = pad.l + (t / tMax) * (W - pad.l - pad.r);
    const yPx = H - pad.b - B * (H - pad.t - pad.b);
    ctx.fillStyle = c.accent2;
    ctx.beginPath(); ctx.arc(xPx, yPx, 5, 0, Math.PI * 2); ctx.fill();
  }

  for (const el of [m0El, dEl, msEl, sEl, ssEl, tEl]) {
    el.addEventListener('input', update);
  }
  update();
}

// ---- bootstrap -----------------------------------------------------

document.addEventListener('DOMContentLoaded', () => {
  setupObserver();
  setupTrajectory();
  setupPopulation();
  // Re-render on color-scheme switch so axes/text pick up new --vars.
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener?.('change', () => {
      // Easiest: just dispatch input on every range to force a redraw.
      document.querySelectorAll('input[type="range"]').forEach(el => {
        el.dispatchEvent(new Event('input'));
      });
    });
  }
});
