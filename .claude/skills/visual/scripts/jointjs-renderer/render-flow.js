import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

// ─── CLI Parsing ───────────────────────────────────────────
const args = process.argv.slice(2);

if (args.length < 2 && !args.includes('--preview')) {
  console.error(`Usage:
  node render-flow.js input.json output.png           # Single PNG
  node render-flow.js input.json --variations dir/    # 4 layout variations
  node render-flow.js input.json --preview            # Open in browser`);
  process.exit(1);
}

const inputPath = args[0];
if (!inputPath || !fs.existsSync(inputPath)) {
  console.error(`Error: Input file not found: ${inputPath}`);
  process.exit(1);
}

const json = JSON.parse(fs.readFileSync(inputPath, 'utf-8'));
const isPreview = args.includes('--preview');
const isVariations = args.includes('--variations');
const outputArg = isVariations ? args[args.indexOf('--variations') + 1] : (isPreview ? null : args[1]);

// ─── SVG Icons ─────────────────────────────────────────────
const ICONS = {
  // Card icons
  route: `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="18" cy="5" r="3"/><circle cx="18" cy="19" r="3"/><circle cx="6" cy="12" r="3"/>
    <path d="M8.59 13.51l6.83 3.98M15.41 6.51l-6.82 3.98"/>
  </svg>`,
  think: `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M9 18h6M10 22h4"/>
    <path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/>
  </svg>`,
  act: `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="10"/>
    <polygon points="10,8 16,12 10,16" fill="#2563eb"/>
  </svg>`,
  result: `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
    <polyline points="14,2 14,8 20,8"/>
    <line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
  </svg>`,
  observe: `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
    <circle cx="12" cy="12" r="3"/>
  </svg>`,
  process: `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="3"/>
    <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
  </svg>`,
  store: `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <ellipse cx="12" cy="5" rx="9" ry="3"/>
    <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
    <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
  </svg>`,

  // Capsule icons
  chat: `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
  </svg>`,
  'chat-check': `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#1e40af" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
    <polyline points="9,11 11,13 15,9"/>
  </svg>`,
  user: `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
    <circle cx="12" cy="7" r="4"/>
  </svg>`,
};

function esc(text) {
  if (!text) return '';
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\n/g, '<br>');
}

// ─── Card HTML Generator ───────────────────────────────────
function renderCard(step, layout) {
  const type = step.type;
  const icon = ICONS[type] || ICONS.process;
  const label = step.num ? `${step.num} ${type.toUpperCase()}` : type.toUpperCase();
  const tag = step.tag ? `<div class="tag">${esc(step.tag)}</div>` : '';

  return `<div class="card ${type}">
    ${icon}
    <div class="content">
      <div class="label">${label}</div>
      <div class="text">${esc(step.text)}</div>
      ${tag}
    </div>
  </div>`;
}

// ─── Arrow Generators ──────────────────────────────────────
function hArrow(blue = false) {
  return `<div class="arrow${blue ? ' blue' : ''}"><div class="shaft"></div></div>`;
}

function vArrow(blue = false) {
  return `<div class="v-arrow${blue ? ' blue' : ''}"><div class="v-shaft"></div></div>`;
}

// ─── Capsule HTML ──────────────────────────────────────────
function renderCapsule(cap, cls) {
  const icon = ICONS[cap.icon] || ICONS.chat;
  return `<div class="cap ${cls}">
    ${icon}
    <div class="title">${esc(cap.title)}</div>
    <div class="desc">${esc(cap.desc)}</div>
  </div>`;
}

// ─── Group HTML ────────────────────────────────────────────
function renderGroup(group, layout) {
  const innerLayout = resolveGroupLayout(group, layout);
  const innerClass = innerLayout === 'grid-2x2' ? 'grid-2x2' : 'inline-row';
  const cards = group.steps.map(s => renderCard(s, layout)).join('\n');

  return `<div class="react-group">
    <div class="group-label">${esc(group.label)}</div>
    <div class="${innerClass}">
      ${cards}
    </div>
  </div>`;
}

function resolveGroupLayout(group, layout) {
  if (layout === 'lr-grid' || layout === 'lr') return 'grid-2x2';
  if (layout === 'tb-inline') return 'inline';
  if (layout === 'tb') return 'grid-2x2';
  // Fallback to JSON-specified layout
  return group.layout === 'grid-2x2' ? 'grid-2x2' : 'inline';
}

