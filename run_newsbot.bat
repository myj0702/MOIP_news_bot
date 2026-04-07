@echo off
chcp 65001 >nul
setlocal

:: 프로젝트 경로
set PROJECT_DIR=C:\claudeCode\Moip_news_bot

:: Anaconda PATH 설정
set PATH=C:\anaconda3\Library\bin;%PATH%

:: 로그 파일 (날짜별)
for /f "tokens=1-3 delims=-" %%a in ('powershell -command "Get-Date -Format yyyy-MM-dd"') do set TODAY=%%a-%%b-%%c
set LOG_FILE=%PROJECT_DIR%\logs\%TODAY%.log

:: 로그 폴더 생성
if not exist "%PROJECT_DIR%\logs" mkdir "%PROJECT_DIR%\logs"

:: Claude Code CLI 실행
cd /d %PROJECT_DIR%
echo [%date% %time%] 뉴스봇 실행 시작 >> "%LOG_FILE%"
claude -p "run_news_bot.md 파일의 지시에 따라 1단계부터 4단계까지 순서대로 실행해줘." --allowedTools "Bash,Read,Write,Edit,WebSearch,WebFetch,Glob,Grep" >> "%LOG_FILE%" 2>&1
echo [%date% %time%] 뉴스봇 실행 완료 >> "%LOG_FILE%"

endlocal
