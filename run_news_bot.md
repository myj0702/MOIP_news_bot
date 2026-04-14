# MOIP 뉴스봇 실행 프롬프트

아래 작업을 순서대로 수행하세요.

## 1단계: 뉴스 검색

아래 검색 쿼리들을 **모두** 웹 검색하여 최신 뉴스를 폭넓게 수집하세요.

### 검색 키워드 확장 규칙

각 키워드를 검색할 때 **파생어, 합성어, 전방/후방 절단어, 유사 의미어(동의어·관련어)**를 모두 포함하여 검색하세요.

예시:
- "특허" → 특허권, 특허청, 특허출원, 특허등록, 특허소송, 특허침해, 특허분쟁, 특허무효, 특허심판, 특허기술, 특허 라이선스, 특허 실시권, 특허 포트폴리오 등
- "상표" → 상표권, 상표등록, 상표분쟁, 상표침해, 상표출원, 상표심판, 등록상표, 서비스표, 브랜드 분쟁, 상호 분쟁 등
- "디자인" → 디자인권, 디자인등록, 디자인출원, 디자인보호, 디자인심사, 디자인침해, 의장권 등
- "발명" → 발명특허, 발명가, 발명대회, 직무발명, 발명진흥, 발명교육, 발명왕, 선사용권 등
- "지식재산" → 지재권, 지적재산권, 산업재산권, IP, 무형자산, 기술자산 등
- "침해·분쟁" → 권리침해, 특허침해, 상표침해, 디자인침해, 영업비밀 침해, 기술 탈취, 기술 유출, IP 분쟁, 지재권 분쟁, 특허 무효심판, 권리범위확인심판, 정정심판, 거절결정불복심판 등
- "소송·판결" → 특허소송, 침해소송, 침해금지, 손해배상, 가처분, 법원 판결, 대법원 판결, 특허법원, ITC 조사, 337조 등
- "라이선스·이전" → 기술이전, 기술실시, 실시권, 전용실시권, 통상실시권, 크로스라이선스, 로열티, 기술료 등
- "patent" → patented, patentable, patentability, patent-pending, patent holder, patentee, patent troll, NPE, PAE 등
- "trademark" → trademarked, trademark registration, trademark infringement, trademark dispute, brand protection 등
- "IP" → intellectual property, IP rights, IP litigation, IP licensing, IP portfolio, IP valuation 등

즉, 검색 결과에서 키워드의 **어근이 포함된 모든 기사** 및 **유사 의미를 가진 기사**를 수집 대상으로 판단하세요.

### 검색 쿼리 목록 (모두 실행)

#### 한국어 쿼리
1. "지식재산처" (보도자료, 정책 동향)
2. "특허 뉴스" (특허권, 특허출원, 특허등록, 특허분쟁, 특허판결, 특허심판)
3. "실용신안" (실용신안 출원, 등록, 분쟁)
4. "상표 분쟁 OR 상표침해 OR 브랜드 분쟁 OR 서비스표"
5. "디자인권 OR 디자인보호 OR 디자인등록 OR 디자인침해"
6. "PCT 국제출원 OR 국제특허출원"
7. "특허침해 OR 특허소송 OR 침해금지 OR 손해배상 특허"
8. "발명 뉴스" (발명특허, 직무발명, 발명대회, 발명진흥, 선사용권)
9. "지식재산 정책 OR 지재권 정책 OR 산업재산권 정책" (IP 정책, 법률 개정)
10. "영업비밀 침해 OR 영업비밀 유출 OR 기술유출 OR 기술 탈취"
11. "특허청 OR 지식재산처" (해외 각국 특허청 동향)
12. "반도체 특허 OR 반도체 지식재산"
13. "AI 특허 OR 인공지능 특허 OR AI 지식재산"
14. "바이오 특허 OR 제약 특허 OR 의약품 특허"
15. "표준특허 OR SEP OR FRAND"
16. "특허 무효심판 OR 권리범위확인 OR 정정심판 OR 특허심판원"
17. "특허 라이선스 OR 기술이전 OR 실시권 OR 로열티 OR 기술료"
18. "특허 트롤 OR NPE OR PAE OR 비실시 특허"
19. "지재권 분쟁 OR IP 분쟁 OR 특허법원 OR 대법원 특허"
20. "부정경쟁행위 OR 부정경쟁방지법 OR 트레이드 드레스"

