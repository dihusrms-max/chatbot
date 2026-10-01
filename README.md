# 챗봇isgoot

Streamlit과 LangChain으로 만든 OpenAI 챗봇입니다. `app.py`가 실행 파일이며, 모델은 `gpt-6-luna`를 사용합니다.

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

로컬에서는 `.env` 파일 또는 환경 변수에 `OPENAI_API_KEY`를 설정할 수 있습니다. 배포에서는 Streamlit 앱의 Secrets에 키를 설정하세요. API 키는 GitHub에 올리지 마세요.

## Streamlit Community Cloud 배포

GitHub 저장소의 `main` 브랜치와 루트의 `app.py`를 선택해 배포하고, 앱 설정의 Secrets에 `OPENAI_API_KEY`를 입력하세요. `.venv` 폴더는 로컬 가상환경이라 Git에서 제외됩니다.
