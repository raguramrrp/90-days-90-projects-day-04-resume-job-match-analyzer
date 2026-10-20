"""Visual Screenshot Capture Engine for Resume-Job Match Analyzer.

Captures high-resolution, genuine demonstration screenshots using Headless Chrome & CDP.
Day 4 — 90 Days 90 Projects Challenge.
"""

import os
import sys
import subprocess
import time
import shutil
import json
import base64
import asyncio
import requests
import websockets

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
TEMP_DIR = os.path.join(os.environ.get("LOCALAPPDATA", "C:\\Temp"), "Temp")


def take_static_screenshot(url: str, output_filename: str, width: int = 1280, height: int = 900):
    """Capture static web page screenshot using Chrome headless CLI."""
    os.makedirs(TEMP_DIR, exist_ok=True)
    temp_target = os.path.join(TEMP_DIR, output_filename)
    if os.path.exists(temp_target):
        os.remove(temp_target)

    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        f"--window-size={width},{height}",
        f"--screenshot={temp_target}",
        url,
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=25)
    time.sleep(1)

    final_target = os.path.join(SCREENSHOTS_DIR, output_filename)
    if os.path.exists(temp_target):
        shutil.copy2(temp_target, final_target)
        os.remove(temp_target)
        print(f"[SUCCESS] Captured screenshot: {final_target} ({os.path.getsize(final_target):,} bytes)")
        return True
    else:
        print(f"[WARNING] Could not find temporary screenshot at {temp_target}")
        return False


async def capture_cdp_screenshot(url: str, output_path: str, width: int = 1400, height: int = 900, wait_seconds: int = 6):
    """Capture dynamic interactive dashboard view via Chrome DevTools Protocol."""
    chrome_proc = subprocess.Popen(
        [
            CHROME_PATH,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--remote-debugging-port=9223",
            f"--window-size={width},{height}",
            url,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(2)

    try:
        targets = requests.get("http://localhost:9223/json").json()
        target = next((t for t in targets if t.get("type") == "page"), targets[0])
        ws_url = target["webSocketDebuggerUrl"]

        async with websockets.connect(ws_url) as ws:
            # Let Streamlit WebSockets mount completely
            await asyncio.sleep(wait_seconds)

            msg = {"id": 1, "method": "Page.captureScreenshot", "params": {"format": "png"}}
            await ws.send(json.dumps(msg))
            resp = await ws.recv()
            data = json.loads(resp)
            img_b64 = data["result"]["data"]
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(img_b64))
            print(f"[SUCCESS] Captured CDP screenshot: {output_path} ({os.path.getsize(output_path):,} bytes)")
            return True
    finally:
        chrome_proc.terminate()
        chrome_proc.wait()


def main():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # 1. Capture HTML Scorecard Report
    html_report_path = os.path.join(REPORTS_DIR, "ats_scorecard_sample.html")
    if not os.path.exists(html_report_path):
        print("[*] Generating sample HTML report first...")
        subprocess.run([
            os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe"),
            os.path.join(BASE_DIR, "scripts", "run_cli_analysis.py"),
            "--resume", os.path.join(BASE_DIR, "data", "sample_resumes", "alex_chen_data_scientist.pdf"),
            "--jd", os.path.join(BASE_DIR, "data", "sample_jds", "ai_data_scientist_job_description.txt"),
            "--export-html", html_report_path
        ], check=True)

    file_url = f"file:///{html_report_path.replace(os.sep, '/')}"
    print(f"[*] Capturing HTML scorecard screenshot from {file_url}...")
    take_static_screenshot(file_url, "02_ats_scorecard_report.png", width=1280, height=1100)

    # 2. Launch Streamlit on port 8507 and capture live dashboard
    python_exe = os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe")
    port = 8507
    print(f"[*] Launching Streamlit on port {port}...")
    st_proc = subprocess.Popen(
        [python_exe, "-m", "streamlit", "run", "src/app.py", f"--server.port={port}", "--server.headless=true"],
        cwd=BASE_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(5)

    try:
        dash_shot = os.path.join(SCREENSHOTS_DIR, "01_streamlit_dashboard_overview.png")
        print("[*] Capturing Streamlit dashboard overview via CDP...")
        asyncio.run(capture_cdp_screenshot(f"http://localhost:{port}", dash_shot, width=1400, height=950, wait_seconds=6))
    finally:
        st_proc.terminate()
        st_proc.wait()
        print("[*] Streamlit server terminated.")


if __name__ == "__main__":
    main()
