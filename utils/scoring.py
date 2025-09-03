from typing import Dict, List, Tuple

def compute_family_impact_scores(questions: List[Tuple[str, str]], answers: List[int]):
    """
    Aggregate scores by facet. Each answer is 1-5.
    Returns (scores_by_facet, summary_text).
    """
    facets = {}
    for (facet, _), score in zip(questions, answers):
        bucket = facets.setdefault(facet, {"sum": 0, "cnt": 0})
        bucket["sum"] += int(score)
        bucket["cnt"] += 1

    for facet, v in facets.items():
        v["avg"] = v["sum"] / max(1, v["cnt"])

    # Summary synthesis (simple rule-based)
    strength = [f for f, v in facets.items() if v["avg"] >= 4.0]
    mid = [f for f, v in facets.items() if 3.0 <= v["avg"] < 4.0]
    weak = [f for f, v in facets.items() if v["avg"] < 3.0]

    parts = []
    if strength:
        parts.append(f"優勢面向：{ '、'.join(strength) }。")
    if mid:
        parts.append(f"可優化面向：{ '、'.join(mid) }。")
    if weak:
        parts.append(f"優先改善面向：{ '、'.join(weak) }。")

    summary = " ".join(parts) or "尚無資料。請完成作答以產出分析。"
    return facets, summary


def interpret_scores(scores: Dict[str, Dict[str, float]]) -> str:
    """Produce advisor-oriented next-step suggestions based on facet averages."""
    advice = []
    avg = {k: v["avg"] for k, v in scores.items()}

    if avg.get("情感連結", 0) < 3:
        advice.append("• 先安排一次以「價值觀與家族期待」為主的會議，避免一開始聚焦在稅務或產品。")
    if avg.get("財務參與度", 0) < 3.5:
        advice.append("• 建立資產列表與決策流程（誰參與、如何紀錄），提升透明度與參與感。")
    if avg.get("家族角色認同", 0) < 3.5:
        advice.append("• 明確界定角色與授權（董事會、家族委員會、信託受託人等），降低決策壓力集中。")
    if avg.get("傳承願景", 0) < 3.5:
        advice.append("• 用 OKR/願景版把 3-5 年目標寫下來，安排交棒時程與關鍵里程碑。")

    if not advice:
        advice.append("• 建議直接進入《傳承策略設計》與保單/信託現金流模型，建立長期護城河。")

    advice.append("• 若需協助，我們可提供顧問會議與策略落地服務（Email：123@gracefo.com）。")
    return "\n".join(advice)
