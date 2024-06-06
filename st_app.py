# -*- coding: utf-8 -*-
import streamlit as st

with st.sidebar:
    environment_variable = st.text_input(
        "Enter your environment variable",
        key="environment_variable",
    )

st.title("Medical Multi Agent")
st.caption(":copyright: Nanyang Technological University")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "message": "Hello! How can I help you today?"},
    ]

for msg in st.session_state.messages:
    st.chat_message("assistant").write(msg["message"])

if prompt := st.chat_input():
    if not environment_variable:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    msg = "I am a placeholder message."
    st.session_state.messages.append({"role": "assistant", "content": msg})
    msg = "Another placeholder message."
    st.session_state.messages.append({"role": "Doctor", "content": msg})
    st.chat_message("Doctor").write(msg)
