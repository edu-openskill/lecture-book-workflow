// ══ Builder ══ SVG build, PDF export, restage, combine MD

import { state, shared } from './state.js';
import { showToast } from './ui.js';
import { getSelectedFiles, renderFileSelector } from './files.js';
import { setZoom } from './zoom.js';
import { fetchImages } from './images.js';
import { renderTableList } from './tables.js';

export function scheduleDesignRebuild(forceStage1 = false) {
  if (shared._svgTimer) clearTimeout(shared._svgTimer);
  setBuildStatus('rebuilding...');
  shared._svgTimer = setTimeout(() => buildSvgPreview(forceStage1), 300);
}

export async function buildSvgPreview(forceStage1 = false) {
  if (shared.currentMode === 'project') {
    const files = getSelectedFiles();
    const totalFiles = files.front.length + files.chapters.length + files.back.length;
    if (totalFiles === 0) {
      clearSvgViewer();
      setBuildStatus('');
      return;
    }
  }

  if (shared._isBuilding) return;
  shared._isBuilding = true;

  setBuildStatus('building...');

  const viewer = document.getElementById('svg-viewer');
  const pages = viewer.querySelectorAll('.svg-page');
  let currentPage = 1;
  pages.forEach(p => {
    if (p.getBoundingClientRect().top < viewer.getBoundingClientRect().top + 100) {
      currentPage = parseInt(p.dataset.page);
    }
  });

  try {
    let reqBody;
    if (shared.currentMode === 'file') {
      reqBody = {
        mode: 'file',
        design_state: state,
        include_cover: document.getElementById('include-cover').checked,
        include_toc: document.getElementById('include-toc').checked,
      };
    } else {
      reqBody = {
        files: getSelectedFiles(),
        design_state: state,
        force_stage1: forceStage1,
        include_cover: document.getElementById('include-cover').checked,
        include_toc: document.getElementById('include-toc').checked,
      };
    }

    const resp = await fetch('/api/build-svg', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(reqBody)
    });
    const data = await resp.json();

    if (data.ok) {
      renderSvgPages(data.page_count, data.svg_base, currentPage);
      setBuildStatus(`${data.page_count}p / ${data.duration}s (stage ${data.stage})`);
      fetchImages();
      if (data.tables) renderTableList(data.tables);
    } else {
      setBuildStatus('error');
      showToast('빌드 실패: ' + (data.error || '').slice(0, 100));
      console.error('Build error:', data.error);
    }
  } catch (e) {
    setBuildStatus('connection error');
    showToast('서버 연결 오류: ' + e.message);
  } finally {
    shared._isBuilding = false;
  }
}

export function setBuildStatus(msg) {
  const el = document.getElementById('build-status');
  if (el) el.textContent = msg;
}

export function clearSvgViewer() {
  document.getElementById('svg-viewer').innerHTML =
    '<div class="svg-empty">파일을 선택하면 실시간 PDF 프리뷰가 표시됩니다.</div>';
  document.getElementById('page-info').innerHTML = '<span class="page-current">-</span><span class="page-sep">/</span><span class="page-total">-</span>';
}

