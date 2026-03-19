import time
import os
import requests
import tempfile
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import pygame

# -----------------------------------------------------------------------
# Load .env from the SAME directory as this script, regardless of where
# the terminal's CWD is. This fixes the "API Key not set" fallback.
# -----------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).parent.resolve()
load_dotenv(dotenv_path=SCRIPT_DIR / ".env")

console = Console()

MURF_API_KEY = os.getenv("MURF_API_KEY")
LOG_FILE     = SCRIPT_DIR / "mock_auth.log"

# -----------------------------------------------------------------------
# Murf Falcon TTS – uses the STREAMING endpoint (correct URL from docs)
# https://global.api.murf.ai/v1/speech/stream
# -----------------------------------------------------------------------
def generate_and_play_audio(text: str):
    if not MURF_API_KEY:
        console.print("\n[bold yellow]⚠ API Key not found in .env! Using Windows fallback TTS.[/bold yellow]")
        os.system(
            f'PowerShell -Command "Add-Type -AssemblyName System.Speech; '
            f'(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\');"'
        )
        return

    url = "https://api.murf.ai/v1/speech/stream"

    headers = {
        "Content-Type": "application/json",
        "api-key": MURF_API_KEY,
    }

    payload = {
        "voiceId"       : "en-US-marcus",
        "style"         : "Conversational",
        "text"          : text,
        "rate"          : 0,
        "pitch"         : 0,
        "sampleRate"    : 48000,
        "format"        : "MP3",
        "channelType"   : "MONO",
        "model"         : "FALCON",
        "locale"        : "en-US",
        "encodeToBase64": False,
    }

    console.print("[bold cyan]⚡ Sending payload to Murf Falcon API...[/bold cyan]")
    t0 = time.time()

    try:
        response = requests.post(url, json=payload, headers=headers, stream=True, timeout=10)

        latency_ms = (time.time() - t0) * 1000

        console.print(f"[dim]HTTP Status: {response.status_code}[/dim]")

        if response.status_code == 200:
            console.print(f"[bold green]✔ Audio received from Murf Falcon in {latency_ms:.0f}ms[/bold green]")

            # Write the streaming audio to a temp file then play it
            tmp = tempfile.NamedTemporaryFile(
                suffix=".mp3", delete=False, dir=SCRIPT_DIR
            )
            for chunk in response.iter_content(chunk_size=4096):
                if chunk:
                    tmp.write(chunk)
            tmp.close()

            console.print(f"[dim]Saved to: {tmp.name}[/dim]")
            # Play invisibly via pygame — no media player window on screen
            pygame.mixer.init()
            pygame.mixer.music.load(tmp.name)
            pygame.mixer.music.play()
            # Wait for playback to finish before returning
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.quit()
        else:
            # Print full response body so we can see exactly what Murf returned
            console.print(f"[bold red]Murf API Error {response.status_code}:[/bold red]")
            console.print(f"[red]{response.text}[/red]")

    except requests.exceptions.Timeout:
        console.print("[bold red]Request timed out. Check network or API key.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/bold red] {e}")


# -----------------------------------------------------------------------
# Log tail & attack detection
# -----------------------------------------------------------------------
def tail_log():
    # Ensure the log file exists
    LOG_FILE.touch(exist_ok=True)

    with open(LOG_FILE, "r") as f:
        f.seek(0, 2)  # seek to end – only watch NEW lines

        failed_attempts = 0
        target_ip       = "UNKNOWN"

        console.print(Panel.fit(
            Text.from_markup(
                "[bold green]VOCAL.SH — Active Defense Daemon[/bold green]\n"
                "[dim]Status: Online │ Model: Murf Falcon │ Latency Target: <130ms[/dim]\n\n"
                "Listening for anomalies... 🎧"
            ),
            border_style="green",
        ))

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue

            console.print(f"[dim]{line.strip()}[/dim]")

            # ── Threat rule: 5 failed SSH passwords → brute force ──────
            if "Failed password" in line:
                failed_attempts += 1

                # Extract IP address from the log line
                for token in line.split():
                    if token.count(".") == 3 and token[0].isdigit():
                        target_ip = token
                        break

                if failed_attempts >= 5:
                    alert = (
                        f"Security Alert: Brute force detected from I.P. {target_ip}. "
                        f"Action suggested: Lock port 22."
                    )
                    console.print(f"\n[bold red]🚨 THREAT DETECTED — 5 Rapid Failed Logins from {target_ip}[/bold red]")
                    console.print(f"[bold yellow]TTS Payload:[/bold yellow] {alert}\n")

                    generate_and_play_audio(alert)
                    failed_attempts = 0  # reset counter after alert

if __name__ == "__main__":
    try:
        tail_log()
    except KeyboardInterrupt:
        console.print("\n[bold red]Daemon stopped.[/bold red]")
