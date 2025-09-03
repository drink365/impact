
import io
import pandas as pd
import streamlit as st
from utils.ui import brand_header, render_sidebar_nav
from utils.scoring import compute_family_impact_scores, interpret_scores
from utils.charts import radar_plot

st.set_page_config(page_title="家族影響力指數", page_icon="logo2.png", layout="wide")
render_sidebar_nav()
brand_header("家族影響力指數（匿名作答｜約 3 分鐘）")

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

mode = st.selectbox("作答模式", ["舒適模式（分頁）", "快速模式（全部題目）"])
OPTIONS = {1: "1｜完全不同意", 2: "2｜不同意", 3: "3｜普通", 4: "4｜同意", 5: "5｜完全同意"}

def ask_radio(label_key, q_text):
    return int(st.radio(label_key, list(OPTIONS.keys()), horizontal=True, format_func=lambda k: OPTIONS[k], index=2))

answers = []

if mode.startswith("舒適模式"):
    st.subheader("請依直覺作答（1-5 分）")
    tabs = st.tabs(sorted(list({f for f, _ in QUESTIONS})))
    facet_to_questions = {}
    for i, (facet, text) in enumerate(QUESTIONS, start=1):
        facet_to_questions.setdefault(facet, []).append((i, text))
    for tab, facet in zip(tabs, facet_to_questions.keys()):
        with tab:
            st.markdown(f"#### {facet}")
            for i, text in facet_to_questions[facet]:
                answers.append(ask_radio(f"Q{i}. {text}", text))
else:
    st.subheader("請依直覺作答（1-5 分）")
    left, right = st.columns(2)
    for i, (facet, text) in enumerate(QUESTIONS, start=1):
        target = left if i % 2 else right
        with target:
            answers.append(ask_radio(f"Q{i}. {text}", text))

submitted = st.button("立即產生分析結果", use_container_width=True)

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

        st.markdown("### 下載結果")
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("下載 CSV", data=csv, file_name="family_impact_scores.csv", mime="text/csv")
        png_buf = io.BytesIO()
        fig.savefig(png_buf, format="png", dpi=200, bbox_inches="tight")
        st.download_button("下載雷達圖（PNG）", data=png_buf.getvalue(), file_name="family_impact_radar.png", mime="image/png")

    with col2:
        st.subheader("AI 分析摘要")
        st.write(summary)

        st.subheader("顧問下一步建議")
        from utils.scoring import interpret_scores as _interp
        st.markdown(_interp(scores))

    from utils.pdf_utils import build_report
    pdf_bytes = build_report(
        title="家族影響力指數｜分析報告",
        subtitle="雷達圖・面向分析・顧問下一步建議",
        summary_text=summary,
        advisor_actions=_interp(scores),
        tables=[("分數明細", df)],
        images=[("家族影響力雷達圖", png_buf.getvalue())],
    )
    st.download_button("下載 PDF 報告", data=pdf_bytes, file_name="family_impact_report.pdf", mime="application/pdf", use_container_width=True)
else:
    st.info("完成作答後，將即時產生雷達圖與建議。")