export function renderSvgPages(pageCount, svgBase, restorePage = null) {
  const viewer = document.getElementById('svg-viewer');
  const ts = Date.now();

  // 페이지 이동용 상태 갱신
  shared._totalPageCount = pageCount;
  shared._currentPageNum = restorePage || 1;

  viewer.innerHTML = '';
  for (let p = 1; p <= pageCount; p++) {
    const pageDiv = document.createElement('div');
    pageDiv.className = 'svg-page';
    pageDiv.dataset.page = p;
    pageDiv.innerHTML = `<img data-src="${svgBase}${p}?t=${ts}" alt="Page ${p}">`;
    viewer.appendChild(pageDiv);
  }

  document.getElementById('page-info').innerHTML = `<span class="page-current">1</span><span class="page-sep">/</span><span class="page-total">${pageCount}</span>`;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const img = e.target.querySelector('img');
        if (img && img.dataset.src) {
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
        }
        observer.unobserve(e.target);
      }
    });
  }, { root: viewer, rootMargin: '400px' });

  viewer.querySelectorAll('.svg-page').forEach(p => observer.observe(p));

  setZoom(shared.zoomLevel);

  if (restorePage) {
    const targetPage = Math.min(restorePage, pageCount);
    const targetEl = viewer.querySelector(`.svg-page[data-page="${targetPage}"]`);
    if (targetEl) {
      const img = targetEl.querySelector('img');
      if (img && img.dataset.src) {
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
      }
      targetEl.scrollIntoView({ behavior: 'instant' });
    }
  }

  viewer.onscroll = () => {
    const pages = viewer.querySelectorAll('.svg-page');
    let current = 1;
    pages.forEach(p => {
      if (p.getBoundingClientRect().top < viewer.getBoundingClientRect().top + 100) {
        current = parseInt(p.dataset.page);
      }
    });
    document.getElementById('page-info').innerHTML = `<span class="page-current">${current}</span><span class="page-sep">/</span><span class="page-total">${pageCount}</span>`;
  };

  const pageInfoEl = document.getElementById('page-info');
  pageInfoEl.style.cursor = 'pointer';
  pageInfoEl.onclick = () => {
    const currentSpan = pageInfoEl.querySelector('.page-current');
    const currentP = currentSpan ? currentSpan.textContent : '1';

    const input = document.createElement('input');
    input.type = 'number';
    input.className = 'page-input';
    input.value = currentP;
    input.min = 1;
    input.max = pageCount;

    pageInfoEl.replaceWith(input);
    input.focus();
    input.select();

    const restore = () => {
      input.replaceWith(pageInfoEl);
    };

    const goToPage = (n) => {
      n = Math.max(1, Math.min(pageCount, parseInt(n) || 1));
      const target = viewer.querySelector(`.svg-page[data-page="${n}"]`);
      if (target) {
        const img = target.querySelector('img');
        if (img && img.dataset.src) {
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
        }
        target.scrollIntoView({ behavior: 'smooth' });
      }
      restore();
    };

    input.addEventListener('keydown', e => {
      if (e.key === 'Enter') goToPage(input.value);
      if (e.key === 'Escape') restore();
    });
    input.addEventListener('blur', () => {
      setTimeout(restore, 150);
    });
  };
}

// ── PDF Export ──

export async function exportPdf() {
  const btn = document.querySelector('.build-btn');
  btn.classList.add('building');
  btn.textContent = 'Exporting...';

  try {
    const resp = await fetch('/api/export-pdf', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ design_state: state })
    });
    const data = await resp.json();

    if (data.ok) {
      showToast('PDF Export 완료 (' + data.duration + '초)');
      window.open(data.pdf + '?t=' + Date.now(), '_blank');
    } else {
      showToast('Export 실패: ' + (data.error || '').slice(0, 100));
    }
  } catch (e) {
    showToast('Export 오류: ' + e.message);
  } finally {
    btn.classList.remove('building');
    btn.textContent = 'PDF Export';
  }
}

// ── Restage ──

export async function restageFiles() {
  try {
    const resp = await fetch('/api/restage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({})
    });
    const data = await resp.json();
    if (data.ok) {
      const s = data.staged;
      shared.fileList = data.files;
      renderFileSelector();
      showToast(`Restage 완료: front ${s.front} + chapters ${s.chapters} + back ${s.back}개`);
    } else {
      showToast('Restage 실패: ' + (data.error || ''));
    }
  } catch (e) {
    showToast('프리뷰 서버에 연결할 수 없습니다. preview.py를 먼저 실행하세요.');
  }
}

// ── Combined MD ──

export async function combineMd() {
  const files = getSelectedFiles();
  if (files.front.length + files.chapters.length + files.back.length === 0) {
    showToast('체크된 파일이 없습니다. PDF에 포함할 파일을 선택하세요.');
    return;
  }

  try {
    const resp = await fetch('/api/combine-md', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ files })
    });
    const data = await resp.json();
    if (data.ok) {
      showToast('통합본 생성 완료: ' + data.path);
    } else {
      showToast('통합본 생성 실패: ' + (data.error || ''));
    }
  } catch (e) {
    showToast('프리뷰 서버에 연결할 수 없습니다. preview.py를 먼저 실행하세요.');
  }
}