// ─── Full Flow HTML ────────────────────────────────────────
function buildFlowHTML(data, layout) {
  const isVertical = layout === 'tb' || layout === 'tb-inline';
  const flowClass = isVertical ? 'flow vertical' : 'flow horizontal';
  const arrowFn = isVertical ? vArrow : hArrow;

  const parts = [];

  // Start capsule
  if (data.start) {
    parts.push(renderCapsule(data.start, 'start'));
    parts.push(arrowFn(false));
  }

  // Steps
  if (data.steps) {
    data.steps.forEach((step, i) => {
      if (i > 0) parts.push(arrowFn(true));

      if (step.type === 'group') {
        parts.push(renderGroup(step, layout));
      } else {
        parts.push(renderCard(step, layout));
      }
    });
  }

  // End capsule
  if (data.end) {
    parts.push(arrowFn(true));
    parts.push(renderCapsule(data.end, 'end'));
  }

  return `<div class="${flowClass}" id="diagram">\n${parts.join('\n')}\n</div>`;
}

// ─── CSS ───────────────────────────────────────────────────
function buildCSS(layout) {
  const isVertical = layout === 'tb' || layout === 'tb-inline';

  return `
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #fff; padding: 48px 32px; font-family: 'Noto Sans KR', sans-serif; }

/* ── Flow container ── */
.flow.horizontal { display: flex; align-items: center; gap: 0; justify-content: center; }
.flow.vertical   { display: flex; flex-direction: column; align-items: center; gap: 0; }

/* ── Capsules ── */
.cap {
  padding: 16px 22px; border-radius: 24px;
  text-align: center; flex-shrink: 0;
  display: flex; flex-direction: column; align-items: center; gap: 6px;
}
.cap .icon { width: 28px; height: 28px; }
.cap.start { background: #fff; border: 2px solid #2563eb; }
.cap.end   { background: #eef2ff; border: 2px solid #2563eb; }
.cap .title { font-size: 13px; font-weight: 700; color: #2563eb; }
.cap .desc  { font-size: 12px; color: #475569; line-height: 1.4; }

/* ── Horizontal arrow ── */
.arrow {
  width: 40px; display: flex; align-items: center; flex-shrink: 0; position: relative;
}
.arrow .shaft { width: 100%; height: 2px; background: #cbd5e1; }
.arrow .shaft::after {
  content: ''; position: absolute; right: 0; top: 50%; transform: translateY(-50%);
  border: 5px solid transparent; border-left: 7px solid #cbd5e1;
}
.arrow.blue .shaft { background: #2563eb; }
.arrow.blue .shaft::after { border-left-color: #2563eb; }

/* ── Vertical arrow ── */
.v-arrow {
  height: 40px; display: flex; justify-content: center; flex-shrink: 0; position: relative;
}
.v-arrow .v-shaft { height: 100%; width: 2px; background: #cbd5e1; }
.v-arrow .v-shaft::after {
  content: ''; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);
  border: 5px solid transparent; border-top: 7px solid #cbd5e1;
}
.v-arrow.blue .v-shaft { background: #2563eb; }
.v-arrow.blue .v-shaft::after { border-top-color: #2563eb; }

/* ── Card common ── */
.card {
  width: 186px; min-height: 84px;
  border-radius: 6px; padding: 12px 14px;
  display: flex; flex-direction: row; align-items: flex-start; gap: 10px;
  flex-shrink: 0;
}
.card .icon { width: 24px; height: 24px; flex-shrink: 0; margin-top: 2px; }
.card .content { flex: 1; }
.card .label {
  font-size: 11px; font-weight: 700; letter-spacing: 0.6px; margin-bottom: 4px;
}
.card .text {
  font-size: 13px; font-weight: 500; line-height: 1.5; color: #1e293b;
}
.card .tag {
  display: inline-block; margin-top: 6px; padding: 2px 10px;
  border-radius: 4px; font-size: 10px; font-weight: 600;
  background: #f1f5f9; border: 1px solid #cbd5e1; color: #475569;
  width: fit-content;
}

/* ── Card types ── */
.card.route   { background: #eef2ff; border: 1.5px solid #2563eb; }
.card.route .label { color: #2563eb; }
.card.route .text  { color: #1e40af; }

.card.think   { background: #f8f9ff; border: 1.5px solid #a5b4fc; }
.card.think .label { color: #6366f1; }
.card.think .text  { color: #1e40af; }

.card.act     { background: #ffffff; border: 1.5px solid #2563eb; }
.card.act .label { color: #2563eb; }

.card.result  { background: #f8fafc; border: 1.5px dashed #94a3b8; }
.card.result .label { color: #64748b; }
.card.result .text  { color: #475569; font-family: 'Menlo', monospace; font-size: 11px; }

.card.observe { background: #f8f9ff; border: 1.5px solid #a5b4fc; }
.card.observe .label { color: #6366f1; }
.card.observe .text  { color: #1e40af; }

.card.process { background: #eef2ff; border: 1.5px solid #2563eb; }
.card.process .label { color: #2563eb; }
.card.process .text  { color: #1e40af; }

.card.store   { background: #f8fafc; border: 1.5px solid #64748b; }
.card.store .label { color: #64748b; }
.card.store .text  { color: #475569; }

/* ── Group (ReAct box) ── */
.react-group {
  border: 2px dashed #2563eb; border-radius: 10px;
  padding: 24px 18px 18px 18px; position: relative;
  background: #fcfcff; flex-shrink: 0;
}
.react-group .group-label {
  position: absolute; top: -10px; left: 20px;
  background: #fff; padding: 0 10px;
  font-size: 11px; font-weight: 700; color: #2563eb; letter-spacing: 0.6px;
}

/* ── Grid 2x2 inside group ── */
.grid-2x2 {
  display: grid;
  grid-template-columns: 186px 186px;
  grid-template-rows: auto auto;
  gap: 12px;
}
.grid-2x2 .card { position: relative; }

/* Grid flow arrows: think→act (right), act→result (down), result→observe (left) */
.grid-2x2 .card.think::after {
  content: ''; position: absolute; right: -9px; top: 50%; transform: translateY(-50%);
  border: 5px solid transparent; border-left: 6px solid #a5b4fc;
}
.grid-2x2 .card.act::after {
  content: ''; position: absolute; bottom: -9px; left: 50%; transform: translateX(-50%);
  border: 5px solid transparent; border-top: 6px solid #2563eb;
}
.grid-2x2 .card.result::before {
  content: ''; position: absolute; left: -9px; top: 50%; transform: translateY(-50%);
  border: 5px solid transparent; border-right: 6px solid #94a3b8;
}

/* ── Inline row inside group ── */
.inline-row {
  display: flex; gap: 12px; align-items: flex-start;
}
.inline-row .card { position: relative; }
.inline-row .card:not(:last-child)::after {
  content: ''; position: absolute; right: -9px; top: 50%; transform: translateY(-50%);
  border: 5px solid transparent; border-left: 6px solid #a5b4fc;
}
`;
}

