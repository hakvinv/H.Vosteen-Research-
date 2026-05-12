// Interactive playground for the four-mechanism burnout model.
// Panels mirror the figures in code/burnout/figures.py:
//   1. Observer-relative accounting   (ρᴾ vs ρᶠ)
//   2. Hedonic decay                  (m(t) → ρᴾ(t))
//   3. Population sigmoid B(t)        (heterogeneous drift + threshold)
//   4. Optimal stopping (Charnov MVT) (u(t) vs A(T), intersection t*)

// ---- math helpers --------------------------------------------------

function erf(x) {
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

// Hedonic-decay multiplier and its definite integral
function mFunc(t, mInf, tau) {
  return mInf + (1 - mInf) * Math.exp(-t / tau);
}
function mIntegral(T, mInf, tau) {
  // ∫_0^T m(τ) dτ
  return mInf * T + (1 - mInf) * tau * (1 - Math.exp(-T / tau));
}

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

function dot(ctx, w, h, pad, xR, yR, xv, yv, color, radius) {
  const xPx = pad.l + ((xv - xR[0]) / (xR[1] - xR[0])) * (w - pad.l - pad.r);
  const yPx = h - pad.b - ((yv - yR[0]) / (yR[1] - yR[0])) * (h - pad.t - pad.b);
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.arc(xPx, yPx, radius || 5, 0, Math.PI * 2);
  ctx.fill();
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

// ---- panel 2: hedonic decay ---------------------------------------

function setupHedonic() {
  const $ = id => document.getElementById(id);
  const r0El = $('hd-rho0'), mInfEl = $('hd-minf'), tauEl = $('hd-tau');
  const rsEl = $('hd-rstar'), tEl = $('hd-t');
  const ctx = $('hd-canvas').getContext('2d');
  const W = $('hd-canvas').width, H = $('hd-canvas').height;

  function update() {
    const rho0 = +r0El.value, mInf = +mInfEl.value, tau = +tauEl.value;
    const rStar = +rsEl.value, tObs = +tEl.value;
    $('hd-rho0-val').textContent  = rho0.toFixed(2);
    $('hd-minf-val').textContent  = mInf.toFixed(2);
    $('hd-tau-val').textContent   = tau.toFixed(0);
    $('hd-rstar-val').textContent = rStar.toFixed(2);
    $('hd-t-val').textContent     = tObs.toFixed(0);

    const mt = mFunc(tObs, mInf, tau);
    const rhoT = rho0 / mt;
    const rhoInf = rho0 / mInf;
    $('hd-mt').textContent   = mt.toFixed(2);
    $('hd-rho').textContent  = rhoT.toFixed(2);
    $('hd-rinf').textContent = rhoInf.toFixed(2);

    // Collapse time: rho0 / m(t) = rStar  ⇒  m(t) = rho0 / rStar
    const mTarget = rho0 / rStar;
    let tCol = NaN;
    if (rho0 >= rStar) {
      tCol = 0;
    } else if (mInf < mTarget && mTarget <= 1) {
      // m(t) = mInf + (1-mInf) e^{-t/tau} = mTarget
      tCol = -tau * Math.log((mTarget - mInf) / (1 - mInf));
    }
    const colEl = $('hd-collapse');
    const colDiv = colEl.parentElement;
    colDiv.classList.remove('warn', 'danger');
    if (rho0 >= rStar) {
      colEl.textContent = 'already past';
      colDiv.classList.add('danger');
    } else if (isFinite(tCol) && tCol > 0) {
      colEl.textContent = tCol.toFixed(0) + ' wk';
      colDiv.classList.add('warn');
    } else {
      colEl.textContent = 'never (ρ∞ ≤ ρ*)';
    }

    // Plot ρᴾ(t) over t ∈ [0, tMax]
    const tMax = 200;
    const N = 240;
    const xs = [], ys = [];
    let yMax = Math.max(rStar * 1.4, rhoInf * 1.1, 1.5);
    yMax = Math.min(yMax, 4);
    for (let i = 0; i <= N; i++) {
      const ti = (i / N) * tMax;
      const m = mFunc(ti, mInf, tau);
      xs.push(ti);
      ys.push(rho0 / m);
    }

    const c = colors();
    const pad = { l: 50, r: 20, t: 20, b: 40 };
    drawAxes(ctx, W, H, pad, [0, tMax], [0, yMax], 't (weeks)', 'ρᴾ(t)');
    hLine(ctx, W, H, pad, [0, tMax], [0, yMax], rStar, c.danger, 'ρ* = ' + rStar.toFixed(2));
    if (rhoInf > 0 && rhoInf < yMax) {
      hLine(ctx, W, H, pad, [0, tMax], [0, yMax], rhoInf, c.dim, 'ρ∞ = ' + rhoInf.toFixed(2));
    }
    if (rho0 > 0 && rho0 < yMax) {
      hLine(ctx, W, H, pad, [0, tMax], [0, yMax], rho0, c.accent2, 'ρ₀ = ' + rho0.toFixed(2));
    }
    plotLine(ctx, W, H, pad, [0, tMax], [0, yMax], xs, ys, c.accent, 2);

    if (isFinite(tCol) && tCol > 0 && tCol < tMax) {
      dot(ctx, W, H, pad, [0, tMax], [0, yMax], tCol, rStar, c.danger, 5);
    }
    if (tObs >= 0 && tObs <= tMax && rhoT < yMax) {
      dot(ctx, W, H, pad, [0, tMax], [0, yMax], tObs, rhoT, c.accent2, 5);
    }
  }

  for (const el of [r0El, mInfEl, tauEl, rsEl, tEl]) el.addEventListener('input', update);
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

    dot(ctx, W, H, pad, [0, tMax], [0, 1], t, B, c.accent2, 5);
  }

  for (const el of [m0El, dEl, msEl, sEl, ssEl, tEl]) {
    el.addEventListener('input', update);
  }
  update();
}

// ---- panel 4: optimal stopping (Charnov MVT) ----------------------

function setupOptimalStopping() {
  const $ = id => document.getElementById(id);
  const u0El = $('os-u0'), mInfEl = $('os-minf'), tauEl = $('os-tau'), sEl = $('os-s');
  const ctx = $('os-canvas').getContext('2d');
  const W = $('os-canvas').width, H = $('os-canvas').height;

  function update() {
    const u0 = +u0El.value, mInf = +mInfEl.value, tau = +tauEl.value, s = +sEl.value;
    $('os-u0-val').textContent   = u0.toFixed(2);
    $('os-minf-val').textContent = mInf.toFixed(2);
    $('os-tau-val').textContent  = tau.toFixed(0);
    $('os-s-val').textContent    = s.toFixed(0);

    const u = (t) => u0 * mFunc(t, mInf, tau);
    const A = (T) => T > 0 ? u0 * mIntegral(T, mInf, tau) / (s + T) : 0;
    const f = (T) => u(T) - A(T);

    // Find t* via bisection. f(eps) > 0, f(large) < 0 typically.
    let lo = 0.01, hi = Math.max(tau * 8, 200);
    let fLo = f(lo), fHi = f(hi);
    let tStar = NaN, uStar = NaN, aStar = NaN;
    if (fLo > 0 && fHi < 0) {
      for (let i = 0; i < 80; i++) {
        const mid = 0.5 * (lo + hi);
        const fm = f(mid);
        if (fm > 0) { lo = mid; fLo = fm; } else { hi = mid; fHi = fm; }
        if (hi - lo < 1e-4) break;
      }
      tStar = 0.5 * (lo + hi);
      uStar = u(tStar);
      aStar = A(tStar);
    }

    const status = $('os-status');
    status.classList.remove('ok', 'warn', 'danger');
    if (isFinite(tStar)) {
      $('os-tstar').textContent = tStar.toFixed(0) + ' wk';
      $('os-ustar').textContent = uStar.toFixed(3);
      $('os-astar').textContent = aStar.toFixed(3);
      if (tStar < 26) {
        status.textContent = 'Quit window opens fast — short patches, high search cost would dominate.';
        status.classList.add('warn');
      } else if (tStar > 156) {
        status.textContent = 'Patch is rich — staying long is rational.';
        status.classList.add('ok');
      } else {
        status.textContent = 'Optimal quit around year ' + (tStar / 52).toFixed(1) + '.';
        status.classList.add('ok');
      }
    } else {
      $('os-tstar').textContent = '—';
      $('os-ustar').textContent = '—';
      $('os-astar').textContent = '—';
      status.textContent = 'No interior optimum: u(t) and A(t) do not cross in plotted range.';
      status.classList.add('warn');
    }

    // Plot u(t) and A(T) on shared axes
    const tMax = Math.max(tau * 6, isFinite(tStar) ? tStar * 2.2 : 200);
    const N = 240;
    const xs = [], ysU = [], ysA = [];
    for (let i = 0; i <= N; i++) {
      const ti = (i / N) * tMax;
      xs.push(ti);
      ysU.push(u(ti));
      ysA.push(A(ti));
    }
    const yMax = Math.max(u0, ...ysU, ...ysA) * 1.1;

    const c = colors();
    const pad = { l: 50, r: 80, t: 20, b: 40 };
    drawAxes(ctx, W, H, pad, [0, tMax], [0, yMax], 't (weeks)', 'rate');
    plotLine(ctx, W, H, pad, [0, tMax], [0, yMax], xs, ysU, c.accent, 2);
    plotLine(ctx, W, H, pad, [0, tMax], [0, yMax], xs, ysA, c.accent2, 2);

    // Legend
    ctx.font = '11px -apple-system, BlinkMacSystemFont, sans-serif';
    ctx.textBaseline = 'middle'; ctx.textAlign = 'left';
    ctx.fillStyle = c.accent;
    ctx.fillRect(W - pad.r + 8, pad.t + 6, 16, 2);
    ctx.fillStyle = c.text;
    ctx.fillText('u(t)', W - pad.r + 28, pad.t + 7);
    ctx.fillStyle = c.accent2;
    ctx.fillRect(W - pad.r + 8, pad.t + 22, 16, 2);
    ctx.fillStyle = c.text;
    ctx.fillText('A(T)', W - pad.r + 28, pad.t + 23);

    if (isFinite(tStar) && tStar < tMax) {
      // Vertical line at t*
      const xPx = pad.l + (tStar / tMax) * (W - pad.l - pad.r);
      ctx.strokeStyle = c.danger;
      ctx.setLineDash([4, 4]);
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(xPx, pad.t);
      ctx.lineTo(xPx, H - pad.b);
      ctx.stroke();
      ctx.setLineDash([]);
      // Dot at intersection
      dot(ctx, W, H, pad, [0, tMax], [0, yMax], tStar, uStar, c.danger, 5);
      // Label
      ctx.fillStyle = c.danger;
      ctx.font = '11px ui-monospace, Menlo, monospace';
      ctx.textAlign = 'left'; ctx.textBaseline = 'bottom';
      ctx.fillText('t* = ' + tStar.toFixed(0) + ' wk', xPx + 6, pad.t + 12);
    }
  }

  for (const el of [u0El, mInfEl, tauEl, sEl]) el.addEventListener('input', update);
  update();
}

// ---- bootstrap -----------------------------------------------------

document.addEventListener('DOMContentLoaded', () => {
  setupObserver();
  setupHedonic();
  setupPopulation();
  setupOptimalStopping();
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener?.('change', () => {
      document.querySelectorAll('input[type="range"]').forEach(el => {
        el.dispatchEvent(new Event('input'));
      });
    });
  }
});
