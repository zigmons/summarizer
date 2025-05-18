# ✂️ Summarizer

**Summarizer** is a cross-platform Python tray app that monitors your clipboard and, on demand, sends the copied text to the Gemini model (via Google Vertex AI) to generate a quick summary, displayed in a native window.

---

## 📋 Features

- Icon in the taskbar (Windows - In development) / menu bar (macOS).
- Menu with actions:
- **Summarize Clipboard** — generates and displays a summary of the copied text.
- **Configure API Key** — opens a window to save your Google API Key.
- **About** — displays the current version of the app.
- **Exit** — closes the app.
- Tkinter-based configuration window to save your API Key in `~/.summarizer_config.json`.
- Asynchronous calls (threading) to avoid crashing the interface while generating the summary.

---

## 🚀 Prerequisites

- **Python 3.12+** 
- **macOS** (10.15+) or **Windows 10+** 
- **Google Cloud API Key** enabled for Vertex AI (Gemini) 
- **pip** 

---

## 🔧 Installation

1. **Clone this repository** 
```bash
git clone https://github.com/zigmons/summarizer
cd summarizer