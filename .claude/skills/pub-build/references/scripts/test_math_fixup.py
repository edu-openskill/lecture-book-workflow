from typst_builder import fix_math_typst

def test_align_block_converted_to_cases_or_aligned():
    # Pandoc이 align을 그대로 흘리면 Typst가 못 읽음 → 보정
    pandoc_out = '$ \\begin{aligned} a &= b \\\\ c &= d \\end{aligned} $'
    out = fix_math_typst(pandoc_out)
    assert '\\begin' not in out
    assert 'aligned' not in out or '&' not in out

def test_xrightarrow_becomes_arrow():
    out = fix_math_typst('$ x \\xrightarrow{f} y $')
    assert 'xrightarrow' not in out

def test_plain_math_untouched():
    src = '$f prime (x) = 0$'
    assert fix_math_typst(src) == src
