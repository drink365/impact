import io
import pandas as pd
import streamlit as st
from utils.ui import brand_header
from utils.scoring import compute_legacy_readiness
from utils.charts import heatmap_from_dict

st.set_page_config(page_title="傳承準備度測驗", page_icon="📋", layout="wide")

brand_header("📋 傳承準備度測驗（Legacy Readiness Assessment）")
st.caption("匿名作答｜約 3-4 分鐘｜結果僅在此裝置計算與顯示")

with st.expander("測驗說明", expanded=False):
    st.markdown(
        """        目標：快速評估家族在 **資產透明度、稅務與合規、接班計畫、保險與信託** 四大面向的準備度。        產出：風險熱力圖、分數表與顧問下一步建議。        結果解讀：分數越高代表準備度越好；風險值越高代表風險越大。
        """    )

OPTIONS = {
    1: "1｜完全不同意",
    2: "2｜不同意",
    3: "3｜普通",
    4: "4｜同意",
    5: "5｜完全同意",
}

QUESTIONS = [
    # 資產透明度
    ("資產透明度", "我們有一份最新且完整的資產清單（含權屬、地區、幣別）。"),
    ("資產透明度", "對境外/跨境資產的所有權與受益人關係清晰明確。"),
    ("資產透明度", "主要資產均有相對應的文件與存證（契約、股權、信託、受益名冊）。"),
    ("資產透明度", "資產清單有指定維護人，且至少每季更新一次。"),

    # 稅務與合規
    ("稅務與合規", "我們清楚不同法域的稅務影響（遺產稅、贈與稅、所得稅、地價/房地合一等）。"),
    ("稅務與合規", "已評估跨境申報要求（如 CRS、FBAR／FATCA 等）。"),
    ("稅務與合規", "已建立年度合規檢核清單（報稅、申報、帳務保存等）。"),
    ("稅務與合規", "遇到重大交易時，會事先諮詢稅務與法律專家意見。"),

    # 接班計畫
    ("接班計畫", "企業或資產已有明確接班人與權責分工。"),
    ("接班計畫", "已擬定 3-5 年交棒時程與里程碑。"),
    ("接班計畫", "有固定的家族/董事會會議節奏與決策紀錄機制。"),
    ("接班計畫", "已規劃風險事件（失能/身故等）下的臨時接班機制。"),

    # 保險與信託
    ("保險與信託", "已有足額的人壽保險或年金，保障傳承所需現金流。"),
    ("保險與信託", "適當運用信託/保單降低風險、避免爭產、保障特定對象。"),
    ("保險與信託", "每 1-2 年檢視一次保單與信託結構的適配性與成本。"),
    ("保險與信託", "對重大風險（長照、醫療、法稅）有對應的財務預備。"),
]

with st.form("readiness_form"):
    st.subheader("請依直覺作答（1-5 分）")
    answers = []
    for i, (domain, text) in enumerate(QUESTIONS, start=1):
        answers.append(
            st.select_slider(
                f"Q{i}. {text}",
                options=list(OPTIONS.keys()),
                value=3,
                format_func=lambda k: OPTIONS[k],
            )
        )
    go = st.form_submit_button("立即產生風險分析", use_container_width=True)

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

        # Downloads
        st.markdown("### 下載結果")
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("下載 CSV", data=csv, file_name="legacy_readiness_scores.csv", mime="text/csv")

    with col2:
        st.subheader("AI 分析摘要")
        st.write(summary)

        st.subheader("顧問下一步建議")
        st.markdown(actions)


        # ==== 下載 PDF 報告 ====
        try:
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
        except Exception as e:
            st.warning("PDF 產生發生問題：{}。請確認已上傳字型與 logo 檔。".format(e))
    
    st.divider()
    with st.expander("隱私與說明", expanded=False):
        st.caption("本頁面不會自動將答案上傳至雲端。若需保存或建立團隊帳號，請於諮詢時開啟。")
else:
    st.info("完成作答後，將即時產生風險熱力圖與顧問建議。")
