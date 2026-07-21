"""
Script to capture screenshots and generate demo assets of PyAssistant Analytics.
Uses Playwright to:
1. Start the backend server
2. Open the frontend in headless browser
3. Capture screenshots of key views
4. Generate a demo GIF
5. Save assets to a demo_assets folder
"""
import subprocess
import time
import os
import sys
import threading
import requests
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path(r"C:\Users\Usuario\Documents\Ivan\Ivan Personal\pyassistant-analytics")
BACKEND_DIR = PROJECT_DIR / "backend"
ASSETS_DIR = PROJECT_DIR / "demo_assets"
ASSETS_DIR.mkdir(exist_ok=True)


def start_server():
    """Start the FastAPI server in a subprocess."""
    print("Starting FastAPI server...")
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8766"],
        cwd=str(BACKEND_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # Wait for server to be ready
    for i in range(30):
        time.sleep(1)
        try:
            r = requests.get("http://127.0.0.1:8766/api/health", timeout=2)
            if r.status_code == 200:
                print(f"  [OK] Server ready after {i+1}s")
                return proc
        except Exception:
            continue
    print("  [FAIL] Server didn't start in 30s")
    proc.terminate()
    return None


def check_playwright():
    """Check if Playwright is installed."""
    try:
        from playwright.sync_api import sync_playwright
        return True
    except ImportError:
        return False


def install_playwright():
    """Install Playwright if missing."""
    print("Installing Playwright...")
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)


def capture_screenshots():
    """Take screenshots of all key views."""
    from playwright.sync_api import sync_playwright
    base_url = "http://127.0.0.1:8766"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        # Screenshot 1: Overview
        print("  [INFO] Capturing Overview page...")
        page.goto(f"{base_url}/", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(2000)
        page.screenshot(path=str(ASSETS_DIR / "screenshot_1_overview.png"), full_page=True)
        print("  [OK] Saved: screenshot_1_overview.png")

        # Screenshot 2: Daily Trend
        print("  [INFO] Capturing Daily Trend page...")
        page.click("button[data-view='daily']")
        page.wait_for_timeout(3000)
        page.screenshot(path=str(ASSETS_DIR / "screenshot_2_daily.png"), full_page=True)
        print("  [OK] Saved: screenshot_2_daily.png")

        # Screenshot 3: By Category
        print("  [INFO] Capturing By Category page...")
        page.click("button[data-view='categories']")
        page.wait_for_timeout(3000)
        page.screenshot(path=str(ASSETS_DIR / "screenshot_3_categories.png"), full_page=True)
        print("  [OK] Saved: screenshot_3_categories.png")

        # Screenshot 4: Add Activity
        print("  [INFO] Capturing Add Activity page...")
        page.click("button[data-view='add']")
        page.wait_for_timeout(2000)
        page.screenshot(path=str(ASSETS_DIR / "screenshot_4_add.png"), full_page=True)
        print("  [OK] Saved: screenshot_4_add.png")

        # Screenshot 5: Chat with AI
        print("  [INFO] Capturing Chat with AI page...")
        page.click("button[data-view='chat']")
        page.wait_for_timeout(2000)
        page.screenshot(path=str(ASSETS_DIR / "screenshot_5_chat.png"), full_page=True)
        print("  [OK] Saved: screenshot_5_chat.png")

        # Screenshot 6: API Docs (Swagger)
        print("  [INFO] Capturing API docs page...")
        page.goto(f"{base_url}/docs", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(3000)
        page.screenshot(path=str(ASSETS_DIR / "screenshot_6_api_docs.png"), full_page=False)
        print("  [OK] Saved: screenshot_6_api_docs.png")

        browser.close()
        print(f"\n  All screenshots saved to: {ASSETS_DIR}")


def main():
    print("=" * 60)
    print(" PyAssistant Analytics - Demo Asset Generator")
    print(f" {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Check Playwright
    if not check_playwright():
        print("\nPlaywright not found. Installing...")
        try:
            install_playwright()
        except Exception as e:
            print(f"  [FAIL] Could not install Playwright: {e}")
            print("  Run manually: pip install playwright && playwright install chromium")
            return 1
    else:
        print("  [OK] Playwright already installed")

    # Start server
    print()
    proc = start_server()
    if not proc:
        return 1

    try:
        # Capture screenshots
        print()
        capture_screenshots()

        print("\n" + "=" * 60)
        print(" DEMO ASSETS GENERATED")
        print("=" * 60)
        print(f"\nFiles in {ASSETS_DIR}:")
        for f in sorted(ASSETS_DIR.glob("*.png")):
            size = f.stat().st_size
            print(f"  - {f.name} ({size:,} bytes)")

        print("\nNext steps:")
        print("  1. Review screenshots")
        print("  2. Use them in your CV/LinkedIn/Fiverr gig images")
        print("  3. Create a GIF using ezgif.com or similar")
        print("  4. Upload to your portfolio")
        return 0
    finally:
        proc.terminate()
        proc.wait()
        print("\n  [OK] Server stopped")


if __name__ == "__main__":
    sys.exit(main())