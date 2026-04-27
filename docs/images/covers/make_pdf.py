#!/usr/bin/env python3
"""v2~v11 목업 HTML을 스크린샷 → PDF로 합치는 스크립트"""
import subprocess, time, os, sys, signal
from pathlib import Path

BASE = Path(__file__).parent
PDF_SRC = BASE / "pdf-src"
PDF_SRC.mkdir(exist_ok=True)

# 캡처 대상 (v2~v11, v8은 없음)
VERSIONS = ["v2", "v3", "v4", "v5", "v6", "v7", "v9", "v10", "v11"]

# 1) HTTP 서버 시작
print("HTTP 서버 시작...")
server = subprocess.Popen(
    [sys.executable, "-m", "http.server", "8773"],
    cwd=str(BASE),
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
time.sleep(1)

try:
    # 2) Playwright로 스크린샷
    print("Playwright로 스크린샷 캡처 중...")
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="chrome")
        page = browser.new_page(viewport={"width": 1920, "height": 1080})

        for ver in VERSIONS:
            fname = f"mockup-{ver}.html" if ver != "v1" else "mockup.html"
            url = f"http://localhost:8773/{fname}"
            out = PDF_SRC / f"{ver}.png"

            print(f"  {ver} → {out.name} ...", end=" ", flush=True)
            page.goto(url, wait_until="networkidle")
            time.sleep(0.5)  # 폰트 로딩 대기
            page.screenshot(path=str(out), full_page=True, type="png")
            print("OK")

        browser.close()

    # 3) PNG → PDF (Pillow)
    print("\nPNG → PDF 변환 중...")
    from PIL import Image

    images = []
    for ver in VERSIONS:
        img_path = PDF_SRC / f"{ver}.png"
        if img_path.exists():
            img = Image.open(img_path).convert("RGB")
            images.append(img)
            print(f"  {ver}: {img.size[0]}x{img.size[1]}")

    if images:
        pdf_path = BASE / "cover-mockups-v2-v11.pdf"
        images[0].save(
            str(pdf_path),
            "PDF",
            save_all=True,
            append_images=images[1:],
            resolution=150,
        )
        print(f"\nPDF 생성 완료: {pdf_path}")
        print(f"  총 {len(images)} 페이지, {pdf_path.stat().st_size / 1024 / 1024:.1f} MB")
    else:
        print("이미지가 없습니다!")

finally:
    server.terminate()
    server.wait()
    print("HTTP 서버 종료")
