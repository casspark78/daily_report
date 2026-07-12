# Daily Report

출근 전 20분 안에 훑어볼 수 있는 개인 맞춤 데일리 뉴스 리포트를 매일 아침 자동으로 생성합니다.

- 📱 디스플레이·반도체
- 💻 IT·개발·스타트업
- 🤖 AI·머신러닝
- 💰 경제·금융·증시
- 🌍 국내외 시사

각 토픽별 RSS 피드에서 최신 기사를 모아 OpenAI API로 한국어 2문장 요약을 만들고,
정적 HTML 리포트(`docs/index.html`)로 생성해 GitHub Pages로 배포합니다.

## 동작 방식

1. `.github/workflows/daily-report.yml`이 평일 06:30(KST)에 자동 실행됩니다.
2. `src/fetch.py`가 토픽별 RSS 피드를 수집하고 키워드로 걸러냅니다.
3. `src/summarize.py`가 OpenAI API로 각 기사를 한국어로 요약합니다 (API 키가 없으면 원문 앞부분으로 대체).
4. `src/render.py` + `templates/report.html.j2`가 `docs/index.html`을 생성하고,
   `docs/archive/YYYY-MM-DD.html`에 보관본을 남깁니다.
5. 워크플로가 결과를 커밋·푸시하면 GitHub Pages가 자동 반영합니다.

## 초기 설정 (최초 1회)

1. **OpenAI API 키 등록**
   - 저장소 Settings → Secrets and variables → Actions → New repository secret
   - Name: `OPENAI_API_KEY`, Value: 발급받은 키
2. **GitHub Pages 활성화**
   - 저장소 Settings → Pages → Source: `Deploy from a branch`
   - Branch: `main`, Folder: `/docs` 선택 후 저장
   - 몇 분 후 `https://<username>.github.io/<repo>/` 에서 리포트 확인 가능
3. 필요하면 Actions 탭에서 `Daily Report` 워크플로를 `Run workflow`로 즉시 실행해볼 수 있습니다.

## 로컬 실행

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...   # 선택사항. 없으면 원문 기반 요약으로 대체됨
cd src && python main.py
```

생성된 `docs/index.html`을 브라우저로 열어 확인하세요.

## 토픽/소스 수정

`src/sources.py`에서 토픽별 RSS 피드 목록, 키워드 필터, 토픽당 최대 기사 수를 조정할 수 있습니다.
관심사가 바뀌면 이 파일만 수정하면 됩니다.

## 실행 주기 변경

`.github/workflows/daily-report.yml`의 `cron` 값을 수정하세요. 기본값은 평일 06:30 KST입니다
(cron은 UTC 기준이라 KST와 9시간 차이가 있습니다).
