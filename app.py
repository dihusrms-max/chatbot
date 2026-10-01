import os

import streamlit as st
from openai import OpenAI
from streamlit.errors import StreamlitSecretNotFoundError


st.set_page_config(page_title="샤이니 챗봇", page_icon="🤖")
st.title("🤖 샤이니 챗봇")
st.caption("궁금한 내용을 편하게 물어보세요.")


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
    st.header("설정")
    st.caption("실제 AI 답변을 사용하려면 OPENAI_API_KEY를 설정하세요.")
    if st.button("대화 지우기"):
        st.session_state.messages = []
        st.rerun()

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