#### 영어 쿼리
21. "patent news Korea"
22. "IP lawsuit Korea"
23. "Korea intellectual property"
24. "patent infringement Korea"
25. "trademark dispute Korea"
26. "trade secret Korea"
27. "WIPO PCT international patent"
28. "EPO patent application Korea"
29. "USPTO patent Korea"
30. "patent litigation Samsung LG SK Hyundai"
31. "standard essential patent SEP FRAND"
32. "pharmaceutical patent drug patent"
33. "semiconductor patent chip IP"
34. "AI patent artificial intelligence IP"
35. "IP policy regulation 2026"
36. "patent troll NPE PAE Korea"
37. "IP licensing royalty technology transfer Korea"
38. "ITC section 337 investigation Korea"

### 검색 시 참고할 주요 언론사
- **국내 일간지**: 조선일보, 중앙일보, 동아일보, 한국경제, 매일경제, 서울경제, 한겨레, 경향신문, 전자신문, 디지털타임스, 파이낸셜뉴스, 헤럴드경제, 아시아경제, 대한경제, 세계일보, 이투데이, 이데일리, 한국일보, 브릿지경제, 내일신문, 머니투데이, PAX경제, 쿠키뉴스
- **국내 통신사**: 연합뉴스, 뉴시스, 뉴스1
- **국내 방송사**: KBS, MBC, SBS, SBS Biz, YTN, TJB, 채널A, 노컷뉴스
- **국내 전문지**: 특허뉴스, IP데일리, 법률신문, 더벨, IT조선
- **해외 주요 외신**: Reuters, Bloomberg, AP, Financial Times, Wall Street Journal, Nikkei Asia, The Guardian, BBC, CNN, The New York Times, The Washington Post, The Economist, CNBC, Forbes, The Japan Times
- **해외 IP 전문 매체**: IAM Media, Managing IP, WIPR, Patent Docs, IPWatchdog, Lexology, JUVE Patent

### 게재 시점 기준

**중요: 아래 기준을 반드시 정확히 따르세요. "오늘"은 이 프롬프트가 실행되는 당일을 의미합니다.**

오늘의 요일을 먼저 확인한 뒤, 아래 규칙에 따라 기준 시점을 결정하세요:

| 오늘 요일 | 기준 시점 | 예시 (오늘이 4/7 화요일인 경우) |
|-----------|-----------|-------------------------------|
| 월요일 | 직전 금요일 00:00 이후 | 오늘이 4/6(월) → 4/3(금) 00:00 이후 |
| 화요일 | 전날(월요일) 00:00 이후 | 오늘이 4/7(화) → 4/6(월) 00:00 이후 |
| 수요일 | 전날(화요일) 00:00 이후 | 오늘이 4/8(수) → 4/7(화) 00:00 이후 |
| 목요일 | 전날(수요일) 00:00 이후 | 오늘이 4/9(목) → 4/8(수) 00:00 이후 |
| 금요일 | 전날(목요일) 00:00 이후 | 오늘이 4/10(금) → 4/9(목) 00:00 이후 |
| 토~일 | 실행하지 않음 (실행 시 직전 금요일 00:00 이후) |

### 검색 규칙
- 위 쿼리들을 모두 검색한 뒤, 게재 시점 기준에 해당하는 뉴스를 **최대 20개**까지 선별하세요
- **저작권 관련 뉴스는 제외**하세요 (저작권, 저작물, 저작자, copyright 등)
- **면세점 특허 관련 뉴스는 제외**하세요 (면세점, 면세 특허, duty-free, duty free 등)
- 중복 기사는 제거하세요 (같은 사안의 기사가 여러 언론사에 있으면 가장 상세한 것 1개만)
- 각 뉴스의 제목, URL, 출처(언론사명), 게재 시점(날짜+시간), 요약(3~5줄)을 정리하세요
- 지식재산처 보도자료뿐 아니라 **국내외 주요 언론사**(연합뉴스, 뉴시스, 한경, 매일경제, 전자신문, 헤럴드경제, 파이낸셜뉴스, Reuters, Bloomberg, AP 등) 기사를 적극 포함하세요

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

## 3단계: 날짜 검증

다음 명령어를 실행하여 기준일 이전 기사를 자동 제거하세요:

```bash
export PATH="/c/anaconda3/Library/bin:$PATH" && python src/date_filter.py news_data.json
```

## 4단계: 텔레그램 발송

다음 명령어를 실행하세요:

```bash
export PATH="/c/anaconda3/Library/bin:$PATH" && python src/telegram_sender.py news_data.json
```

## 5단계: GitHub Pages 업데이트

다음 명령어를 실행하세요:

```bash
export PATH="/c/anaconda3/Library/bin:$PATH" && python src/github_pages.py news_data.json
```

## 주의사항
- .env 파일이 존재하고 필수 값이 설정되어 있어야 합니다
- 뉴스 검색 시 신뢰할 수 있는 출처를 우선하세요
- 에러 발생 시 에러 내용을 출력하고 다음 단계로 넘어가세요
