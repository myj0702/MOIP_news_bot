"""
날짜 검증 필터: news_data.json에서 기준일 이전 기사를 자동 제거한다.

기준일 규칙:
  - 월요일: 직전 금요일 00:00 이후
  - 화~금: 전날 00:00 이후
  - 토~일: 직전 금요일 00:00 이후
"""

import json
import sys
from datetime import datetime, timedelta


def calc_cutoff_date(today=None):
    """오늘 요일에 따라 기준 날짜(cutoff)를 계산한다."""
    if today is None:
        today = datetime.now().date()

    weekday = today.weekday()  # 0=월, 1=화, ..., 6=일

    if weekday == 0:  # 월요일 → 직전 금요일
        cutoff = today - timedelta(days=3)
    elif weekday in (5, 6):  # 토/일 → 직전 금요일
        days_since_friday = weekday - 4
        cutoff = today - timedelta(days=days_since_friday)
    else:  # 화~금 → 전날
        cutoff = today - timedelta(days=1)

    return cutoff


def filter_articles(json_path):
    """news_data.json을 읽어 기준일 이전 기사를 제거하고 다시 저장한다."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cutoff = calc_cutoff_date()
    cutoff_str = cutoff.strftime("%Y-%m-%d")
    weekday_names = ["월", "화", "수", "목", "금", "토", "일"]
    cutoff_weekday = weekday_names[cutoff.weekday()]

    print(f"[날짜 필터] 기준일: {cutoff_str}({cutoff_weekday}) 00:00 이후")

    articles = data.get("articles", [])
    original_count = len(articles)

    filtered = []
    removed = []
    for article in articles:
        published = article.get("published", "")
        try:
            pub_date = datetime.strptime(published[:10], "%Y-%m-%d").date()
            if pub_date >= cutoff:
                filtered.append(article)
            else:
                removed.append(article)
        except (ValueError, IndexError):
            # 날짜 파싱 실패 시 포함 (수동 확인 필요)
            filtered.append(article)
            print(f"  [경고] 날짜 파싱 실패, 포함 유지: {article.get('title', '?')}")

    for article in removed:
        print(f"  [제거] {article.get('published', '?')} - {article.get('title', '?')}")

    data["articles"] = filtered
    data["time_range"] = f"{cutoff.month}/{cutoff.day}({cutoff_weekday}) 00:00 이후"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[날짜 필터] 완료: {original_count}개 → {len(filtered)}개 (제거: {len(removed)}개)")


if __name__ == "__main__":
    json_path = sys.argv[1] if len(sys.argv) > 1 else "news_data.json"
    filter_articles(json_path)
