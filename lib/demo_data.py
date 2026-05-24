"""One-click demo profile for viva / presentation."""

DEMO_PROFILE = {
    "profile_age": 22,
    "profile_income": 45_000,
    "profile_sip": 12_000,
    "profile_equity": 75,
    "profile_mf_value": 185_000,
    "profile_crypto_usd": 850.0,
    "profile_emergency_fund": True,
    "profile_insurance": False,
    "profile_usd_inr": 83.5,
}


def load_demo_into_session():
    import streamlit as st

    for k, v in DEMO_PROFILE.items():
        st.session_state[k] = v
    st.session_state.demo_loaded = True
