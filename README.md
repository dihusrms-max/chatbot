# 샤이니 챗봇

Streamlit으로 만든 간단한 AI 챗봇입니다.

## 로컬에서 실행

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

AI 답변을 사용하려면 `OPENAI_API_KEY` 환경 변수를 설정하거나 `.streamlit/secrets.toml`에 아래 내용을 넣으세요.

```toml
OPENAI_API_KEY = "발급받은_API_키"
```

API 키가 없어도 페이지를 열 수 있습니다. 키는 GitHub에 올리지 마세요.

## Streamlit Community Cloud 배포

GitHub 저장소의 `main` 브랜치와 `app.py`를 선택해 배포하고, 앱 설정의 Secrets에 `OPENAI_API_KEY`를 입력하세요.
