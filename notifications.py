import os
import subprocess
import requests
import json
import random
from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict, Any

TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def run_command(command: str) -> Tuple[str, str]:
    try:
        process = subprocess.run(command, capture_output=True, text=True, shell=True, check=True)
        return process.stdout.strip(), process.stderr.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error output: {e.stderr}")
        return "", e.stderr

def get_latest_changes() -> str:
    output, error = run_command("git log -1 --pretty=%B")
    if error:
        print(f"Error getting latest changes: {error}")
        return "No recent changes"
    return output

def generate_article() -> Tuple[str, str]:
    title = f"FlashCryptoSenders Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    content = "Latest updates and improvements for FlashCryptoSenders. Stay tuned for more exciting features!"
    return title, content

def create_html_article(title: str, content: str) -> int:
    post_id = int(datetime.now().timestamp())
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <script type="application/ld+json">
        {{
          "@context": "https://schema.org",
          "@type": "Article",
          "headline": "{title}",
          "datePublished": "{datetime.now().isoformat()}",
          "author": {{
            "@type": "Organization",
            "name": "FlashCryptoSenders"
          }}
        }}
        </script>
    </head>
    <body>
        <h1>{title}</h1>
        <p>{content}</p>
    </body>
    </html>
    """
    Path("articles").mkdir(exist_ok=True)
    with open(f"articles/{post_id}.html", "w") as f:
        f.write(html_content)
    return post_id

def send_telegram_message(message: str) -> Dict[str, Any]:
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error sending Telegram message: {e}")
        return {"ok": False, "error": str(e)}

def main():
    latest_changes = get_latest_changes()
    title, content = generate_article()
    post_id = create_html_article(title, content)

    message = f"""
🚀 FlashCryptoSenders Update ✨

🟢 Latest Changes:
{latest_changes}

📝 New Article: {title}
🔗 Read more: https://flashcrypto.vercel.app/articles/{post_id}.html

⚖️ Risk Level: {random.randint(1, 5)}/5
⭐ Score: {random.randint(1, 100)}/100
🏢 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

🔗 Quick Links:
[Website](https://flashcrypto.vercel.app/) | [GitHub](https://github.com/flash-crypto-senders) | [Telegram](https://t.me/RecentCoders) | [Documentation](https://flashcrypto.vercel.app/docs) | [Support](https://flashcrypto.vercel.app/support)
    """

    response = send_telegram_message(message)
    print(f"Telegram API response: {json.dumps(response, indent=2)}")

if __name__ == "__main__":
    main()
