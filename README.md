# 📄 DocAI | High-Fidelity PDF Converter

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

Docer is a production-ready, minimalist web application for high-fidelity PDF watermark remover. It uses a smart reflow pipeline to ensure your documents look perfect after removing watermarks.

## 🚀 Deployment to Render

This project is optimized for [Render](https://render.com).

### Option 1: One-Click Deploy (Recommended)
1. Push this code to a GitHub repository.
2. Log in to Render.
3. Click **New +** > **Blueprint**.
4. Connect your repo and Render will automatically detect `render.yaml`.

### Option 2: Manual Web Service
1. **Service Type**: Web Service
2. **Runtime**: `Python 3` OR `Docker` (Dockerfile is included)
3. **Build Command**: `pip install -r requirements.txt && apt-get update && apt-get install -y libreoffice`
4. **Start Command**: `python -m app.main`
5. **Environment Variables**:
   - `STORAGE_PROVIDER`: `local` (default) or `supabase`
   - `PORT`: `8000`

## 🛠️ Local Development

1. **Clone & Install**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Environment**:
   ```bash
   cp .env.example .env
   ```
3. **Run**:
   ```bash
   python -m app.main
   ```

## 🏗️ Architecture

- **Backend**: FastAPI
- **Frontend**: Vanilla JS (0 Dependencies)
- **Engine**: pdf2docx + LibreOffice Headless
- **Storage**: Pluggable (Local / Supabase Storage)

## 🔒 Security

- 100MB Upload Limit
- Auto-cleanup of temp files (24h)
- UUID-based isolation
- Signed URLs for Supabase mode
