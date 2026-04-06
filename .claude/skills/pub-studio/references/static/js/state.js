// ══ State ══ Central state, constants, presets

export const state = {
  preset: '1',
  components: { body:'d1', heading:'d1', code:'d1', inline_code:'d1', quote:'d1', table:'d1', toc:'d1' },
  fonts: { body: '"RIDIBatang", serif', code: '"D2Coding", monospace' },
  typo: { size: 10, tracking: 0, leading: 10, paragraphGap: 8 },
  margins: { top: 20, bottom: 28, left: 22, right: 17 },
  images: {
    gemini:   { preset: 'bordered', width: 70 },
    terminal: { preset: 'minimal',  width: 70 },
    diagram:  { preset: 'minimal',  width: 60 }
  },
  colors: { primary: '#2563eb', text: '#1a1a1a', codeText: '#1e40af', quoteBg: '#f5f8ff' },
  page: { format: 'B5_4x6배판', outputMode: 'pod' },
  typoSizes: { h1: 26, h2: 16, h3: 13, h4: 11, code: 8, quote: 9, table: 8.5, inlineCode: 8.5 },
  tocDepth: 2,
  tocSpacing: 4,
  imageOverrides: {},
  tableWidth: 100,
  tableAlign: 'left',
  tableFirstColRatio: 1.0,
  tableOverrides: {},
  componentStyles: {},
};

export const PAGE_FORMATS = {
  'A4_국배판':   { w: 210, h: 297, label: 'A4 / 국배판 (210×297)' },
  'B5_4x6배판': { w: 188, h: 254, label: 'B5 / 4×6배판 (188×254)' },
  '크라운판':    { w: 176, h: 248, label: '크라운판 (176×248)' },
  '신국판':      { w: 152, h: 225, label: '신국판 (152×225)' },
  'A5_국판':     { w: 148, h: 210, label: 'A5 / 국판 (148×210)' },
  'A6_국반판':   { w: 105, h: 148, label: 'A6 / 국반판 (105×148)' },
};

export const PRESETS = {
  '1': {
    components: { body:'d1',heading:'d1',code:'d1',inline_code:'d1',quote:'d1',table:'d1',toc:'d1' },
  },
  '2': {
    components: { body:'d2',heading:'d2',code:'d2',inline_code:'d2',quote:'d2',table:'d2',toc:'d2' },
  }
};

export const CODE_SAMPLE = `from fastapi import FastAPI
from langchain.vectorstores import Chroma

app = FastAPI()
vectorstore = Chroma(persist_directory="./chroma_db")

@app.get("/ask")
async def ask(query: str):
    # 유사도 검색 실행
    docs = vectorstore.similarity_search(query, k=3)
    return {"results": docs}`;

