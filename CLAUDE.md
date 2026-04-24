# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 커뮤니케이션 스타일
- 한국어로 답변
- 코딩 전 반드시 계획 먼저 제시
- 사용자 확인 전까지 파일 수정 금지
- 스킬 생성시 스킬 이름과 트리거 확인

## 프로젝트 개요

MOIP_news_bot은 지식재산(IP) 관련 뉴스를 자동 수집하여 Telegram과 GitHub Pages로 배포하는 봇이다.

**아키텍처:** 구글 뉴스 RSS 1차 대량 수집 → Claude WebSearch로 보강 → JSON 정리 → Python으로 Telegram 발송 및 GitHub Pages 배포

## 실행 워크플로우

`run_news_bot.md`에 정의된 6단계 순서:
1. `python src/google_news.py news_data.json` — 구글 뉴스 RSS 일괄 수집 (한국어 16 + 영어 10 쿼리, 보통 100~250개 후보)
2. Claude WebSearch로 영문 IP 전문 매체·해외 외신·국내 전문지 보강
3. 최종 20개 선별 (중요도/출처 다양성 기준)
4. `python src/date_filter.py news_data.json` — 날짜 검증
5. `python src/telegram_sender.py news_data.json` — Telegram 발송
6. `python src/github_pages.py news_data.json` — GitHub Pages HTML 생성 및 git push

## 명령어

```bash
# 의존성 설치 (Anaconda 환경 필수)
export PATH="/c/anaconda3/Library/bin:$PATH" && pip install -r requirements.txt

# 구글 뉴스 RSS 수집
export PATH="/c/anaconda3/Library/bin:$PATH" && python src/google_news.py news_data.json

# 날짜 검증
export PATH="/c/anaconda3/Library/bin:$PATH" && python src/date_filter.py news_data.json

# Telegram 발송
export PATH="/c/anaconda3/Library/bin:$PATH" && python src/telegram_sender.py news_data.json

# GitHub Pages 배포
export PATH="/c/anaconda3/Library/bin:$PATH" && python src/github_pages.py news_data.json

# 배치 자동 실행 (Windows)
run_newsbot.bat

# Claude CLI 비대화형 실행
claude -p "$(cat run_news_bot.md)" --allowedTools "Bash,Read,Write,Edit,WebSearch,WebFetch,Glob,Grep"
```

## 핵심 아키텍처

- **`src/google_news.py`** — 구글 뉴스 RSS 호출 → 표준 JSON 변환·병합. `feedparser` 사용, 키 불필요. `date_filter.calc_cutoff_date()` 재사용
- **`src/date_filter.py`** — `news_data.json`에서 기준일 이전 기사 제거. 평일/주말 룰 정의
- **`src/telegram_sender.py`** — JSON → Telegram 마크다운 포맷 변환 및 API 발송. 4000자 초과 시 메시지 분할 발송
- **`src/github_pages.py`** — JSON → Jinja2 HTML 렌더링 → `docs/index.html` 저장 → git commit & push
- **`run_news_bot.md`** — Claude Code 실행 프롬프트. 6단계 워크플로우, 보강 검색 쿼리, 선별 기준, 저작권/면세점 제외 규칙 포함
- **`news_data.json`** — 수집된 뉴스 데이터 (중간 산출물)
- **`docs/index.html`** — GitHub Pages 배포용 HTML (자동 생성)

## 환경 설정

- **Python 실행 시 반드시** `export PATH="/c/anaconda3/Library/bin:$PATH"` 선행 (Anaconda SSL DLL 의존성)
- `.env` 필수 변수: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `GITHUB_REPO_PATH`, `GITHUB_BRANCH`

## 뉴스 수집 규칙

- 평일(화~금): 전일 00:00 이후 기사
- 월요일: 전주 금요일 00:00 이후 기사
- 주말: 건너뜀
- 저작권 관련 기사(저작권, 저작물, 저작자, copyright) 제외
- 면세점 특허 관련 기사(면세점, 면세 특허, duty-free) 제외
