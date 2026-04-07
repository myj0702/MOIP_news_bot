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
    time_range = data.get("time_range", "")
    articles = data.get("articles", [])

    lines = [f"📰 *{keywords} 뉴스* ({date})"]
    if time_range:
        lines.append(f"🕐 수집 범위: {time_range}")
    lines.append("")

    for i, article in enumerate(articles, 1):
        title = article.get("title", "제목 없음")
        url = article.get("url", "")
        source = article.get("source", "")
        published = article.get("published", "")
        summary = article.get("summary", "")

        lines.append(f"*{i}. {title}*")
        meta = []
        if source:
            meta.append(f"출처: {source}")
        if published:
            meta.append(f"게재: {published}")
        if meta:
            lines.append(f"  {' | '.join(meta)}")
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


def split_and_send(header, articles_text_list):
    MAX_LEN = 4000
    messages = []
    current = header + "\n"

    for article_text in articles_text_list:
        if len(current) + len(article_text) > MAX_LEN:
            messages.append(current)
            current = ""
        current += article_text

    if current.strip():
        messages.append(current)

    results = []
    for i, msg in enumerate(messages, 1):
        if len(messages) > 1:
            msg = msg.rstrip() + f"\n\n_(({i}/{len(messages)}))_"
        result = send_message(msg)
        results.append(result)
    return results


def main():
    json_path = sys.argv[1] if len(sys.argv) > 1 else "news_data.json"

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID를 .env에 설정하세요.")
        sys.exit(1)

    data = load_news(json_path)
    date = data.get("date", "")
    keywords = data.get("keywords", "")
    time_range = data.get("time_range", "")
    articles = data.get("articles", [])

    header_lines = [f"📰 *{keywords} 뉴스* ({date})"]
    if time_range:
        header_lines.append(f"🕐 수집 범위: {time_range}")
    header_lines.append("")
    header = "\n".join(header_lines)

    article_texts = []
    for i, article in enumerate(articles, 1):
        lines = []
        title = article.get("title", "제목 없음")
        url = article.get("url", "")
        source = article.get("source", "")
        published = article.get("published", "")
        summary = article.get("summary", "")

        lines.append(f"*{i}. {title}*")
        meta = []
        if source:
            meta.append(f"출처: {source}")
        if published:
            meta.append(f"게재: {published}")
        if meta:
            lines.append(f"  {' | '.join(meta)}")
        if summary:
            lines.append(f"  {summary}")
        if url:
            lines.append(f"  [기사 링크]({url})")
        lines.append("")
        article_texts.append("\n".join(lines))

    results = split_and_send(header, article_texts)
    for r in results:
        print(f"텔레그램 발송 완료: message_id={r['result']['message_id']}")


if __name__ == "__main__":
    main()
