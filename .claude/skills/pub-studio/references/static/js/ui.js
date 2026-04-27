// ══ UI ══ Tabs, sections, toast, page navigation

import { shared } from './state.js';

export function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2000);
}

export function switchTab(tab) {
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.toggle('active', p.id === 'panel-' + tab));
}

export function toggleSection(id) { document.getElementById(id).classList.toggle('collapsed'); }

export function goToPreviewPage(pageNum) {
  switchTab('editor');
  const viewer = document.getElementById('svg-viewer');
  const target = viewer.querySelector(`.svg-page[data-page="${pageNum}"]`);
  if (target) {
    const img = target.querySelector('img');
    if (img && img.dataset.src) {
      img.src = img.dataset.src;
      img.removeAttribute('data-src');
    }
    target.scrollIntoView({ behavior: 'smooth' });
  }
}

export function goToPrevPage() {
  if (shared._currentPageNum > 1) {
    shared._currentPageNum--;
    _scrollToPage(shared._currentPageNum);
  }
}

export function goToNextPage() {
  if (shared._currentPageNum < shared._totalPageCount) {
    shared._currentPageNum++;
    _scrollToPage(shared._currentPageNum);
  }
}

function _scrollToPage(n) {
  const viewer = document.getElementById('svg-viewer');
  const target = viewer.querySelector(`.svg-page[data-page="${n}"]`);
  if (target) {
    const img = target.querySelector('img');
    if (img && img.dataset.src) { img.src = img.dataset.src; img.removeAttribute('data-src'); }
    target.scrollIntoView({ behavior: 'smooth' });
  }
}

export function switchLayoutSubTab(tab) {
  document.querySelectorAll('.layout-sub-tab').forEach(b => b.classList.remove('active'));
  document.getElementById('sub-tab-' + tab).classList.add('active');
  document.getElementById('layout-issues-panel').style.display = tab === 'issues' ? '' : 'none';
  document.getElementById('readability-panel').style.display = tab === 'readability' ? '' : 'none';
}

export function onEditorInput() {
  document.getElementById('rebuild-hint').classList.add('visible');
}
