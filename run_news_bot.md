# MOIP 뉴스봇 실행 프롬프트

아래 작업을 순서대로 수행하세요.

## 1단계: 뉴스 검색

.env 파일에서 NEWS_KEYWORDS 값을 읽고, 해당 키워드로 최신 뉴스를 웹 검색하세요.

- 오늘 날짜 기준 최신 뉴스 5~10개를 찾으세요
- 각 뉴스의 제목, URL, 요약(1~2문장)을 정리하세요

## 2단계: JSON 저장

검색 결과를 아래 형식으로 `news_data.json` 파일에 저장하세요:

```json
{
  "date": "YYYY-MM-DD",
  "keywords": "검색 키워드",
  "articles": [
    {
      "title": "기사 제목",
      "url": "https://기사URL",
      "summary": "기사 요약 1~2문장"
    }
  ]
}
```

## 3단계: 텔레그램 발송

다음 명령어를 실행하세요:

```bash
python src/telegram_sender.py news_data.json
```

## 4단계: GitHub Pages 업데이트

다음 명령어를 실행하세요:

```bash
python src/github_pages.py news_data.json
```

## 주의사항
- .env 파일이 존재하고 필수 값이 설정되어 있어야 합니다
- 뉴스 검색 시 신뢰할 수 있는 출처를 우선하세요
- 에러 발생 시 에러 내용을 출력하고 다음 단계로 넘어가세요
