import os

import httpx
import streamlit as st

API_BASE = (
    os.environ.get("API_BASE_URL")
    or f"http://{os.environ.get('API_HOST', 'localhost')}:{os.environ.get('API_PORT', '8080')}"
)

# Used for browser-facing links (OAuth button). Must be reachable from the user's browser,
# not from inside Docker — so it uses the host-accessible URL, not the internal Docker hostname.
API_PUBLIC_URL = os.environ.get("API_PUBLIC_URL") or API_BASE

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
        r = httpx.post(url=f"{API_BASE}/healthz", timeout=35)
        return r.status_code == 204
    except Exception:
        return False

with st.spinner("Connecting to server..."):
    if not ping_api():
        st.error("Backend unavailable. Please try again in a moment.")
        st.stop()
# endregion


# region SESSION STATE
if "athlete_id" not in st.session_state:
    # 1. Prefer athlete_id coming from the OAuth callback query param
    params = st.query_params
    if "athlete_id" in params:
        st.session_state.athlete_id = int(params["athlete_id"])
    else:
        # 2. Fall back to any athlete already stored in the database
        try:
            r = httpx.get(url=f"{API_BASE}/auth/athletes", timeout=10)
            ids: list[int] = r.json() if r.status_code == 200 else []
            st.session_state.athlete_id = ids[0] if ids else None
        except Exception:
            st.session_state.athlete_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []
# endregion


# region AUTH GATE
if not st.session_state.athlete_id:
    st.markdown("### Connect your Strava account")
    st.markdown("No account found in the database. Authorise once to get started.")
    st.link_button(
        label="Connect with Strava",
        url=f"{API_PUBLIC_URL}/auth/strava",
        use_container_width=True,
    )
    st.stop()
# endregion


# region CONNECT UI
athlete_id = st.session_state.athlete_id
st.success(f"Connected - Athlete ID: {athlete_id}")

if st.button(label="Sync latest activities", use_container_width=True):
    with st.spinner("Syncing from Strava..."):
        try:
            r = httpx.post(
                url=f"{API_BASE}/agent/sync",
                json={"athlete_id": athlete_id, "pages": 3},
                timeout=60,
            )
            data = r.json()
            count = len(data) if isinstance(data, list) else 0
            st.success(f"Synced {count} activities.")
        except Exception as e:
            st.error(f"Sync failed: {e}")
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
                    url=f"{API_BASE}/agent/chat",
                    json={"athlete_id": athlete_id, "message": user_input},
                    timeout=60,
                )
                reply = r.json().get("message", "No response.")
            except Exception as e:
                reply = f"Error contacting the backend: {e}"
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
# endregion