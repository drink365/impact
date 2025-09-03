
import os
import streamlit as st

def brand_header(subtitle: str = ""):
    cols = st.columns([0.16, 0.84])
    with cols[0]:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_column_width=True)
        else:
            st.empty()
    with cols[1]:
        st.markdown(
            f"""
            <div style="padding-top:8px">
              <h1 style="margin:0">影響力傳承平台｜永傳家族辦公室</h1>
              <p style="margin:6px 0 0 0; opacity:.85">{subtitle}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.divider()

def render_sidebar_nav():
    """Hide Streamlit default Pages nav then render Chinese labels."""
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"], .stSidebarNav, .css-1d391kg, nav[aria-label="Main menu"], [data-testid="stSidebarNavItems"] { display: none !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.sidebar:
        st.markdown("### 影響力傳承平台")
        st.page_link("app.py", label="首頁", icon="🏠")
        st.page_link("pages/01_family_impact.py", label="家族影響力指數", icon="🧭")
        st.page_link("pages/02_legacy_readiness.py", label="傳承準備度測驗", icon="🧪")
