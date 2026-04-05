import json
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def load_news(json_path="news_data.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def format_message(data):
    date = data.get("date", "")
    keywords = data.get("keywords", "")
    articles = data.get("articles", [])

    lines = [f"📰 *{keywords} 뉴스* ({date})\n"]

    for i, article in enumerate(articles, 1):
        title = article.get("title", "제목 없음")
        url = article.get("url", "")
        summary = article.get("summary", "")
        lines.append(f"*{i}. {title}*")
        if summary:
            lines.append(f"  {summary}")
        if url:
            lines.append(f"  [기사 링크]({url})")
        lines.append("")

    return "\n".join(lines)


def send_message(text):
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    response = requests.post(f"{TELEGRAM_API_URL}/sendMessage", json=payload)
    response.raise_for_status()
    return response.json()


def main():
    json_path = sys.argv[1] if len(sys.argv) > 1 else "news_data.json"

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID를 .env에 설정하세요.")
        sys.exit(1)

    data = load_news(json_path)
    message = format_message(data)
    result = send_message(message)
    print(f"텔레그램 발송 완료: message_id={result['result']['message_id']}")


if __name__ == "__main__":
    main()
