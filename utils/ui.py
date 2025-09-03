
import os
import streamlit as st

def brand_header(subtitle: str = ""):
    """Render a consistent brand header with logo and subtitle on every page."""
    cols = st.columns([0.18, 0.82])
    with cols[0]:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_column_width=True)
        else:
            st.markdown("### 🏛️ 影響力傳承平台")
    with cols[1]:
        st.markdown(
            f"""
            <div style="padding-top:8px">
              <h1 style="margin-bottom:0">影響力傳承平台｜永傳家族辦公室</h1>
              <p style="margin-top:6px; opacity:.85">{subtitle}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.divider()
