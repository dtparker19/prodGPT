import streamlit as st
from streamlit_option_menu import option_menu
from helper import show_chat_buttons, show_text_input, show_conversation


# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "ProdigyGPT"
PAGE_ICON: str = "🤖"
LANG_EN: str = "En"
AI_MODEL_OPTIONS: list[str] = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-32k",
]
AI_ROLE_OPTIONS_EN: list[str] = [
    "helpful assistant",
    "code assistant",
    "code reviewer",
    "text improver",
    "cinema expert",
    "sport expert",
    "online games expert",
    "food recipes expert",
    "English grammar expert",
    "friendly and helpful teaching assistant",
    "laconic assistant",
    "helpful, pattern-following assistant",
    "translate corporate jargon into plain English",
]

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

selected_lang = option_menu(
    menu_title=None,
    options=[LANG_EN],
    icons=["globe2", "translate"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Storing The Context
if "locale" not in st.session_state:
    st.session_state.locale = LANG_EN
if "generated" not in st.session_state:
    st.session_state.generated = []
if "past" not in st.session_state:
    st.session_state.past = []
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_text" not in st.session_state:
    st.session_state.user_text = ""
if "title" not in st.session_state:
    st.session_state.title = "ProdigyGPT"
if "select_placeholder1" not in st.session_state:
    st.session_state.select_placeholder1 = "Select Model"        
if "radio_placeholder" not in st.session_state:
    st.session_state.radio_placeholder = "Role Interaction"        
if "radio_text1" not in st.session_state:
    st.session_state.radio_text1 = "Select"        
if "radio_text2" not in st.session_state:
    st.session_state.radio_text2 = "Create"        
if "select_placeholder2" not in st.session_state:
    st.session_state.select_placeholder2 = "Select Role"        
if "ai_role_options" not in st.session_state:
    st.session_state.ai_role_options = AI_ROLE_OPTIONS_EN
if "select_placeholder3" not in st.session_state:
    st.session_state.select_placeholder3 = "Create Role"        
if "ai_role_prefix" not in st.session_state:
    st.session_state.ai_role_prefix="You are a female",
if "ai_role_postix" not in st.session_state:
    st.session_state.ai_role_postfix="Answer as concisely as possible"
if "lang_code" not in st.session_state:
    st.session_state.lang_code="en"    
if "stt_placeholder" not in st.session_state:
    st.session_state.stt_placeholder="STT Placeholder"  

def show_sidebar():
    with st.sidebar:
        for i in range(len(st.session_state.generated)):
            with st.expander(st.session_state.past[i]):
                st.session_state.generated[i]
            st.divider()    
      
def main() -> None:
    c1, c2 = st.columns(2)
    with c1, c2:
        c1.selectbox(label=st.session_state.select_placeholder1, key="model", options=AI_MODEL_OPTIONS)
        role_kind = c1.radio(
            label=st.session_state.radio_placeholder,
            options=(st.session_state.radio_text1, st.session_state.radio_text2),
            horizontal=True,
        )
        match role_kind:
            case st.session_state.radio_text1:
                c2.selectbox(label=st.session_state.select_placeholder2, key="role",
                             options=st.session_state.ai_role_options)
            case st.session_state.radio_text2:
                c2.text_input(label=st.session_state.select_placeholder3, key="role")
    if st.session_state.user_text:
        show_conversation()
        st.session_state.user_text = ""
    show_text_input()
    show_chat_buttons()
    show_sidebar()

if __name__ == "__main__":
    st.markdown(f"<h1 style='text-align: center;'>{st.session_state.title}</h1>", unsafe_allow_html=True)
    main()