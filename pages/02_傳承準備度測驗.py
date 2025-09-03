import streamlit as st

st.set_page_config(page_title="傳承準備度測驗（預告）", page_icon="📋", layout="wide")

st.title("📋 傳承準備度測驗（預告）")
st.caption("此模組將評估：資產透明度、稅務合規、接班計劃、保險與信託結構等四大面向。")

st.markdown(
    """
    我們將在下一版提供可操作的測驗與風險熱力圖，內容包含：
    - 15 條關鍵檢核題（1-5 分 Likert 量表）
    - 即時產出風險熱度圖與高風險提醒
    - 建議下一步（家族會議 / 顧問諮詢 / 策略設計）
    """
)

st.info("若您希望優先體驗此模組，請來信：123@gracefo.com")
