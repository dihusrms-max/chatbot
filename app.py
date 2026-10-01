import os

import streamlit as st
from openai import OpenAI
from streamlit.errors import StreamlitSecretNotFoundError


st.set_page_config(
    page_title="샤이니 AI | 대화 공간",
    page_icon="🤖",
    layout="centered",
)

st.markdown(
    """
    <style>
      .stApp {
        background:
          radial-gradient(ellipse at 12% 4%, rgba(183, 160, 255, .18), transparent 38%),
          radial-gradient(ellipse at 92% 18%, rgba(255, 197, 143, .16), transparent 34%),
          #fbfaff;
      }
      [data-testid="stMainBlockContainer"] { max-width: 850px; padding-top: 2.6rem; }
      [data-testid="stSidebar"] { background: #f3f0fb; }
      .brand-mark {
        display: inline-block; padding: .38rem .8rem; border-radius: 999px;
        background: #eee8ff; color: #6244a5; font-size: .8rem;
        font-weight: 700; letter-spacing: .08em;
      }
      .hero-title { margin: .8rem 0 .25rem; color: #211a35; font-size: 2.55rem; font-weight: 750; }
      .hero-copy { margin: 0 0 1.4rem; color: #6b6578; font-size: 1.05rem; }
      .welcome-card {
        margin: 1.5rem 0 1rem; padding: 1.2rem 1.35rem;
        border: 1px solid #e8e1f4; border-radius: 18px;
        background: rgba(255,255,255,.82); color: #494257;
      }
      [data-testid="stChatMessage"] {
        border: 1px solid rgba(226, 220, 238, .85);
        border-radius: 18px; padding: .85rem 1rem; background: rgba(255,255,255,.8);
      }
      [data-testid="stChatInput"] { border-color: #d9cdef; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="brand-mark">SHINY AI · 대화 도우미</div>'
    '<h1 class="hero-title">궁금한 걸 편하게 물어보세요</h1>'
    '<p class="hero-copy">아이디어를 정리하고, 새로운 내용을 배우고, 필요한 답을 찾아드려요.</p>',
    unsafe_allow_html=True,
)


def get_api_key() -> str | None:
    if key := os.getenv("OPENAI_API_KEY"):
        return key
    try:
        return st.secrets["OPENAI_API_KEY"]
    except (KeyError, StreamlitSecretNotFoundError):
        return None


if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("🤖 샤이니 AI")
    st.caption("편하게 질문하고 생각을 나눠 보세요.")
    st.divider()
    if st.button("대화 지우기"):
        st.session_state.messages = []
        st.rerun()
    st.caption("새로 시작하면 현재 대화가 화면에서 지워집니다.")

if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome-card">
          <strong>이렇게 시작해 보세요</strong><br>
          관심 있는 주제를 설명해 달라고 하거나, 복잡한 내용을 쉽게 풀어 달라고 요청해 보세요.
        </div>
        """,
        unsafe_allow_html=True,
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("메시지를 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    api_key = get_api_key()
    if not api_key:
        with st.chat_message("assistant"):
            st.info(
                "아직 API 키가 설정되지 않았어요. 배포 환경의 Secrets에 "
                "`OPENAI_API_KEY`를 추가하면 답변을 받을 수 있습니다."
            )
    else:
        with st.chat_message("assistant"):
            try:
                response = OpenAI(api_key=api_key).responses.create(
                    model=os.getenv("OPENAI_MODEL", "gpt-5"),
                    input=st.session_state.messages,
                )
                answer = response.output_text
                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            except Exception as exc:
                st.error(f"답변을 가져오지 못했어요: {exc}")
