import streamlit as st

st.set_page_config(
    page_title="影響力傳承平台｜家族影響力指數",
    page_icon="🏛️",
    layout="wide",
)

# --------- Global Style ---------
st.markdown(
    '''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;600;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, 'Segoe UI',
                     Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans',
                     'Helvetica Neue', Arial, 'Microsoft JhengHei', 'Noto Sans CJK TC', sans-serif;
    }
    .hero {
        padding: 2rem;
        border-radius: 18px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.06);
    }
    .muted {opacity: .85}
    </style>
    ''',
    unsafe_allow_html=True,
)

# --------- Header ---------
st.title("🏛️ 影響力傳承平台 | 永傳家族辦公室")
st.caption("以人為本｜情感 × 風險 × 信任｜陪您把重要的事說清楚、做紮實")

with st.container():
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown(
            """
            <div class="hero">
            <h3>從「不想談」到「願意行動」：以《一如既往》的恆久原則，打造可落地的傳承工具</h3>
            <p class="muted">本平台提供兩個入門測驗：<b>《家族影響力指數》</b> 與 <b>《傳承準備度測驗》</b>。            不先談保單與資產金額，而是先理解價值觀、角色與風險，讓每一步都更穩健。</p>
            <ul>
              <li>匿名作答，三分鐘完成</li>
              <li>即時產出雷達圖與風險熱點</li>
              <li>可下載 CSV / 圖像，用於家族會議</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.info(
            "**隱私聲明**：本平台預設不儲存個資與作答內容。"
            " 如需建立專屬帳號或雲端保存，請在諮詢時另行開啟。"
        )

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
    st.page_link("pages/01_家族影響力指數.py", label="開始：《家族影響力指數》", icon="➡️")
with colB:
    st.page_link("pages/02_傳承準備度測驗.py", label="預告：《傳承準備度測驗》", icon="📋")
with colC:
    st.link_button("預約顧問（Email）", "mailto:123@gracefo.com?subject=預約傳承顧問&body=您好，我想預約傳承規劃諮詢。")

st.divider()
st.caption("《影響力》傳承策略平台｜永傳家族辦公室｜Email：123@gracefo.com")
