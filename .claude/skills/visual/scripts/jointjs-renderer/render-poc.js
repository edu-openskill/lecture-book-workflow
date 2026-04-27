import puppeteer from 'puppeteer';
import fs from 'fs';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const htmlPath = path.join(__dirname, 'poc-sequence.html');
const outputPath = process.argv[2] || '/tmp/poc-sequence.png';

async function render() {
  const html = fs.readFileSync(htmlPath, 'utf-8');

  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage();

  page.on('console', msg => console.log('PAGE:', msg.text()));
  page.on('pageerror', err => console.error('PAGE ERROR:', err.message));

  // setContent로 HTML 직접 주입 (file:// 프로토콜 문제 회피)
  await page.setContent(html, { waitUntil: 'networkidle0', timeout: 30000 });

  // JointJS + SVG 렌더링 대기
  await new Promise(r => setTimeout(r, 2000));

  await page.screenshot({ path: outputPath, fullPage: true, omitBackground: false });
  console.log(`OK: ${outputPath}`);

  await browser.close();
}

render().catch(err => { console.error(err); process.exit(1); });
