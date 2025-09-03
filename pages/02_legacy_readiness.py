
import io
import pandas as pd
import streamlit as st
from utils.ui import brand_header, render_sidebar_nav
from utils.scoring import compute_legacy_readiness
from utils.charts import heatmap_from_dict

st.set_page_config(page_title="傳承準備度測驗", page_icon="logo2.png", layout="wide")
render_sidebar_nav()
brand_header("傳承準備度測驗（匿名作答｜約 3-4 分鐘）")

QUESTIONS = [
    ("資產透明度", "我們有一份最新且完整的資產清單（含權屬、地區、幣別）。"),
    ("資產透明度", "對境外/跨境資產的所有權與受益人關係清晰明確。"),
    ("資產透明度", "主要資產均有相對應的文件與存證（契約、股權、信託、受益名冊）。"),
    ("資產透明度", "資產清單有指定維護人，且至少每季更新一次。"),

    ("稅務與合規", "我們清楚不同法域的稅務影響（遺產稅、贈與稅、所得稅、地價/房地合一等）。"),
    ("稅務與合規", "已評估跨境申報要求（如 CRS、FBAR／FATCA 等）。"),
    ("稅務與合規", "已建立年度合規檢核清單（報稅、申報、帳務保存等）。"),
    ("稅務與合規", "遇到重大交易時，會事先諮詢稅務與法律專家意見。"),

    ("接班計畫", "企業或資產已有明確接班人與權責分工。"),
    ("接班計畫", "已擬定 3-5 年交棒時程與里程碑。"),
    ("接班計畫", "有固定的家族/董事會會議節奏與決策紀錄機制。"),
    ("接班計畫", "已規劃風險事件（失能/身故等）下的臨時接班機制。"),

    ("保險與信託", "已有足額的人壽保險或年金，保障傳承所需現金流。"),
    ("保險與信託", "適當運用信託/保單降低風險、避免爭產、保障特定對象。"),
    ("保險與信託", "每 1-2 年檢視一次保單與信託結構的適配性與成本。"),
    ("保險與信託", "對重大風險（長照、醫療、法稅）有對應的財務預備。"),
]

mode = st.selectbox("作答模式", ["舒適模式（分頁）", "快速模式（全部題目）"])
OPTIONS = {1: "1｜完全不同意", 2: "2｜不同意", 3: "3｜普通", 4: "4｜同意", 5: "5｜完全同意"}

def ask_radio(label_key, q_text):
    return int(st.radio(label_key, list(OPTIONS.keys()), horizontal=True, format_func=lambda k: OPTIONS[k], index=2))

answers = []

if mode.startswith("舒適模式"):
    st.subheader("請依直覺作答（1-5 分）")
    tabs = st.tabs(sorted(list({d for d, _ in QUESTIONS})))
    domain_to_questions = {}
    for i, (domain, text) in enumerate(QUESTIONS, start=1):
        domain_to_questions.setdefault(domain, []).append((i, text))
    for tab, domain in zip(tabs, domain_to_questions.keys()):
        with tab:
            st.markdown(f"#### {domain}")
            for i, text in domain_to_questions[domain]:
                answers.append(ask_radio(f"Q{i}. {text}", text))
else:
    st.subheader("請依直覺作答（1-5 分）")
    left, right = st.columns(2)
    for i, (domain, text) in enumerate(QUESTIONS, start=1):
        target = left if i % 2 else right
        with target:
            answers.append(ask_radio(f"Q{i}. {text}", text))

go = st.button("立即產生風險分析", use_container_width=True)

if go:
    domains, risk, summary, actions = compute_legacy_readiness(QUESTIONS, answers)

    col1, col2 = st.columns([1.2, 1], vertical_alignment="top")
    with col1:
        st.subheader("風險熱力圖")
        fig = heatmap_from_dict(risk)
        st.pyplot(fig, use_container_width=True)

        st.subheader("分數與風險值")
        df = pd.DataFrame({
            "面向": list(domains.keys()),
            "總分(滿分20)": [v["sum"] for v in domains.values()],
            "平均(1-5)": [round(v["avg"], 2) for v in domains.values()],
            "風險值(0-4, 越高越需留意)": [risk[k] for k in domains.keys()],
        })
        st.dataframe(df, hide_index=True, use_container_width=True)

        st.markdown("### 下載結果")
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("下載 CSV", data=csv, file_name="legacy_readiness_scores.csv", mime="text/csv")

    with col2:
        st.subheader("AI 分析摘要")
        st.write(summary)

        st.subheader("顧問下一步建議")
        st.markdown(actions)

    from utils.pdf_utils import build_report
    png_buf = io.BytesIO()
    fig.savefig(png_buf, format="png", dpi=200, bbox_inches="tight")
    pdf_bytes = build_report(
        title="傳承準備度測驗｜分析報告",
        subtitle="風險熱力圖・分數摘要・顧問下一步建議",
        summary_text=summary,
        advisor_actions=actions,
        tables=[("分數與風險值", df)],
        images=[("傳承風險熱力圖", png_buf.getvalue())],
    )
    st.download_button("下載 PDF 報告", data=pdf_bytes, file_name="legacy_readiness_report.pdf", mime="application/pdf", use_container_width=True)
else:
    st.info("完成作答後，將即時產生風險熱力圖與顧問建議。")
