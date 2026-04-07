# MOIP 뉴스봇 개발 히스토리

## 프로젝트 개요
- **프로젝트명**: MOIP_news_bot
- **목적**: 지식재산처(MOIP) 최신 뉴스를 자동 수집하여 텔레그램 발송 + GitHub Pages 게시
- **GitHub**: https://github.com/myj0702/MOIP_news_bot
- **GitHub Pages**: https://myj0702.github.io/MOIP_news_bot/
- **작업일**: 2026-04-06

---

## 기술 스택
- Python 3.x (Anaconda 환경)
- 웹 검색: Claude Code 내장 웹 검색 활용
- 텔레그램: python-telegram-bot (requests로 Bot API 직접 호출)
- GitHub Pages: git push 자동화
- 환경변수: python-dotenv
- HTML 템플릿: jinja2

---

## 1단계: 프로젝트 구조 및 기본 설정

### 생성 파일
```
MOIP_news_bot/
├── .env.example
├── .gitignore
├── requirements.txt
├── run_news_bot.md          # claude -p용 프롬프트
├── src/
│   ├── news_collector.py    # (미사용 - A방식 채택)
│   ├── telegram_sender.py   # 텔레그램 발송
│   └── github_pages.py      # GitHub Pages 생성/push
├── docs/                    # GitHub Pages용 HTML 출력 폴더
│   └── index.html
└── news_data.json           # Claude가 생성하는 뉴스 데이터
```

### 설계 결정: A방식 채택
- **A방식**: `run_news_bot.md` 프롬프트에서 Claude가 웹 검색 → JSON 파일로 저장 → Python이 텔레그램 발송 + GitHub Pages 생성
- **B방식(미채택)**: 전부 Python으로 처리 (웹 검색은 외부 API 사용)
- A방식이 "Claude Code 내장 웹 검색 활용" 취지에 부합하여 채택

### .env 설정
```
TELEGRAM_BOT_TOKEN=8592616947:AAGVUaa6UB5yp2lf9h4GA9U0G066aiBI2aY
TELEGRAM_CHAT_ID=5373287662
NEWS_KEYWORDS=MOIP
GITHUB_REPO_PATH=./docs
GITHUB_BRANCH=main
```
- 텔레그램 봇: @MOIP_news_bot
- Chat ID는 `getUpdates` API로 조회 시도했으나 빈 결과 → 사용자가 직접 제공

---

## 2단계: Python SSL 문제 해결

### 문제
- Anaconda 환경에서 `import ssl` 시 `ImportError: DLL load failed while importing _ssl` 발생
- pip 설치, urllib HTTPS 요청 모두 불가

### 원인
- `_ssl.pyd`는 `C:\anaconda3\DLLs\`에 있음 (PATH에 포함)
- `_ssl.pyd`가 의존하는 `libssl-1_1-x64.dll`은 `C:\anaconda3\Library\bin\`에 있음 (PATH에 **미포함**)
- DLL 로드 시 libssl을 찾지 못해 실패

### 해결
- PATH에 `C:\anaconda3\Library\bin` 추가로 해결
- 임시: `export PATH="/c/anaconda3/Library/bin:$PATH"`
- 영구: 윈도우 시스템 환경변수 Path에 `C:\anaconda3\Library\bin` 추가

### 패키지 설치
```bash
export PATH="/c/anaconda3/Library/bin:$PATH" && pip install requests python-dotenv jinja2
```

---

## 3단계: 모듈 테스트

### 텔레그램 발송 테스트
1. **curl로 첫 테스트**: 영문 메시지 발송 성공 (한글 인코딩 이슈로 영문 먼저)
2. **Python telegram_sender.py 테스트**: 성공 (message_id=6)

### GitHub Pages HTML 생성 테스트
- `docs/index.html` 생성 성공
- git push는 레포 미초기화로 실패 (예상된 결과)

---

## 4단계: Git 레포 초기화 및 GitHub 연결

### 설정
```bash
git init
git remote add origin https://github.com/myj0702/MOIP_news_bot.git
git branch -M main
git config user.name "myj0702"
git config user.email "meakkang@gmail.com"
```

### 첫 push
- 원격에 이미 커밋 존재하여 `git pull origin main --rebase` 후 push 성공

---

## 5단계: claude -p 전체 플로우 테스트

### 시도 1: claude -p 비대화형 실행
```bash
claude -p "$(cat run_news_bot.md)"
```
- **실패**: WebSearch/WebFetch 도구 권한이 거부됨

### 시도 2: --allowedTools 옵션 추가
```bash
claude -p "$(cat run_news_bot.md)" --allowedTools WebSearch WebFetch Read Write Edit Bash
```
- **실패**: 5분 이상 무응답

### 시도 3: 대화형 실행
```bash
claude "$(cat run_news_bot.md)" --allowedTools WebSearch WebFetch Read Write Edit Bash
```
- **실패**: 역시 무응답

### 최종 해결: 현재 대화에서 직접 실행
- Claude가 직접 웹 검색 → JSON 저장 → Python 스크립트 실행
- 전체 플로우 성공 확인

---

## 6단계: 뉴스 선별 기준 개선

### 변경 사항
1. **저작권 관련 뉴스 제외** (저작권, 저작물, 저작자, copyright)
2. **게재 시점 기준 변경**:
   - 평일(화~금): 전날 00:00 이후
   - 주말(토~일) 또는 월요일: 직전 금요일 18:00 이후
3. **time_range에 구체적 기준일시 표기** (예: "4/3(금) 18:00 이후")

### JSON 형식 확장
```json
{
  "date": "2026-04-06",
  "time_range": "4/3(금) 18:00 이후",
  "keywords": "MOIP(지식재산처)",
  "articles": [
    {
      "title": "기사 제목",
      "url": "https://...",
      "source": "출처 언론사명",
      "published": "2026-04-06",
      "summary": "3~5줄 요약"
    }
  ]
}
```

### 모듈 업데이트
- `telegram_sender.py`: 시간 범위, 출처, 게재시점 표시 추가
- `github_pages.py`: 상단에 시간 범위 배지, 각 기사에 출처/게재시점 표시, 인코딩 오류 수정
- `run_news_bot.md`: 검색 기준 상세화

### 테스트 결과 (최종)
| 항목 | 결과 |
|------|------|
| 기준 | 일요일 → 직전 금요일(4/3) 18:00 이후 |
| 수집 기사 | 4/6 게재 3건 |
| 텔레그램 | 발송 성공 (message_id=9) |
| GitHub Pages | push 완료 |

---

## 미완료 작업
- [ ] `claude -p` 비대화형 자동 실행 문제 해결
- [ ] 윈도우 작업 스케줄러 등록 (run_bot.bat + 스케줄러 설정)
- [ ] 시스템 환경변수 PATH에 `C:\anaconda3\Library\bin` 영구 추가

---

## GitHub Pages 참고
- 무료 계정에서는 **Public 레포**에서만 GitHub Pages 사용 가능
- Settings → Pages → Source: Deploy from branch, Branch: main, Folder: /docs
