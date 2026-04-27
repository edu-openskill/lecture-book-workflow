// ══ Editor ══ File content editor, MD modal

import { shared } from './state.js';
import { showToast } from './ui.js';
import { buildSvgPreview, scheduleDesignRebuild } from './builder.js';

export async function openFileEditor(path) {
  document.querySelectorAll('.file-item').forEach(el => el.classList.toggle('active', el.dataset.path === path));

  try {
    const resp = await fetch('/api/file-content?path=' + encodeURIComponent(path));
    const data = await resp.json();
    if (data.error) { showToast(data.error); return; }

    shared.editingPath = data.path;
    shared.editingMtime = data.last_modified;
    document.getElementById('editing-filename').textContent = path.split('/').pop();
    document.getElementById('raw-editor').value = data.content;
    document.getElementById('content-editor').style.display = 'flex';
  } catch (e) {
    showToast('파일 로드 실패');
  }
}

export async function saveFileContent() {
  if (!shared.editingPath) return;
  const content = document.getElementById('raw-editor').value;
  try {
    const resp = await fetch('/api/save-raw', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: shared.editingPath, content })
    });
    const data = await resp.json();
    if (data.ok) {
      shared.editingMtime = data.last_modified;
      showToast('저장 완료');
      scheduleDesignRebuild(true);
    } else {
      showToast('저장 실패: ' + (data.error || ''));
    }
  } catch (e) {
    showToast('서버 연결 오류');
  }
}

export function closeFileEditor() {
  document.getElementById('content-editor').style.display = 'none';
  shared.editingPath = '';
  document.querySelectorAll('.file-item').forEach(el => el.classList.remove('active'));
}

// ── MD 편집 모달 ──

export async function openMdModal(path) {
  shared._mdModalPath = path;
  const overlay = document.getElementById('md-modal-overlay');
  const title = document.getElementById('md-modal-title');
  const editor = document.getElementById('md-modal-editor');
  title.textContent = path.split('/').pop();
  editor.value = 'Loading...';
  overlay.style.display = 'flex';
  try {
    const resp = await fetch('/api/file-content?path=' + encodeURIComponent(path));
    const data = await resp.json();
    if (data.error) { editor.value = 'Error: ' + data.error; return; }
    editor.value = data.content || '';
  } catch (e) {
    editor.value = 'Error loading file: ' + e.message;
  }
}

export function closeMdModal() {
  document.getElementById('md-modal-overlay').style.display = 'none';
  shared._mdModalPath = '';
}

export async function buildFromModal() {
  const editor = document.getElementById('md-modal-editor');
  const content = editor.value;
  if (!shared._mdModalPath) return;
  try {
    const saveResp = await fetch('/api/save-raw', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ path: shared._mdModalPath, content })
    });
    const saveData = await saveResp.json();
    if (!saveData.ok) { showToast('저장 실패: ' + (saveData.error || ''), 'error'); return; }
    closeMdModal();
    showToast('저장 완료. 빌드 중...');
    await buildSvgPreview(true);
    showToast('빌드 완료');
  } catch (e) {
    showToast('오류: ' + e.message, 'error');
  }
}

// Keyboard shortcut: Ctrl/Cmd + S
export function initKeyboardShortcuts() {
  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
      e.preventDefault();
      if (shared.editingPath) saveFileContent();
    }
  });
}

// ── Resize handles ──

export function initResizeHandles() {
  // 수직 리사이즈: editor-left ↔ editor-right
  const vHandle = document.getElementById('resize-left-right');
  const leftPanel = document.querySelector('.editor-left');
  if (vHandle && leftPanel) {
    let startX, startW;
    vHandle.addEventListener('mousedown', e => {
      startX = e.clientX;
      startW = leftPanel.offsetWidth;
      vHandle.classList.add('dragging');
      const onMove = ev => {
        leftPanel.style.flex = 'none';
        leftPanel.style.width = Math.max(200, Math.min(600, startW + (ev.clientX - startX))) + 'px';
      };
      const onUp = () => {
        vHandle.classList.remove('dragging');
        document.removeEventListener('mousemove', onMove);
        document.removeEventListener('mouseup', onUp);
      };
      document.addEventListener('mousemove', onMove);
      document.addEventListener('mouseup', onUp);
      e.preventDefault();
    });
  }

  // 수평 리사이즈: file-selector ↔ content-editor
  const hHandle = document.getElementById('resize-file-editor');
  const fileUI = document.getElementById('project-file-ui');
  if (hHandle && fileUI) {
    let startY, startH;
    hHandle.addEventListener('mousedown', e => {
      startY = e.clientY;
      startH = fileUI.offsetHeight;
      hHandle.classList.add('dragging');
      const onMove = ev => {
        fileUI.style.flex = 'none';
        fileUI.style.height = Math.max(80, startH + (ev.clientY - startY)) + 'px';
      };
      const onUp = () => {
        hHandle.classList.remove('dragging');
        document.removeEventListener('mousemove', onMove);
        document.removeEventListener('mouseup', onUp);
      };
      document.addEventListener('mousemove', onMove);
      document.addEventListener('mouseup', onUp);
      e.preventDefault();
    });
  }
}
