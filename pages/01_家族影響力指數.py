import io
import json
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from utils.scoring import compute_family_impact_scores, interpret_scores
from utils.charts import radar_plot

st.set_page_config(page_title="家族影響力指數", page_icon="🧭", layout="wide")

st.title("🧭 家族影響力指數（Family Legacy Impact Index）")
st.caption("匿名作答｜約 3 分鐘｜結果僅在此裝置計算與顯示")

with st.expander("為什麼做這份測驗？", expanded=False):
    st.markdown(
        """
        - 幫助家族在不談數字的情況下，先釐清 **角色、參與、情感與願景**。
        - 以人為本的對話入口，避免一開始就陷入產品討論。
        - 讓下一步（家族會議 / 顧問諮詢）變得自然、有效。
        """
    )

# ---------------- Likert options ----------------
OPTIONS = {
    1: "1｜完全不同意",
    2: "2｜不同意",
    3: "3｜普通",
    4: "4｜同意",
    5: "5｜完全同意",
}

# ---------------- Questions ----------------
QUESTIONS = [
    ("家族角色認同", "我清楚知道自己在家族中的責任與影響力。"),
    ("家族角色認同", "我願意在需要時承擔家族的決策責任。"),
    ("家族角色認同", "我能夠代表家族做出理性且負責任的決策。"),
    ("財務參與度", "我了解家族資產的主要分布與結構。"),
    ("財務參與度", "我參與過家族重大財務決策的討論。"),
    ("財務參與度", "我知道家族資產未來的分配與管理計畫。"),
    ("情感連結", "我們家族成員之間有開放且尊重的溝通。"),
    ("情感連結", "家族成員之間能彼此支持，並共同面對挑戰。"),
    ("情感連結", "我感受到家族成員之間的情感與信任連結很強。"),
    ("傳承願景", "我們家族對下一代的願景是清晰一致的。"),
    ("傳承願景", "我們已經討論過家族的長期目標與計劃。"),
    ("傳承願景", "家族成員都同意需要一個明確的傳承與交棒方案。"),
]

with st.form("impact_form"):
    st.subheader("請依直覺作答（1-5 分）")
    answers = []
    for i, (facet, text) in enumerate(QUESTIONS, start=1):
        answers.append(
            st.select_slider(
                f"Q{i}. {text}",
                options=list(OPTIONS.keys()),
                value=3,
                format_func=lambda k: OPTIONS[k],
            )
        )
    col_submit = st.columns([1,3,1])[1]
    with col_submit:
        submitted = st.form_submit_button("立即產生分析結果", use_container_width=True)

if submitted:
    scores, summary = compute_family_impact_scores(QUESTIONS, answers)
    col1, col2 = st.columns([1.2, 1], vertical_alignment="top")

    with col1:
        st.subheader("雷達圖｜四大面向概覽")
        fig = radar_plot(scores)
        st.pyplot(fig, use_container_width=True)

        st.subheader("分數明細")
        df = pd.DataFrame({
            "面向": list(scores.keys()),
            "總分(滿分15)": [v["sum"] for v in scores.values()],
            "平均(1-5)": [round(v["avg"], 2) for v in scores.values()],
        })
        st.dataframe(df, hide_index=True, use_container_width=True)

        # Downloads
        st.markdown("### 下載結果")
        # CSV
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("下載 CSV", data=csv, file_name="family_impact_scores.csv", mime="text/csv")
        # PNG of chart
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
        st.download_button("下載雷達圖（PNG）", data=buf.getvalue(), file_name="family_impact_radar.png", mime="image/png")

    with col2:
        st.subheader("AI 觀察摘要")
        st.write(summary)

        st.subheader("顧問建議（下一步）")
        st.markdown(interpret_scores(scores))

    st.divider()
    with st.expander("隱私與說明", expanded=False):
        st.caption("本頁面不會自動將答案上傳至雲端。若需保存或建立團隊帳號，請於諮詢時開啟。")

else:
    st.info("完成作答後，將即時產生雷達圖與建議。")
