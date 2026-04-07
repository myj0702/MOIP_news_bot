# MOIP 뉴스봇 실행 프롬프트

아래 작업을 순서대로 수행하세요.

## 1단계: 뉴스 검색

아래 검색 쿼리들을 **모두** 웹 검색하여 최신 뉴스를 폭넓게 수집하세요.

### 검색 키워드 확장 규칙

각 키워드를 검색할 때 **파생어, 합성어, 전방/후방 절단어**를 모두 포함하여 검색하세요.

예시:
- "특허" → 특허권, 특허청, 특허출원, 특허등록, 특허소송, 특허침해, 특허분쟁, 특허무효, 특허심판, 특허기술 등
- "상표" → 상표권, 상표등록, 상표분쟁, 상표침해, 상표출원, 상표심판, 등록상표 등
- "디자인" → 디자인권, 디자인등록, 디자인출원, 디자인보호, 디자인심사, 디자인침해 등
- "발명" → 발명특허, 발명가, 발명대회, 직무발명, 발명진흥, 발명교육, 발명왕 등
- "patent" → patented, patentable, patentability, patent-pending, patent holder, patentee 등
- "trademark" → trademarked, trademark registration, trademark infringement, trademark dispute 등

즉, 검색 결과에서 키워드의 **어근이 포함된 모든 기사**를 수집 대상으로 판단하세요.

### 검색 쿼리 목록 (모두 실행)

#### 한국어 쿼리
1. "지식재산처" (보도자료, 정책 동향)
2. "특허 뉴스" (특허권, 특허출원, 특허등록, 특허분쟁, 특허판결, 특허심판)
3. "실용신안" (실용신안 출원, 등록, 분쟁)
4. "상표 분쟁" (상표권, 상표등록, 상표침해, 브랜드 보호)
5. "디자인권 OR 디자인보호 OR 디자인등록" (디자인 분쟁 포함)
6. "PCT 국제출원"
7. "특허침해 OR 특허 침해 소송 OR 특허소송"
8. "발명 뉴스" (발명특허, 직무발명, 발명대회, 발명진흥)
9. "지식재산 정책" (IP 정책, 법률 개정, 지재권)
10. "영업비밀 침해 OR 영업비밀 유출 OR 기술유출"
11. "특허청 OR 지식재산처" (해외 각국 특허청 동향)
12. "반도체 특허 OR 반도체 지식재산"
13. "AI 특허 OR 인공지능 특허 OR AI 지식재산"
14. "바이오 특허 OR 제약 특허 OR 의약품 특허"
15. "표준특허 OR SEP OR FRAND"

#### 영어 쿼리
16. "patent news Korea"
17. "IP lawsuit Korea"
18. "Korea intellectual property"
19. "patent infringement Korea"
20. "trademark dispute Korea"
21. "trade secret Korea"
22. "WIPO PCT international patent"
23. "EPO patent application Korea"
24. "USPTO patent Korea"
25. "patent litigation Samsung LG SK Hyundai"
26. "standard essential patent SEP FRAND"
27. "pharmaceutical patent drug patent"
28. "semiconductor patent chip IP"
29. "AI patent artificial intelligence IP"
30. "IP policy regulation 2026"

### 검색 시 참고할 주요 언론사
- **국내 일간지**: 조선일보, 중앙일보, 동아일보, 한국경제, 매일경제, 서울경제, 한겨레, 경향신문, 전자신문, 디지털타임스
- **국내 방송사**: KBS, MBC, SBS, YTN, 연합뉴스
- **국내 전문지**: 특허뉴스, 법률신문, 더벨, IT조선
- **해외 주요 외신**: Reuters, Bloomberg, AP, Financial Times, Wall Street Journal, Nikkei Asia, The Guardian
- **해외 IP 전문 매체**: IAM Media, Managing IP, WIPR, Patent Docs, IPWatchdog, Lexology, JUVE Patent

### 게재 시점 기준
- **월요일**: 직전 금요일 00:00 이후 게재된 뉴스
- **화~금**: 전날 00:00 이후 게재된 뉴스
- **주말(토~일)**: 실행하지 않음 (만약 실행할 경우 직전 금요일 00:00 이후 기준)

### 검색 규칙
- 위 쿼리들을 모두 검색한 뒤, 게재 시점 기준에 해당하는 뉴스를 **최대 20개**까지 선별하세요
- **저작권 관련 뉴스는 제외**하세요 (저작권, 저작물, 저작자, copyright 등)
- 중복 기사는 제거하세요 (같은 사안의 기사가 여러 언론사에 있으면 가장 상세한 것 1개만)
- 각 뉴스의 제목, URL, 출처(언론사명), 게재 시점(날짜+시간), 요약(3~5줄)을 정리하세요
- 지식재산처 보도자료뿐 아니라 **국내외 주요 언론사**(연합뉴스, 한경, 매일경제, 전자신문, Reuters, Bloomberg 등) 기사를 적극 포함하세요

## 2단계: JSON 저장

검색 결과를 아래 형식으로 `news_data.json` 파일에 저장하세요:

```json
{
  "date": "YYYY-MM-DD",
  "time_range": "24시간 이내",
  "keywords": "검색 키워드",
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

- `time_range`은 실제 검색 범위를 기재 (예: "4/5(토) 00:00 이후" 또는 "4/4(금) 18:00 이후")

## 3단계: 텔레그램 발송

다음 명령어를 실행하세요:

```bash
export PATH="/c/anaconda3/Library/bin:$PATH" && python src/telegram_sender.py news_data.json
```

## 4단계: GitHub Pages 업데이트

다음 명령어를 실행하세요:

```bash
export PATH="/c/anaconda3/Library/bin:$PATH" && python src/github_pages.py news_data.json
```

## 주의사항
- .env 파일이 존재하고 필수 값이 설정되어 있어야 합니다
- 뉴스 검색 시 신뢰할 수 있는 출처를 우선하세요
- 에러 발생 시 에러 내용을 출력하고 다음 단계로 넘어가세요
