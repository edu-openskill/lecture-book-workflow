from pathlib import Path
from image_gen import scan_placeholders, parse_thread_id, find_generated_image, replace_placeholder

SAMPLE = '''본문.

<!-- [GEMINI PROMPT: 03_rag-flow]
path: assets/CH03/03_rag-flow.png
A minimalist diagram of RAG pipeline.
Style: architecture-infographic
-->
![RAG 파이프라인](../assets/CH03/03_rag-flow.png)
*그림 3-2: RAG 파이프라인의 전체 흐름*

다음 본문.'''

def test_scan_finds_one():
    phs = scan_placeholders(SAMPLE)
    assert len(phs) == 1

def test_scan_fields():
    ph = scan_placeholders(SAMPLE)[0]
    assert ph.id == '03_rag-flow'
    assert ph.path == 'assets/CH03/03_rag-flow.png'
    assert 'RAG pipeline' in ph.prompt
    assert ph.caption == '*그림 3-2: RAG 파이프라인의 전체 흐름*'

def test_image_prompt_alias():
    text = SAMPLE.replace('GEMINI PROMPT', 'IMAGE PROMPT')
    assert len(scan_placeholders(text)) == 1

def test_parse_thread_id():
    out = '\n'.join([
        '{"type":"thread.started","thread_id":"019ef6f7-3ff9-7a41-97cf-c80126da856d"}',
        '{"type":"turn.started"}',
        '{"type":"turn.completed"}',
    ])
    assert parse_thread_id(out) == '019ef6f7-3ff9-7a41-97cf-c80126da856d'

def test_parse_thread_id_none():
    assert parse_thread_id('비-JSON 출력\n{"type":"turn.started"}') is None

def test_find_generated_image(tmp_path):
    tid = 'abc-123'
    d = tmp_path / 'generated_images' / tid
    d.mkdir(parents=True)
    png = d / 'ig_deadbeef.png'
    png.write_bytes(b'\x89PNG')
    assert find_generated_image(tid, codex_home=tmp_path) == png

def test_find_generated_image_missing(tmp_path):
    assert find_generated_image('nope', codex_home=tmp_path) is None

def test_replace_emits_img_tag():
    ph = scan_placeholders(SAMPLE)[0]
    out = replace_placeholder(SAMPLE, ph)
    assert '<!--' not in out
    assert '<img src="../assets/CH03/03_rag-flow.png" width="720"' in out
    assert '*그림 3-2: RAG 파이프라인의 전체 흐름*' in out