// ─── Full HTML Document ────────────────────────────────────
function buildFullHTML(data, layout) {
  return `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>${buildCSS(layout)}</style>
</head>
<body>
${buildFlowHTML(data, layout)}
</body>
</html>`;
}

// ─── Puppeteer Render ──────────────────────────────────────
let _browser = null;

async function getBrowser() {
  if (!_browser) {
    _browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox'],
      protocolTimeout: 60000,
    });
  }
  return _browser;
}

async function closeBrowser() {
  if (_browser) {
    await _browser.close();
    _browser = null;
  }
}

async function renderPNG(html, outputPath) {
  const browser = await getBrowser();
  const page = await browser.newPage();

  await page.setViewport({ width: 2400, height: 1200, deviceScaleFactor: 2 });

  page.on('console', msg => console.log('PAGE:', msg.text()));
  page.on('pageerror', err => console.error('PAGE ERROR:', err.message));

  await page.setContent(html, { waitUntil: 'networkidle0', timeout: 30000 });

  // Wait for Google Fonts
  await page.waitForFunction(() => document.fonts && document.fonts.ready);

  const diagram = await page.$('#diagram');
  if (!diagram) {
    console.error('Error: #diagram element not found');
    await page.close();
    return;
  }

  await diagram.screenshot({ path: outputPath, omitBackground: false });
  console.log(`OK: ${outputPath}`);

  await page.close();
}

// ─── Main ──────────────────────────────────────────────────
async function main() {
  if (isPreview) {
    // Preview mode: write HTML to temp file and open in browser
    const layout = 'lr-grid'; // Default preview layout
    const html = buildFullHTML(json, layout);
    const tmpPath = '/tmp/flow-preview.html';
    fs.writeFileSync(tmpPath, html, 'utf-8');
    execSync(`open "${tmpPath}"`);
    console.log(`Preview: ${tmpPath}`);
    return;
  }

  if (isVariations) {
    // Variations mode: generate 4 PNGs with single browser
    const outDir = outputArg;
    if (!fs.existsSync(outDir)) {
      fs.mkdirSync(outDir, { recursive: true });
    }

    const layouts = ['lr', 'tb', 'lr-grid', 'tb-inline'];
    for (const layout of layouts) {
      const html = buildFullHTML(json, layout);
      const pngPath = path.join(outDir, `flow-${layout}.png`);
      await renderPNG(html, pngPath);
    }
    await closeBrowser();
    return;
  }

  // Single PNG mode
  const layout = detectBestLayout(json);
  const html = buildFullHTML(json, layout);
  await renderPNG(html, outputArg);
  await closeBrowser();
}

function detectBestLayout(data) {
  // If there's a group, use lr-grid by default
  const hasGroup = data.steps && data.steps.some(s => s.type === 'group');
  return hasGroup ? 'lr-grid' : 'lr';
}

main().catch(err => { console.error(err); process.exit(1); });
