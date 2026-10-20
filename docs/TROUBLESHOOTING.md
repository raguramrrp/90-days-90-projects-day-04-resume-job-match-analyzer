# Troubleshooting Guide

This guide covers common questions, error messages, and solutions when installing or running the **AI-Powered Resume–Job Compatibility Analyzer** on Windows.

---

## 1. Setup & Installation Issues

### Error: `No compatible Python installation found on system PATH`
- **Cause:** Python is not installed or not added to your system environment `PATH`.
- **Solution:** 
  1. Download and install Python 3.10, 3.11, or 3.12 from [python.org](https://www.python.org/).
  2. During installation, make sure to check the box: **"Add Python to PATH"**.
  3. Re-run `setup.bat`.

### Error: `Failed to create virtual environment`
- **Cause:** Permission restrictions in the workspace directory or an existing corrupted `.venv` folder.
- **Solution:** 
  1. Delete the existing `.venv` folder: `rmdir /s /q .venv`
  2. Re-run `setup.bat`.

---

## 2. Runtime & Document Parsing Issues

### Error: `DocumentParseError: PDF extracted text was empty. The file may be image-only (scanned)`
- **Cause:** The uploaded PDF is a scanned image or screenshot rather than a digital PDF containing selectable text.
- **Solution:** 
  - Standard ATS parsers cannot read scanned images without OCR. Export your resume from Word, Google Docs, Canva, or LaTeX as a digital PDF with selectable text, or paste your plain text into the editor.

### Error: `Unsupported file format`
- **Cause:** Uploaded an unsupported file extension (e.g., `.pages`, `.rtf`, `.odt`, `.zip`).
- **Solution:** 
  - Convert your document to `.pdf`, `.docx`, or `.txt`.

### Warning: `Total weight is X%. Normalizing to 100%.`
- **Cause:** In the sidebar custom scoring sliders, the sum of weights does not equal 100.
- **Solution:** 
  - The application automatically normalizes each slider proportionally so your final score remains strictly on a 0–100% scale.

---

## 3. Server & Network Issues

### Error: `Port 8501 is already in use`
- **Cause:** Another Streamlit application or background task is occupying port 8501.
- **Solution:** 
  - Run Streamlit on an alternate port:
    ```cmd
    .\.venv\Scripts\streamlit run src/app.py --server.port=8502
    ```
  - Or terminate the existing process using PowerShell:
    ```powershell
    Get-Process python | Stop-Process -Force
    ```
