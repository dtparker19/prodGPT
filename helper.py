import streamlit as st
import openai
from openai.error import InvalidRequestError, OpenAIError
from typing import List
from tts import show_audio_player
from streamlit_chat import message

def clear_chat() -> None:
    st.session_state.generated = []
    st.session_state.past = []
    st.session_state.messages = []
    st.session_state.user_text = ""
    
    
def show_text_input() -> None:
    st.session_state.chat_placeholder = "Start Your Conversation With AI:"
    st.text_area(label=st.session_state.chat_placeholder, value=st.session_state.user_text, key="user_text")

def show_chat_buttons() -> None:
    st.session_state.chat_run_btn = "Submit Request"
    st.session_state.chat_clear_btn = "Clear Request"
    st.session_state.chat_save_btn = "Save Request"
    b0, b1, b2 = st.columns(3)
    with b0, b1, b2:
        b0.button(label=st.session_state.chat_run_btn)
        b1.button(label=st.session_state.chat_clear_btn, on_click=clear_chat)
        b2.download_button(
            label=st.session_state.chat_save_btn,
            data="\\n".join([str(d) for d in st.session_state.messages[1:]]),
            file_name="ai-talks-chat.json",
            mime="application/json",
        )

def show_chat(ai_content: str, user_text: str) -> None:
    if ai_content not in st.session_state.generated:
        # store the ai content
        st.session_state.past.append(user_text)
        st.session_state.generated.append(ai_content)
    if st.session_state.generated:
        for i in range(len(st.session_state.generated)):
            message(st.session_state.past[i], is_user=True, key=str(i) + "_user", avatar_style="micah")
            message("", key=str(i))
            st.markdown(st.session_state.generated[i])

def create_gpt_completion(ai_model: str, messages: List[dict]) -> dict:
    openai.api_key = st.secrets.api_credentials
    completion = openai.ChatCompletion.create(
        model=ai_model,
        messages=messages,
    )
    return completion

def show_gpt_conversation() -> None:
    try:
        completion = create_gpt_completion(st.session_state.model, st.session_state.messages)
        ai_content = completion.get("choices")[0].get("message").get("content")
        st.session_state.messages.append({"role": "assistant", "content": ai_content})
        if ai_content:
            show_chat(ai_content, st.session_state.user_text)
            st.divider()
            show_audio_player(ai_content)
    except InvalidRequestError as err:
        if err.code == "context_length_exceeded":
            st.session_state.messages.pop(1)
            if len(st.session_state.messages) == 1:
                st.session_state.user_text = ""
            show_conversation()
        else:
            st.error(err)
    except (OpenAIError, UnboundLocalError) as err:
        st.error(err)
        
def show_conversation() -> None:
    if st.session_state.messages:
        st.session_state.messages.append({"role": "user", "content": st.session_state.user_text})
    else:
        ai_role = f"{st.session_state.ai_role_prefix} {st.session_state.role}. {st.session_state.ai_role_postfix}"  # NOQA: E501
        st.session_state.messages = [
            {"role": "system", "content": ai_role},
            {"role": "user", "content": st.session_state.user_text},
        ]
    show_gpt_conversation()        