// ── Builtin Variant Definitions ──
// Property naming: prefix_camelCase (prefix = sub-selector, camelCase = CSS property)
// No prefix = root element. 'name' is reserved (display label, not CSS).
export const BUILTIN_VARIANTS = {
  heading: {
    d1: {
      name: '클래식',
      h1_fontWeight: '700', h1_color: 'var(--color-text)', h1_paddingBottom: '8px',
      h1_borderBottom: '3px solid var(--color-primary)', h1_marginTop: '10px', h1_marginBottom: '14px',
      h2_fontWeight: '700', h2_color: 'var(--color-primary-dark)',
      h2_borderLeft: '4px solid var(--color-primary)', h2_paddingLeft: '12px',
      h2_marginTop: '16px', h2_marginBottom: '14px',
      h3_fontWeight: '600', h3_color: '#1e3a5f', h3_marginTop: '12px', h3_marginBottom: '14px',
      h4_fontWeight: '600', h4_color: '#374151', h4_marginTop: '8px', h4_marginBottom: '14px',
      _globals: { 'typoSizes.h1': 26, 'typoSizes.h2': 16, 'typoSizes.h3': 13, 'typoSizes.h4': 11 },
    },
    d2: {
      name: '미니멀',
      h1_fontWeight: '700', h1_color: 'var(--color-text)', h1_paddingBottom: '8px',
      h1_borderBottom: '3px solid var(--color-primary)', h1_marginTop: '10px', h1_marginBottom: '8px',
      h2_fontWeight: '700', h2_color: 'var(--color-text)',
      h2_marginTop: '8px', h2_marginBottom: '6px', h2_borderLeft: 'none', h2_paddingLeft: '0',
      h3_fontWeight: '600', h3_color: '#374151', h3_marginTop: '8px', h3_marginBottom: '4px',
      h4_fontWeight: '500', h4_color: '#555', h4_marginTop: '6px', h4_marginBottom: '4px',
      _globals: { 'typoSizes.h1': 16, 'typoSizes.h2': 10, 'typoSizes.h3': 10, 'typoSizes.h4': 10 },
    },
  },
  code: {
    d1: {
      name: '카드',
      fontWeight: '700', color: 'var(--color-text)', background: 'white',
      padding: '14px 16px', borderRadius: '8px', border: '1px solid #d1d5db',
      whiteSpace: 'pre', overflowX: 'auto',
      code_marginTop: '8px', code_marginBottom: '8px',
      _globals: { 'typoSizes.code': 8 },
    },
    d2: {
      name: '라인',
      fontWeight: '700', color: 'var(--color-text)', background: 'white',
      padding: '6px 16px', borderRadius: '0', border: 'none',
      borderTop: '2px solid #999', borderBottom: '2px solid #999',
      whiteSpace: 'pre', overflowX: 'auto',
      code_marginTop: '8px', code_marginBottom: '8px',
      _globals: { 'typoSizes.code': 6 },
    },
  },
  inline_code: {
    d1: {
      name: '배경',
      color: 'var(--color-code-text)', background: '#f3f4f6',
      padding: '2px 4px', borderRadius: '3px', fontSize: 'inherit',
    },
    d2: {
      name: '굵게',
      fontWeight: '700', color: '#1e3a5f', background: 'none',
      padding: '0', borderRadius: '0', fontSize: 'inherit',
    },
  },
  quote: {
    d1: {
      name: '사이드라인',
      color: '#4b5563', background: 'var(--color-quote-bg)',
      borderLeft: '3px solid var(--color-quote-border)', borderRadius: '0 4px 4px 0',
      padding: '10px 14px', margin: '10px 0', lineHeight: '1.5',
      _globals: { 'typoSizes.quote': 9 },
    },
    d2: {
      name: '점선',
      color: '#333', background: 'none',
      border: '1px dashed #aaa', borderRadius: '0',
      borderLeft: '1px dashed #aaa',
      padding: '10px 14px', margin: '10px 0', lineHeight: '1.5',
      _globals: { 'typoSizes.quote': 9 },
    },
    d3: {
      name: '콜아웃',
      color: '#333', background: '#f5f5f5',
      border: 'none', borderLeft: 'none', borderRadius: '4px',
      padding: '10px 14px', margin: '10px 0', lineHeight: '1.5',
      _globals: { 'typoSizes.quote': 9 },
    },
  },
  table: {
    d1: {
      name: '컬러 헤더',
      th_background: 'var(--color-primary-dark)', th_color: 'white',
      th_fontWeight: '500', th_padding: '8px 10px',
      td_padding: '8px 10px', td_borderBottom: '0.5px solid #e5e7eb',
      oddTd_background: '#f8fafc',
      table_marginTop: '0', table_marginBottom: '0',
      _globals: { 'typoSizes.table': 8.5 },
    },
    d2: {
      name: '그레이 헤더',
      th_background: '#e5e5e5', th_color: '#1a1a1a',
      th_fontWeight: '700', th_padding: '8px 10px', th_border: '0.5px solid #d1d5db',
      td_padding: '8px 10px', td_border: '0.5px solid #d1d5db',
      oddTd_background: '#fafafa',
      table_marginTop: '0', table_marginBottom: '0',
      _globals: { 'typoSizes.table': 8 },
    },
  },
  body: {
    d1: {
      name: '양쪽 정렬',
      p_textAlign: 'justify', strong_fontWeight: '700',
      strong_color: '#1e3a5f', emph_color: '#6b7280',
    },
  },
  toc: {
    d1: { name: '기본', _globals: { tocDepth: 2, tocSpacing: 4 } },
    d2: { name: '확장', _globals: { tocDepth: 3, tocSpacing: 4 } },
  },
  figure: {
    d1: { name: '기본', figure_marginTop: '8px', figure_marginBottom: '4px', figure_captionGap: '2px', figure_captionSize: '8px' },
  },
};

