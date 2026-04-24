"""
구글 뉴스 RSS 수집기: 한국어/영어 IP 키워드를 일괄 검색해 news_data.json에 저장한다.

특징:
  - API 키 불필요 (https://news.google.com/rss/search)
  - 쿼리에 when:1d / when:3d 자동 부착으로 RSS 단계 1차 시간 필터
  - date_filter.calc_cutoff_date() 재사용하여 평일/주말 기준 일치
  - 저작권/면세점 키워드 제외 (CLAUDE.md 룰)
  - URL/제목 기반 중복 제거
  - news_data.json이 이미 있으면 기존 articles와 병합 (기존 우선)
"""

import html
import json
import os
import re
import sys
import time
from datetime import datetime
from urllib.parse import quote_plus

import feedparser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from date_filter import calc_cutoff_date

KOREAN_QUERIES = [
    "특허",
    "상표",
    "디자인권",
    "발명",
    "지식재산",
    "침해",
    "분쟁",
    "소송",
    "영업비밀",
    "부정경쟁",
    "기술유출",
    "라이선스 OR 로열티",
    "심판",
    "표준특허",
    "위조 OR 짝퉁",
]

ENGLISH_QUERIES = [
    "patent Korea",
    "trademark Korea",
    "IP litigation Korea",
    "trade secret Korea",
    "NPE patent troll",
    "WIPO PCT",
    "USPTO Korea",
    "ITC 337 Korea",
    "SEP FRAND",
    "semiconductor AI patent",
]

KOREAN_LOCALE = "hl=ko&gl=KR&ceid=KR:ko"
ENGLISH_LOCALE = "hl=en-US&gl=US&ceid=US:en"

BLOCKED_KEYWORDS = [
    "저작권", "저작물", "저작자", "copyright",
    "면세점", "면세 특허", "duty-free", "duty free",
]

DOMAIN_TO_SOURCE = {
    "yna.co.kr": "연합뉴스",
    "yonhapnews.co.kr": "연합뉴스",
    "newsis.com": "뉴시스",
    "news1.kr": "뉴스1",
    "etnews.com": "전자신문",
    "dt.co.kr": "디지털타임스",
    "hankyung.com": "한국경제",
    "mk.co.kr": "매일경제",
    "sedaily.com": "서울경제",
    "fnnews.com": "파이낸셜뉴스",
    "heraldcorp.com": "헤럴드경제",
    "asiae.co.kr": "아시아경제",
    "edaily.co.kr": "이데일리",
    "mt.co.kr": "머니투데이",
    "chosun.com": "조선일보",
    "joongang.co.kr": "중앙일보",
    "donga.com": "동아일보",
    "hani.co.kr": "한겨레",
    "khan.co.kr": "경향신문",
    "korea.kr": "대한민국 정책브리핑",
    "ipdaily.co.kr": "IP데일리",
    "lawtimes.co.kr": "법률신문",
    "kipo.go.kr": "특허청",
    "reuters.com": "Reuters",
    "bloomberg.com": "Bloomberg",
    "ft.com": "Financial Times",
    "wsj.com": "Wall Street Journal",
    "nytimes.com": "The New York Times",
    "iam-media.com": "IAM Media",
    "managingip.com": "Managing IP",
    "ipwatchdog.com": "IPWatchdog",
    "lexology.com": "Lexology",
}


def build_rss_url(query, locale, when_operator):
    q = f"{query} {when_operator}".strip()
    return f"https://news.google.com/rss/search?q={quote_plus(q)}&{locale}"


def calc_when_operator():
    """오늘 요일에 따라 when:Nd 연산자 결정. cutoff와 같은 룰을 따른다."""
    today = datetime.now().date()
    cutoff = calc_cutoff_date(today)
    days = (today - cutoff).days
    return f"when:{max(days, 1)}d"


def strip_html(s):
    if not s:
        return ""
    text = re.sub(r"<[^>]+>", "", s)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def parse_pubdate(entry):
    pp = entry.get("published_parsed") or entry.get("updated_parsed")
    if not pp:
        return ""
    return time.strftime("%Y-%m-%d %H:%M", pp)


def extract_title_source(raw_title):
    """구글 뉴스 RSS title은 '기사제목 - 출처명' 형식."""
    if " - " in raw_title:
        idx = raw_title.rfind(" - ")
        return raw_title[:idx].strip(), raw_title[idx + 3:].strip()
    return raw_title.strip(), ""


