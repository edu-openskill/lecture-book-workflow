// ══ App ══ Entry point, init, window.* exports for inline HTML handlers

import { state, shared } from './state.js';
import { render, syncFromRange, syncFromNum } from './renderer.js';
import { showToast, switchTab, toggleSection, goToPreviewPage, goToPrevPage, goToNextPage, switchLayoutSubTab, onEditorInput } from './ui.js';
import { fetchProject } from './api.js';
import { applyPreset, applyPresetFromJSON, setComponent, updateFont, updateTypo, updateTypoSizes, updateTocDepth, updatePageFormat, setOutputMode, updateMargin, setImgPreset, updateImgWidth, updateColor, exportConfig, resetAll, fetchDesigns, saveDesign, loadDesign, deleteDesign, fetchPresets, saveAsPreset, deletePreset, renamePreset, updatePresetValues } from './design.js';
import { scheduleDesignRebuild, buildSvgPreview, exportPdf, restageFiles, combineMd } from './builder.js';
import { fetchFiles, toggleFileSelectAll, toggleFileGroup, onFileCheckChange } from './files.js';
import { openFileEditor, saveFileContent, closeFileEditor, openMdModal, closeMdModal, buildFromModal, initKeyboardShortcuts, initResizeHandles } from './editor.js';
import { fetchImages, setImageOverride, resetImageOverride } from './images.js';
import { renderTableList, onTableSlider, applyTableOverride, resetTableOverride } from './tables.js';
import { setZoom, zoomIn, zoomOut, zoomFit } from './zoom.js';
import { fetchLayoutIssues, buildVerified, hideVerifyBanner, runReadabilityCheck } from './layout.js';
import { renderAllPropertyEditors, updateComponentProp, resetComponentProp, toggleCompProps, loadCustomVariants, selectVariant, showCreateVariantDialog, createVariant, renameVariant, removeVariant, saveCurrentAsVariant } from './variants.js';

// ── Expose to window for inline HTML event handlers ──
Object.assign(window, {
  // state (for inline expressions like state.tableWidth=+this.value)
  state,

  // renderer
  render, syncFromRange, syncFromNum,

  // ui
  showToast, switchTab, toggleSection, goToPreviewPage, goToPrevPage, goToNextPage,
  switchLayoutSubTab, onEditorInput,

  // design
  applyPreset, setComponent, updateFont, updateTypo, updateTypoSizes, updateTocDepth,
  updatePageFormat, setOutputMode, updateMargin, setImgPreset, updateImgWidth, updateColor,
  exportConfig, resetAll, saveDesign, loadDesign, deleteDesign,
  saveAsPreset, deletePreset, applyPresetFromJSON, renamePreset, updatePresetValues,

  // builder
  scheduleDesignRebuild, buildSvgPreview, exportPdf, restageFiles, combineMd,

  // files
  toggleFileSelectAll, toggleFileGroup, onFileCheckChange,

  // editor
  openFileEditor, saveFileContent, closeFileEditor, openMdModal, closeMdModal, buildFromModal,

  // images
  setImageOverride, resetImageOverride,

  // tables
  onTableSlider, applyTableOverride, resetTableOverride,

  // zoom
  zoomIn, zoomOut, zoomFit,

  // layout
  fetchLayoutIssues, buildVerified, hideVerifyBanner, runReadabilityCheck,

  // variants
  updateComponentProp, resetComponentProp, toggleCompProps,
  selectVariant, showCreateVariantDialog, createVariant,
  renameVariant, removeVariant, saveCurrentAsVariant,
});

// ── Init ──

async function init() {
  render();
  await fetchProject();
  await fetchFiles();
  await fetchDesigns();
  await fetchPresets();
  await loadCustomVariants();

  // 서버 모드 확인 (CLI --file로 시작했을 수 있음)
  try {
    const modeResp = await fetch('/api/mode');
    const modeData = await modeResp.json();
    if (modeData.mode === 'file' && modeData.file_path) {
      shared.currentMode = 'file';
      shared.fileDesignable = modeData.designable;
      if (typeof window.applyFileModeUI === 'function') {
        window.applyFileModeUI(modeData.file_path, modeData.designable);
      }
    }
  } catch (e) { /* 프로젝트 모드로 fallback */ }

  initKeyboardShortcuts();
  initResizeHandles();
  renderAllPropertyEditors();
  scheduleDesignRebuild(true);
}

document.addEventListener('DOMContentLoaded', init);