// Sub-selector mapping: prefix → CSS selector template ($D = [data-design="dN"])
export const VARIANT_SELECTORS = {
  heading: { h1: '.book-h1$D', h2: '.book-h2$D', h3: '.book-h3$D', h4: '.book-h4$D' },
  code: { '': '.book-code$D' },
  inline_code: { '': '.book-inline-code$D' },
  quote: { '': '.book-quote$D' },
  table: { th: '.book-table$D th', td: '.book-table$D td', oddTd: '.book-table$D tr:nth-child(odd) td' },
  body: { p: '.book-body$D p', strong: '.book-body$D strong' },
  figure: { '': '.book-figure$D' },
};

// Component property schemas (for Phase 2 property editor)
// global: { path } — 값을 state[path]에서 읽고 쓰는 글로벌 속성 (componentStyles 대신)
// type: 'separator' — 시각적 구분선
export const COMPONENT_SCHEMAS = {
  body: {
    p_textAlign: { type: 'select', options: ['justify','left','center'], label: '정렬' },
    _sep_typo: { type: 'separator', label: '타이포그래피' },
    _bodySize: { type: 'range', min: 4, max: 20, step: 0.5, unit: 'pt', label: '글자 크기', global: { path: 'typo.size' } },
    _bodyTracking: { type: 'range', min: -1, max: 2, step: 0.1, unit: 'pt', label: '자간', global: { path: 'typo.tracking' } },
    _bodyLeading: { type: 'range', min: 4, max: 100, step: 1, unit: 'pt', label: '행간', global: { path: 'typo.leading' } },
    _parGap: { type: 'range', min: 0, max: 100, step: 1, unit: 'pt', label: '문단 간격', global: { path: 'typo.paragraphGap' } },
    _sep_bold: { type: 'separator', label: '볼드' },
    strong_fontWeight: { type: 'select', options: [
      { value: '400', label: '400 (얇게)' },
      { value: '500', label: '500 (중간)' },
      { value: '600', label: '600 (약간 굵게)' },
      { value: '700', label: '700 (굵게)' },
      { value: '800', label: '800 (매우 굵게)' },
      { value: '900', label: '900 (극굵게)' },
    ], label: '볼드 굵기' },
    strong_color: { type: 'color', label: '볼드 색상' },
    emph_color: { type: 'color', label: '이탤릭 색상' },
  },
  heading: {
    _sep_h1: { type: 'separator', label: 'H1' },
    h1_marginTop: { type: 'range', min: 0, max: 80, unit: 'px', label: '위 여백' },
    h1_fontWeight: { type: 'select', options: ['400','500','600','700','800'], label: '굵기' },
    h1_color: { type: 'color', label: '색상' },
    h1_marginBottom: { type: 'range', min: 0, max: 40, unit: 'px', label: '아래 간격' },
    h1_borderBottom: { type: 'text', label: '하단선' },
    _sep_h2: { type: 'separator', label: 'H2' },
    h2_fontWeight: { type: 'select', options: ['400','500','600','700','800'], label: '굵기' },
    h2_color: { type: 'color', label: '색상' },
    h2_borderLeft: { type: 'text', label: '좌측선' },
    h2_paddingLeft: { type: 'range', min: 0, max: 30, unit: 'px', label: '좌측 간격' },
    h2_marginTop: { type: 'range', min: 0, max: 40, unit: 'px', label: '위 여백' },
    h2_marginBottom: { type: 'range', min: 0, max: 40, unit: 'px', label: '아래 간격' },
    _sep_h3: { type: 'separator', label: 'H3' },
    h3_fontWeight: { type: 'select', options: ['400','500','600','700'], label: '굵기' },
    h3_color: { type: 'color', label: '색상' },
    h3_marginTop: { type: 'range', min: 0, max: 30, unit: 'px', label: '위 여백' },
    h3_marginBottom: { type: 'range', min: 0, max: 30, unit: 'px', label: '아래 간격' },
    _sep_h4: { type: 'separator', label: 'H4' },
    h4_fontWeight: { type: 'select', options: ['400','500','600','700'], label: '굵기' },
    h4_color: { type: 'color', label: '색상' },
    h4_marginTop: { type: 'range', min: 0, max: 30, unit: 'px', label: '위 여백' },
    h4_marginBottom: { type: 'range', min: 0, max: 20, unit: 'px', label: '아래 간격' },
    _sep_sizes: { type: 'separator', label: '글자 크기' },
    _h1Size: { type: 'range', min: 10, max: 48, step: 1, unit: 'pt', label: 'h1 크기', global: { path: 'typoSizes.h1' } },
    _h2Size: { type: 'range', min: 6, max: 36, step: 1, unit: 'pt', label: 'h2 크기', global: { path: 'typoSizes.h2' } },
    _h3Size: { type: 'range', min: 6, max: 28, step: 1, unit: 'pt', label: 'h3 크기', global: { path: 'typoSizes.h3' } },
    _h4Size: { type: 'range', min: 6, max: 20, step: 1, unit: 'pt', label: 'h4 크기', global: { path: 'typoSizes.h4' } },
  },
  code: {
    background: { type: 'color', label: '배경색' },
    padding: { type: 'text', label: '패딩' },
    borderRadius: { type: 'range', min: 0, max: 16, unit: 'px', label: '모서리' },
    border: { type: 'text', label: '테두리' },
    _sep_margin: { type: 'separator', label: '여백' },
    code_marginTop: { type: 'range', min: 4, max: 40, unit: 'px', label: '위 여백' },
    code_marginBottom: { type: 'range', min: 4, max: 40, unit: 'px', label: '아래 여백' },
    _sep_padding: { type: 'separator', label: '내부 패딩' },
    code_paddingX: { type: 'range', min: 4, max: 30, unit: 'px', label: '좌우 패딩' },
    code_paddingY: { type: 'range', min: 4, max: 20, unit: 'px', label: '상하 패딩' },
    _sep_size: { type: 'separator', label: '글자 크기' },
    _codeSize: { type: 'range', min: 4, max: 18, step: 0.5, unit: 'pt', label: '코드 크기', global: { path: 'typoSizes.code' } },
  },
  inline_code: {
    color: { type: 'color', label: '글자 색상' },
    fontWeight: { type: 'select', options: ['400','500','600','700','800'], label: '굵기' },
    background: { type: 'color', label: '배경색' },
    borderRadius: { type: 'range', min: 0, max: 8, unit: 'px', label: '모서리' },
  },
  quote: {
    color: { type: 'color', label: '글자 색상' },
    background: { type: 'color', label: '배경색' },
    borderLeft: { type: 'text', label: '좌측선' },
    padding: { type: 'text', label: '패딩' },
    _sep_margin: { type: 'separator', label: '여백' },
    quote_marginTop: { type: 'range', min: 4, max: 40, unit: 'px', label: '위 여백' },
    quote_marginBottom: { type: 'range', min: 4, max: 40, unit: 'px', label: '아래 여백' },
    _sep_size: { type: 'separator', label: '글자 크기' },
    _quoteSize: { type: 'range', min: 4, max: 18, step: 0.5, unit: 'pt', label: '인용문 크기', global: { path: 'typoSizes.quote' } },
  },
  table: {
    th_background: { type: 'color', label: '헤더 배경' },
    th_color: { type: 'color', label: '헤더 글자' },
    th_fontWeight: { type: 'select', options: ['400','500','600','700'], label: '헤더 굵기' },
    td_padding: { type: 'text', label: '셀 패딩' },
    oddTd_background: { type: 'color', label: '줄무늬 배경' },
    _sep_margin: { type: 'separator', label: '표 여백' },
    table_marginTop: { type: 'range', min: 0, max: 30, unit: 'px', label: '위 여백' },
    table_marginBottom: { type: 'range', min: 0, max: 30, unit: 'px', label: '아래 여백' },
    _sep_layout: { type: 'separator', label: '크기 & 레이아웃' },
    _tableSize: { type: 'range', min: 4, max: 18, step: 0.5, unit: 'pt', label: '표 글자 크기', global: { path: 'typoSizes.table' } },
    _tableWidth: { type: 'range', min: 40, max: 100, step: 5, unit: '%', label: '표 너비', global: { path: 'tableWidth' } },
    _tableAlign: { type: 'select', label: '셀 정렬', options: [
      { value: 'left', label: '왼쪽' }, { value: 'center', label: '가운데' }, { value: 'right', label: '오른쪽' }
    ], global: { path: 'tableAlign' } },
    _sep_cols: { type: 'separator', label: '열 너비' },
    _tableFirstColRatio: { type: 'range', min: 0.3, max: 3.0, step: 0.1, unit: 'x', label: '첫 열 비율', global: { path: 'tableFirstColRatio' } },
  },
  figure: {
    figure_marginTop: { type: 'range', min: 0, max: 30, unit: 'px', label: '위 여백' },
    figure_marginBottom: { type: 'range', min: 0, max: 30, unit: 'px', label: '아래 여백' },
    _sep_caption: { type: 'separator', label: '캡션' },
    figure_captionGap: { type: 'range', min: 0, max: 20, unit: 'px', label: '이미지-캡션 간격' },
    figure_captionSize: { type: 'range', min: 4, max: 14, step: 0.5, unit: 'px', label: '캡션 크기' },
  },
  toc: {
    _tocDepth: { type: 'select', label: '목차 깊이', options: [
      { value: '1', label: 'h1만' }, { value: '2', label: 'h1~h2' },
      { value: '3', label: 'h1~h3' }, { value: '4', label: 'h1~h4' }
    ], global: { path: 'tocDepth' } },
    _tocSpacing: { type: 'range', min: 0, max: 20, step: 1, unit: 'pt', label: '항목 간격', global: { path: 'tocSpacing' } },
  },
};

// Custom variants loaded from server (merged with BUILTIN_VARIANTS at runtime)
// Format: { heading: { d3: { name:'커스텀', ...props }, d4: ... }, code: { d3: ... } }
export const customVariants = {};

// Get all variants for a component (builtin + custom merged)
export function getAllVariants(component) {
  const builtin = BUILTIN_VARIANTS[component] || {};
  const custom = customVariants[component] || {};
  return { ...builtin, ...custom };
}

// Mutable shared state (object reference, so all modules can mutate properties)
export const shared = {
  projectInfo: null,
  fileList: { chapters: [], front: [], back: [] },
  editingPath: '',
  editingMtime: 0,
  zoomLevel: 100,
  _svgTimer: null,
  _isBuilding: false,
  currentMode: 'project',
  fileDesignable: true,
  _serverConnected: false,
  _designCache: {},
  _imageList: [],
  _layoutData: { issues: [], page_usage: [] },
  _verifyPollTimer: null,
  _mdModalPath: '',
  _currentPageNum: 1,
  _totalPageCount: 0,
};