def extract_source(entry, raw_title):
    src = entry.get("source", {})
    if isinstance(src, dict) and src.get("title"):
        return src["title"]
    _, fallback = extract_title_source(raw_title)
    if fallback:
        return fallback
    link = entry.get("link", "")
    for domain, name in DOMAIN_TO_SOURCE.items():
        if domain in link:
            return name
    return ""


def is_blocked(title, summary):
    text = f"{title} {summary}".lower()
    for kw in BLOCKED_KEYWORDS:
        if kw.lower() in text:
            return True
    return False


def normalize_url(url):
    return url.split("?")[0].split("#")[0].rstrip("/").lower()


def normalize_title(title):
    return re.sub(r"[\s\W_]+", "", title).lower()


def fetch_rss(query, locale, when_operator):
    url = build_rss_url(query, locale, when_operator)
    feed = feedparser.parse(url)
    return feed.entries or []


def to_article(entry):
    raw_title = entry.get("title", "")
    title, _ = extract_title_source(raw_title)
    summary = strip_html(entry.get("summary", "") or entry.get("description", ""))
    return {
        "title": title,
        "url": entry.get("link", ""),
        "source": extract_source(entry, raw_title),
        "published": parse_pubdate(entry),
        "summary": summary,
    }


def collect():
    when_op = calc_when_operator()
    cutoff = calc_cutoff_date()
    print(f"[구글 RSS] 기간 연산자: {when_op}, cutoff: {cutoff}")

    seen_urls = set()
    seen_titles = set()
    collected = []
    blocked = 0
    out_of_range = 0

    queries = [(q, KOREAN_LOCALE) for q in KOREAN_QUERIES] + \
              [(q, ENGLISH_LOCALE) for q in ENGLISH_QUERIES]

    for i, (query, locale) in enumerate(queries, 1):
        print(f"  [{i}/{len(queries)}] {query[:50]}")
        try:
            entries = fetch_rss(query, locale, when_op)
        except Exception as e:
            print(f"    [오류] {e}")
            continue

        for entry in entries:
            article = to_article(entry)
            if not article["title"] or not article["url"]:
                continue

            url_key = normalize_url(article["url"])
            title_key = normalize_title(article["title"])
            if url_key in seen_urls or title_key in seen_titles:
                continue

            if is_blocked(article["title"], article["summary"]):
                blocked += 1
                continue

            if article["published"]:
                try:
                    pub_date = datetime.strptime(article["published"][:10], "%Y-%m-%d").date()
                    if pub_date < cutoff:
                        out_of_range += 1
                        continue
                except ValueError:
                    pass

            seen_urls.add(url_key)
            seen_titles.add(title_key)
            collected.append(article)

        time.sleep(0.6)

    print(f"[구글 RSS] 수집: {len(collected)}개 (제외: {blocked}, 기간외: {out_of_range})")
    return collected


def merge_into_json(json_path, new_articles):
    today = datetime.now().date()
    cutoff = calc_cutoff_date(today)
    weekday_names = ["월", "화", "수", "목", "금", "토", "일"]
    cutoff_weekday = weekday_names[cutoff.weekday()]

    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {
            "date": today.strftime("%Y-%m-%d"),
            "time_range": f"{cutoff.month}/{cutoff.day}({cutoff_weekday}) 00:00 이후",
            "keywords": "구글 뉴스 RSS 일괄 수집",
            "articles": [],
        }

    existing_urls = {normalize_url(a.get("url", "")) for a in data.get("articles", [])}
    existing_titles = {normalize_title(a.get("title", "")) for a in data.get("articles", [])}

    appended = 0
    for article in new_articles:
        url_key = normalize_url(article["url"])
        title_key = normalize_title(article["title"])
        if url_key in existing_urls or title_key in existing_titles:
            continue
        data["articles"].append(article)
        existing_urls.add(url_key)
        existing_titles.add(title_key)
        appended += 1

    data["date"] = today.strftime("%Y-%m-%d")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[구글 RSS] {json_path}에 {appended}개 추가 (총 {len(data['articles'])}개)")


def main():
    json_path = sys.argv[1] if len(sys.argv) > 1 else "news_data.json"
    articles = collect()
    merge_into_json(json_path, articles)


if __name__ == "__main__":
    main()
