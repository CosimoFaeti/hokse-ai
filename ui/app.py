import httpx
import streamlit as st

from src.domain.utilities.settings import SETTINGS


st.set_page_config(
    page_title="Hokse-ai",
    page_icon="🏃",
    layout="centered",
)

st.title("Hokse-ai 🏃 Strava AI Agent")
st.caption("Your personal training coach, powered by AI")


# region WAKE UP
@st.cache_data(ttl=300, show_spinner=False)
def ping_api() -> bool:
    try:
        r = httpx.get(url=f"http://{SETTINGS.HOST}:{SETTINGS.PORT}/health", timeout=35)
        return r.status_code == 200
    except Exception:
        return False

with st.spinner("Connecting to server..."):
    if not ping_api():
        st.error("Backend unavailable. Please try again in a moment.")
        st.stop()
# endregion


# region SESSION STATE
if "athlete_id" not in st.session_state:
    params = st.query_params
    st.session_state.athlete_id = int(params["athlete_id"] if "athlete_id" in params else None)

if "messages" not in st.session_state:
    st.session_state.messages = []
# endregion


# region AUTH GATE
if not st.session_state.athlete_id:
    st.markdown("### Connect your Strava account")
    st.markdown(
        "Click to authorise the agent to read your activities."
    )
    st.link_button(
        label="Connect with Strava",
        url=f"http://{SETTINGS.HOST}:{SETTINGS.PORT}/auth/strava",
        use_container_width=True,
    )
    st.stop()
# endregion


# region CONNECT UI
athlete_id = st.session_state.athlete_id
st.success(f"Connected - Athlete ID: {athlete_id}")

col1, col2 = st.columns(2)

with col1:
    if st.button(label="Sync latest activities", use_container_width=True):
        with st.spinner("Syncing from Strava..."):
            try:
                r = httpx.post(
                    url=f"http://{SETTINGS.HOST}:{SETTINGS.PORT}/agent/sync",
                    json={"athlete_id": athlete_id, "pages": 3},
                    timeout=60,
                )
                data = r.json()
                st.success(data.get("message", "Sync complete"))
            except Exception as e:
                st.error(f"Sync failed: {e}")

with col2:
    if st.button(label="Disconnect", use_container_width=True):
        try:
            httpx.delete(url=f"http://{SETTINGS.HOST}:{SETTINGS.PORT}/auth/{athlete_id}", timeout=10)
        except Exception:
            pass
        st.session_state.athlete_id = None
        st.session_state.messages   = []
        st.query_params.clear()
        st.rerun()
st.divider()
# endregion


# region CHAT
st.markdown("### Ask your coach")

SUGGESTIONS = [
    "Am I overtraining?",
    "How does this week compare to last week?",
    "What's my pace trend over the last 8 weeks?",
    "Give me a summary of my last 10 activities.",
]

cols = st.columns(2)
for i, prompt in enumerate(SUGGESTIONS):
    if cols[i % 2].button(prompt, key=f"sug_{i}", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": prompt})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ask about your training..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                r = httpx.post(
                    url=f"https://{SETTINGS.HOST}:{SETTINGS:PORT}/agent/chat",
                    json={"athlete_id": athlete_id, "message": user_input},
                    timeout=60,
                )
                reply = r.json().get("reply", "No response.")
            except Exception as e:
                reply = f"Error contacting the backend: {e}"
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
# endregion