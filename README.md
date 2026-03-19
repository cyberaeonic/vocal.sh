# 🔊 VOCAL.SH — Real-Time Auditory Intelligence for Live Technical Defense

> *"I never had to look at the logs."*

**VOCAL.SH** is a voice-first security middleware for the terminal. It transforms the silent, text-heavy terminal into a high-speed **auditory defense environment** by parsing live system logs and speaking critical security alerts with human-like clarity — powered by the **Murf Falcon TTS API** at under 130ms latency.

Built for **SOC analysts**, **CTF competitors**, and **developers** who need to stay in flow state while defending a live system.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎧 **Eyes-Free Alerting** | Hear threats without switching windows |
| ⚡ **Murf Falcon TTS** | < 130ms voice response latency |
| 🔍 **Brute Force Detection** | Fires on 5+ rapid failed SSH logins |
| 🖥️ **Rich TUI** | Clean, minimal terminal UI |
| 🔒 **Secure by Design** | API key lives in `.env`, never in code |

---

## 📋 Prerequisites

- Python **3.10+**
- A [Murf AI](https://murf.ai) account with a **Falcon API key**
- Windows, macOS, or Linux

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/vocal-sh.git
cd vocal-sh
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `rich` — for the terminal UI
- `requests` — for the Murf Falcon API calls
- `python-dotenv` — for secure API key loading
- `pygame` — for invisible in-terminal audio playback

### 3. Configure your API key

Create a `.env` file in the project root (it is already listed in `.gitignore` — it will **never** be pushed to GitHub):

```bash
# .env
MURF_API_KEY=your_murf_falcon_api_key_here
```

> **Get your key:** Log in to [Murf AI → Developer Settings](https://murf.ai) → Generate API Key.

---

## ▶️ Running the Demo

Open **two terminal windows** side by side.

### Window 1 — Start the Daemon

```bash
python vocal.py
```

You will see the live defense panel appear:

```
╭──────────────────────────────────────────────────────────╮
│ VOCAL.SH — Active Defense Daemon                         │
│ Status: Online │ Model: Murf Falcon │ Latency: <130ms   │
│                                                          │
│ Listening for anomalies... 🎧                            │
╰──────────────────────────────────────────────────────────╯
```

### Window 2 — Simulate a Brute Force Attack

```bash
python simulate_attack.py
```

This injects **5 rapid failed SSH login attempts** into the mock log, simulating a real attacker.

### What happens next (automatically)

1. The daemon detects the 5th failed login
2. It prints: `🚨 THREAT DETECTED — 5 Rapid Failed Logins from 192.168.1.55`
3. The payload is dispatched to **Murf Falcon API**
4. Within milliseconds, your speakers announce:

> *"Security Alert: Brute force detected from IP 192.168.1.55. Action suggested: Lock port 22."*

---

## 📁 Project Structure

```
vocal-sh/
├── vocal.py            # Main daemon — tails logs & triggers TTS
├── simulate_attack.py  # Injects fake brute-force SSH logs for demo
├── mock_auth.log       # Simulated log file (auto-created)
├── .env                # Your Murf API key (never committed to git)
├── .gitignore          # Excludes .env, logs, and audio files
└── requirements.txt    # Python dependencies
```

---

## 🔐 Security Note

Your API key is loaded exclusively from the `.env` file at runtime using `python-dotenv`. The key is **never hardcoded** in any source file. The `.gitignore` blocks the `.env` file from being pushed to GitHub.

---

## 🛠️ Customization

### Change the alert threshold
In `vocal.py`, find and edit:
```python
if failed_attempts >= 5:   # Change 5 to any number
```

### Change the voice
In `vocal.py`, update the `voiceId` field:
```python
"voiceId": "en-US-marcus",  # Try: "en-US-cooper", "en-US-natalie"
```
Browse all available voices at the [Murf Voice Library](https://murf.ai/voices).

### Watch a real log file
Replace `LOG_FILE` in `vocal.py`:
```python
LOG_FILE = Path("/var/log/auth.log")   # Linux live SSH log
```

---

## 📦 Dependencies

```
rich==13.7.0
requests==2.31.0
python-dotenv==1.0.1
pygame==2.6.1
```

---

## 🏆 Built For

**Murf AI Hackathon** — *"Live Attack" Demo Category*

Demonstrating that **Murf Falcon's 130ms latency** is the only reason a real-time auditory security layer is possible. This is not a notification system — it is an **auditory layer for the modern SOC analyst**.

---

## 📄 License

MIT License — free to use, modify, and distribute.
