import os

import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from streamlit.errors import StreamlitSecretNotFoundError


load_dotenv()

st.set_page_config(
    page_title="챗봇isgoot",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 챗봇isgoot")
st.caption("질문을 입력하면 AI가 답변해 드립니다.")


def get_api_key() -> str | None:
    if key := os.getenv("OPENAI_API_KEY"):
        return key
    try:
        return st.secrets["OPENAI_API_KEY"]
    except (KeyError, StreamlitSecretNotFoundError):
        return None


@st.cache_resource
def get_model(api_key: str):
    return init_chat_model(
        "openai:gpt-6-luna",
        reasoning_effort="none",
        api_key=api_key,
    )


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("질문해주세용"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    api_key = get_api_key()
    if not api_key:
        with st.chat_message("assistant"):
            st.info(
                "API 키가 설정되지 않았어요. Streamlit Secrets에 "
                "`OPENAI_API_KEY`를 추가해 주세요."
            )
    else:
        with st.chat_message("assistant"):
            try:
                answer = get_model(api_key).invoke(st.session_state.messages)
                answer_text = answer.text
                st.markdown(answer_text)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer_text}
                )
            except Exception as exc:
                st.error(f"답변을 가져오지 못했어요: {exc}")
