from image_gen import scan_placeholders

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
