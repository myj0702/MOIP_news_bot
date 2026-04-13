# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 커뮤니케이션 스타일
- 한국어로 답변
- 코딩 전 반드시 계획 먼저 제시
- 사용자 확인 전까지 파일 수정 금지
- 스킬 생성시 스킬 이름과 트리거 확인

## 프로젝트 개요

MOIP_news_bot은 지식재산(IP) 관련 뉴스를 자동 수집하여 Telegram과 GitHub Pages로 배포하는 봇이다.

**A-Method 아키텍처:** Claude Code의 웹검색으로 뉴스 수집 → JSON 저장 → Python으로 Telegram 발송 및 GitHub Pages 배포

## 실행 워크플로우

`run_news_bot.md`에 정의된 4단계 순서:
1. Claude 웹검색 (한국어 16개 + 영어 14개 쿼리, 최대 20개 기사)
2. `news_data.json` 저장
3. `python src/telegram_sender.py news_data.json` — Telegram 발송
4. `python src/github_pages.py news_data.json` — GitHub Pages HTML 생성 및 git push

## 명령어

```bash
# 의존성 설치 (Anaconda 환경 필수)
export PATH="/c/anaconda3/Library/bin:$PATH" && pip install -r requirements.txt

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

- **`src/telegram_sender.py`** — JSON → Telegram 마크다운 포맷 변환 및 API 발송. 4000자 초과 시 메시지 분할 발송
- **`src/github_pages.py`** — JSON → Jinja2 HTML 렌더링 → `docs/index.html` 저장 → git commit & push
- **`run_news_bot.md`** — Claude Code 실행 프롬프트. 검색 키워드, 날짜 필터링 규칙, 저작권 기사 제외 규칙 포함
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
