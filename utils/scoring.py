
from typing import Dict, List, Tuple

def compute_family_impact_scores(questions: List[Tuple[str, str]], answers: List[int]):
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
    if strength: parts.append(f"優勢面向：{'、'.join(strength)}。")
    if mid: parts.append(f"可優化面向：{'、'.join(mid)}。")
    if weak: parts.append(f"優先改善面向：{'、'.join(weak)}。")

    summary = " ".join(parts) or "尚無資料。請完成作答以產出分析。"
    return facets, summary

def interpret_scores(scores: Dict[str, Dict[str, float]]) -> str:
    advice = []
    avg = {k: v["avg"] for k, v in scores.items()}

    if avg.get("情感連結", 0) < 3:
        advice.append("• 先安排一次以「價值觀與家族期待」為主的會議，避免一開始聚焦在稅務或產品。")
    if avg.get("財務參與度", 0) < 3.5:
        advice.append("• 建立資產列表與決策流程（誰參與、如何紀錄），提升透明度與參與感。")
    if avg.get("家族角色認同", 0) < 3.5:
        advice.append("• 明確界定角色與授權（董事會、家族委員會、受託人等），降低決策壓力集中。")
    if avg.get("傳承願景", 0) < 3.5:
        advice.append("• 用 OKR/願景版把 3-5 年目標寫下來，安排交棒時程與里程碑。")

    if not advice:
        advice.append("• 建議直接進入《傳承策略設計》與保單/信託現金流模型，建立長期護城河。")

    advice.append("• 若需協助，我們可提供顧問會議與策略落地服務（Email：123@gracefo.com）。")
    return "\n".join(advice)

def compute_legacy_readiness(questions: List[Tuple[str, str]], answers: List[int]):
    domains = {}
    for (domain, _), score in zip(questions, answers):
        bucket = domains.setdefault(domain, {"sum": 0, "cnt": 0})
        bucket["sum"] += int(score)
        bucket["cnt"] += 1
    for d, v in domains.items():
        v["avg"] = v["sum"] / max(1, v["cnt"])

    risk = {d: round(5 - v["avg"], 2) for d, v in domains.items()}

    high_risk = [d for d, r in risk.items() if r >= 2.0]
    mid_risk = [d for d, r in risk.items() if 1.0 <= r < 2.0]
    low_risk = [d for d, r in risk.items() if r < 1.0]

    parts = []
    if high_risk: parts.append(f"高風險：{'、'.join(high_risk)}（建議立即安排顧問會議）")
    if mid_risk: parts.append(f"中度風險：{'、'.join(mid_risk)}（建議 30~60 天內改善）")
    if low_risk: parts.append(f"低風險：{'、'.join(low_risk)}（維持並定期檢視）")
    summary = "；".join(parts) or "尚無資料。"

    actions = []
    if risk.get("資產透明度", 0) >= 1.0:
        actions.append("• 建立最新資產清單與權屬（含跨境資產），指定維護頻率與責任人。")
    if risk.get("稅務與合規", 0) >= 1.0:
        actions.append("• 進行跨境稅務/申報盤點（CRS/FBAR/遺贈稅），建立年度合規清單。")
    if risk.get("接班計畫", 0) >= 1.0:
        actions.append("• 設定交棒時程表與角色授權，建立家族治理/董事會會議節奏。")
    if risk.get("保險與信託", 0) >= 1.0:
        actions.append("• 用保單/信託打造長期現金流與風險隔離，定期壓力測試。")
    if not actions:
        actions.append("• 建議直接進入《傳承策略設計》與現金流模型優化，建立長期護城河。")
    actions.append("• 需要協助？來信 123@gracefo.com 安排顧問會議。")

    return domains, risk, summary, "\n".join(actions)
