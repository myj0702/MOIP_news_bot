# MOIP 뉴스봇 실행 프롬프트

아래 작업을 순서대로 수행하세요.

## 1단계: 구글 뉴스 RSS 선수집

먼저 구글 뉴스 RSS로 한국어/영어 IP 관련 기사를 일괄 수집합니다. 다음 명령어를 실행하세요:

```bash
export PATH="/c/anaconda3/Library/bin:$PATH" && python src/google_news.py news_data.json
```

이 단계의 결과:
- `news_data.json`이 생성되며 보통 100~250개의 기사가 저장됩니다
- 기간 필터(when:Nd)와 중복 제거, 저작권/면세점 제외가 자동 적용됩니다
- 출처는 한국 주요 일간지, 통신사, IP 전문지(전자신문, IP데일리, 특허뉴스 등) 및 영문 매체를 포괄합니다

## 2단계: WebSearch로 보강 수집

구글 RSS가 잘 잡지 못하는 영역만 집중적으로 보강하세요. 다음 영역에 한정하여 검색합니다:

### 보강 검색 쿼리 (필요 시 실행)

#### 영어 IP 전문 매체 / 해외 외신
1. `site:iam-media.com Korea patent`
2. `site:managingip.com Korea`
3. `site:ipwatchdog.com Korea`
4. `site:lexology.com Korea intellectual property`
5. `Reuters patent Korea Samsung LG SK Hynix`
6. `Bloomberg Korea intellectual property lawsuit`
7. `ITC section 337 Korea investigation 2026`

#### 국내 전문지 보강 (구글 RSS 누락 시)
8. `site:ipdaily.co.kr 특허`
9. `site:특허뉴스 OR site:patentnews.co.kr`

### 보강 규칙
- **각 검색 전에 `news_data.json`의 기존 `articles[].url` 목록을 확인**하여 중복 검색을 피하세요
- 새로 찾은 기사만 `articles` 배열에 append하세요
- **핵심 기사(주요 정책 발표, 대형 판결, M&A 등)는 WebFetch로 본문을 가져와 `summary`를 3~5줄로 보강**하세요 (구글 RSS의 description은 짧음)
- 검색 키워드 확장 규칙: 파생어, 유사어, 동의어 모두 포함
- 게재 시점은 아래 "기준 시점" 표를 따르세요

### 게재 시점 기준

오늘의 요일을 먼저 확인한 뒤, 아래 규칙에 따라 기준 시점을 결정하세요:

| 오늘 요일 | 기준 시점 |
|-----------|-----------|
| 월요일 | 직전 금요일 00:00 이후 |
| 화~금 | 전날 00:00 이후 |
| 토~일 | 실행하지 않음 (실행 시 직전 금요일 00:00 이후) |

## 3단계: 최종 기사 선별 (최대 20개)

`news_data.json`의 모든 기사를 검토하여 최대 20개로 추리세요. 선별 기준:

1. **중요도** — 정책 발표, 대법원/특허법원 판결, 표준특허 분쟁, 대기업 IP 소송, 주요 기술이전 등 우선
2. **출처 다양성** — 같은 사안의 기사가 여러 언론사에 있으면 가장 상세한 1개만
3. **카테고리 다양성** — 특허/상표/디자인/영업비밀/정책/해외 외신 등 균형 있게
4. **저작권 관련 뉴스 제외** (저작권, 저작물, 저작자, copyright)
5. **면세점 특허 관련 뉴스 제외** (면세점, 면세 특허, duty-free)

선별된 기사만 `news_data.json`의 `articles` 배열에 남기고 나머지는 제거하세요. JSON 포맷:

```json
{
  "date": "YYYY-MM-DD",
  "time_range": "M/D(요일) 00:00 이후",
  "keywords": "검색 키워드 요약",
  "articles": [
    {
      "title": "기사 제목",
      "url": "https://기사URL",
      "source": "출처 언론사명",
      "published": "YYYY-MM-DD HH:MM",
      "summary": "기사 요약 3~5줄"
    }
  ]
}
```

## 4단계: 날짜 검증

다음 명령어를 실행하여 기준일 이전 기사를 자동 제거하세요:

```bash
export PATH="/c/anaconda3/Library/bin:$PATH" && python src/date_filter.py news_data.json
```

## 5단계: 텔레그램 발송

```bash
export PATH="/c/anaconda3/Library/bin:$PATH" && python src/telegram_sender.py news_data.json
```

## 6단계: GitHub Pages 업데이트

```bash
export PATH="/c/anaconda3/Library/bin:$PATH" && python src/github_pages.py news_data.json
```

## 주의사항
- `.env` 파일이 존재하고 필수 값이 설정되어 있어야 합니다 (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` 등)
- 구글 뉴스 RSS는 별도 키가 필요 없습니다
- 에러 발생 시 에러 내용을 출력하고 다음 단계로 넘어가세요
