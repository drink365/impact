from typing import Dict, List, Tuple

def compute_legacy_scores(questions: List[Tuple[str, str]], answers: List[int]):
    facets = {}
    for (facet, _), score in zip(questions, answers):
        bucket = facets.setdefault(facet, {"sum": 0, "cnt": 0})
        bucket["sum"] += int(score)
        bucket["cnt"] += 1

    for facet, v in facets.items():
        v["avg"] = v["sum"] / max(1, v["cnt"])

    strength = [f for f, v in facets.items() if v["avg"] >= 4.0]
    mid = [f for f, v in facets.items() if 3.0 <= v["avg"] < 4.0]
    weak = [f for f, v in facets.items() if v["avg"] < 3.0]

    parts = []
    if strength:
        parts.append(f"成熟度高：{ '、'.join(strength) }。")
    if mid:
        parts.append(f"需優化：{ '、'.join(mid) }。")
    if weak:
        parts.append(f"高風險：{ '、'.join(weak) }。")

    summary = " ".join(parts) or "尚無資料。請完成作答以產出分析。"
    return facets, summary


def interpret_legacy_scores(scores: Dict[str, Dict[str, float]]) -> str:
    advice = []
    avg = {k: v["avg"] for k, v in scores.items()}

    if avg.get("資產透明度", 0) < 3.5:
        advice.append("• 優先完成資產清冊與文件數位化，確保透明度與安全性。")
    if avg.get("稅務與合規", 0) < 3.5:
        advice.append("• 進行跨國稅務與法律合規檢核，避免潛在風險。")
    if avg.get("接班計畫", 0) < 3.5:
        advice.append("• 啟動家族憲章與接班培訓，建立治理與交棒機制。")
    if avg.get("保險與信託", 0) < 3.5:
        advice.append("• 規劃保險與信託結構，確保現金流、稅務與慈善願景。")

    if not advice:
        advice.append("• 已具備良好基礎，建議進入策略與財務模型設計階段。")

    advice.append("• 我們可提供顧問會議，協助落地執行並設計專屬方案（Email：123@gracefo.com）。")
    return "\n".join(advice)
