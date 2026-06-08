# 🏦 Multilingual Banking TTS System

A **FastAPI**-powered text-to-speech service that generates spoken queue announcements for banking environments. Supports **5 languages** with neural voices via Microsoft Edge-TTS.

---

## ✨ Features

- 🌐 **5 languages** — English, Bangla, Japanese, German, Spanish
- 🎙 **Neural voices** — male & female options per language (Microsoft Edge-TTS)
- ⚙ **Prosody control** — configurable speech rate, pitch, and volume
- ⚡ **Async MP3 generation** — non-blocking synthesis with instant audio URL
- 🧹 **Auto-cleanup** — generated audio files expire after a configurable TTL
- 🛡 **Rate limiting** — per-IP request throttling via SlowAPI
- 📄 **Interactive UI** — built-in web demo at `http://127.0.0.1:8000/`
- 📖 **Auto docs** — Swagger UI at `/docs`, ReDoc at `/redoc`

---

## 🗂 Project Structure

```
Multilingual-TTS-System/
├── app/
│   ├── core/               # Config, logging, exceptions, constants
│   ├── modules/
│   │   ├── announcement/   # POST /api/v1/announcements
│   │   ├── health/         # GET  /api/v1/health
│   │   ├── tts/            # Edge-TTS provider & synthesis logic
│   │   └── voice/          # GET  /api/v1/voices
│   ├── shared/             # Middleware, helpers, base responses
│   ├── static/
│   │   ├── index.html      # Web demo UI
│   │   └── generated_audio/  # Runtime MP3 output (git-ignored)
│   └── main.py             # FastAPI app factory & entry point
├── tests/
├── .env                    # Local config (git-ignored)
├── example.env             # Env template to commit
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone & install

```bash
git clone https://github.com/FaisalAhmedBijoy/Multilingual-TTS-System.git
cd Multilingual-TTS-System

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp example.env .env
# Edit .env as needed — defaults work out of the box
```

### 3. Run

```bash
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/** in your browser.

---

## 🔌 API Reference

### Generate Announcement

```http
POST /api/v1/announcements
Content-Type: application/json

{
  "token":    "A13",
  "counter":  "5",
  "language": "en",
  "gender":   "female",
  "rate":     1.0,
  "pitch":    0,
  "volume":   1.0
}
```

**Supported languages:**

| Code | Language | Female Voice             | Male Voice            |
|------|----------|--------------------------|-----------------------|
| `en` | English  | en-US-AriaNeural         | en-US-GuyNeural       |
| `bn` | Bangla   | bn-BD-NabanitaNeural     | bn-BD-PradeepNeural   |
| `ja` | Japanese | ja-JP-NanamiNeural       | ja-JP-KeitaNeural     |
| `de` | German   | de-DE-KatjaNeural        | de-DE-ConradNeural    |
| `es` | Spanish  | es-ES-ElviraNeural       | es-ES-AlvaroNeural    |

**Response:**

```json
{
  "success": true,
  "data": {
    "token": "A13",
    "counter": "5",
    "language": "en",
    "voice": "en-US-AriaNeural",
    "announcement_text": "Token A 1 3, please proceed to counter 5.",
    "audio_url": "/static/generated_audio/abc123.mp3",
    "filename": "abc123.mp3"
  }
}
```

### Other Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/` | Web demo UI |
| `GET`  | `/api/v1/health` | Health check |
| `GET`  | `/api/v1/voices` | List all supported voices |
| `GET`  | `/docs` | Swagger UI |
| `GET`  | `/redoc` | ReDoc |

---

## ⚙ Configuration (`.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | `Banking TTS System` | Application name |
| `APP_VERSION` | `1.0.0` | Version string |
| `DEBUG` | `true` | Enable debug mode & auto-reload |
| `HOST` | `0.0.0.0` | Bind address |
| `PORT` | `8000` | Bind port |
| `ALLOWED_ORIGINS` | `["http://localhost:8000", ...]` | CORS origins |
| `AUDIO_OUTPUT_DIR` | `static/generated_audio` | MP3 output directory |
| `AUDIO_TTL_SECONDS` | `300` | Audio file lifetime (seconds) |
| `DEFAULT_VOICE_GENDER` | `female` | Fallback voice gender |
| `DEFAULT_SPEECH_RATE` | `1.0` | Fallback speech rate |
| `LOG_LEVEL` | `INFO` | Logging level |
| `RATE_LIMIT_PER_MINUTE` | `30` | Max requests per IP per minute |

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 🛠 Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** — async web framework
- **[Edge-TTS](https://github.com/rany2/edge-tts)** — Microsoft neural TTS (no API key required)
- **[Uvicorn](https://www.uvicorn.org/)** — ASGI server
- **[Pydantic v2](https://docs.pydantic.dev/)** — data validation
- **[SlowAPI](https://github.com/laurentS/slowapi)** — rate limiting

---

## 📄 License

MIT
