import json
import os
import subprocess
import sys
from datetime import datetime
from dotenv import load_dotenv
from jinja2 import Template

load_dotenv()

GITHUB_REPO_PATH = os.getenv("GITHUB_REPO_PATH", "./docs")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>지식재산 뉴스 by Claude Code CLI - {{ date }}</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
        .meta { color: #666; font-size: 0.9em; margin-bottom: 20px; }
        .time-range { display: inline-block; background: #007bff; color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.85em; margin-top: 5px; }
        .article { background: white; padding: 15px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .article h2 { margin: 0 0 8px 0; font-size: 1.1em; }
        .article h2 a { color: #007bff; text-decoration: none; }
        .article h2 a:hover { text-decoration: underline; }
        .article .article-meta { color: #888; font-size: 0.85em; margin-bottom: 8px; }
        .article .article-meta span { margin-right: 12px; }
        .article .summary { color: #555; margin: 0; line-height: 1.6; white-space: pre-line; }
        footer { text-align: center; color: #999; margin-top: 30px; font-size: 0.8em; }
    </style>
</head>
<body>
    <h1>지식재산 뉴스 by Claude Code CLI</h1>
    <div class="meta">
        <div>{{ date }}</div>
        {% if time_range %}
        <span class="time-range">{{ time_range }}</span>
        {% endif %}
    </div>
    {% for article in articles %}
    <div class="article">
        <h2><a href="{{ article.url }}" target="_blank">{{ article.title }}</a></h2>
        <div class="article-meta">
            {% if article.source %}<span>📌 {{ article.source }}</span>{% endif %}
            {% if article.published %}<span>🕐 {{ article.published }}</span>{% endif %}
        </div>
        <p class="summary">{{ article.summary }}</p>
    </div>
    {% endfor %}
    <footer>자동 생성 by Claude Code CLI</footer>
</body>
</html>"""


def load_news(json_path="news_data.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_html(data):
    template = Template(HTML_TEMPLATE)
    return template.render(**data)


def save_html(html_content, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML 생성 완료: {output_path}")
    return output_path


def git_push(repo_path, date):
    commands = [
        ["git", "add", "."],
        ["git", "commit", "-m", f"뉴스 업데이트: {date}"],
        ["git", "push", "origin", GITHUB_BRANCH],
    ]
    for cmd in commands:
        result = subprocess.run(
            cmd, cwd=repo_path, capture_output=True, text=True, encoding="utf-8"
        )
        if result.returncode != 0 and "nothing to commit" not in result.stderr:
            print(f"Git 명령 실패: {' '.join(cmd)}")
            print(result.stderr)
            return False
    print("GitHub Pages push 완료")
    return True


def main():
    json_path = sys.argv[1] if len(sys.argv) > 1 else "news_data.json"

    data = load_news(json_path)
    html = generate_html(data)
    save_html(html, GITHUB_REPO_PATH)
    git_push(GITHUB_REPO_PATH, data.get("date", datetime.now().strftime("%Y-%m-%d")))


if __name__ == "__main__":
    main()
