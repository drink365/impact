
import streamlit as st
from utils.ui import brand_header

st.set_page_config(
    page_title="影響力傳承平台｜家族影響力指數",
    page_icon="logo2.png",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;600;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, 'Segoe UI',
                     Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans',
                     'Helvetica Neue', Arial, 'Microsoft JhengHei', 'Noto Sans CJK TC', sans-serif;
    }
    .hero { padding: 2rem; border-radius: 18px; box-shadow: 0 4px 24px rgba(0,0,0,0.06); }
    .muted {opacity: .85}
    .stRadio > label { font-weight: 600; }
    .stRadio [data-baseweb="radio"] { margin-bottom: 0.25rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

brand_header("讓家族對話更自然，讓傳承規劃更清晰")

with st.container():
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown(
            """
            <div class="hero">
            <h3>讓家族對話更自然，讓傳承規劃更清晰</h3>
            <p class="muted">本平台提供兩個入門測驗：<b>家族影響力指數</b> 與 <b>傳承準備度測驗</b>。
            在談資產與保單前，先陪伴家族理解價值觀、角色定位與潛在風險，讓每一步更安心、更有方向。</p>
            <ul>
              <li>匿名作答，三分鐘完成</li>
              <li>即時產出雷達圖與風險熱力圖</li>
              <li>可下載 CSV / 圖像，用於家族會議</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.info("**隱私聲明**：本平台預設不儲存個資與作答內容。如需建立專屬帳號或雲端保存，請在諮詢時另行開啟。")

st.divider()
st.subheader("📌 建議使用方式")
st.markdown(
    """
    1. 先至側邊欄進入 **《家族影響力指數》**，以低壓力方式開啟話題。
    2. 下載報告圖表或 CSV，做為家族會議的討論起點。
    3. 若需要專業協助，可點選下方按鈕安排諮詢，進入策略設計。
    """
)

colA, colB, colC = st.columns(3)
with colA:
    st.page_link("pages/01_family_impact.py", label="開始：《家族影響力指數》", icon="➡️")
with colB:
    st.page_link("pages/02_legacy_readiness.py", label="開始：《傳承準備度測驗》", icon="📋")
with colC:
    st.link_button("預約顧問（Email）", "mailto:123@gracefo.com?subject=預約傳承顧問&body=您好，我想預約傳承規劃諮詢。")

st.divider()
st.caption("影響力傳承平台｜永傳家族辦公室｜Email：123@gracefo.com")
