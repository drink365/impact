import numpy as np
import matplotlib.pyplot as plt
import os

import matplotlib

# Try to register local Noto Sans TC for Chinese labels
try:
    from matplotlib import font_manager
    for p in ["NotoSansTC-Regular.ttf", "./NotoSansTC-Regular.ttf", "assets/NotoSansTC-Regular.ttf"]:
        if os.path.exists(p):
            font_manager.fontManager.addfont(p)
            matplotlib.rcParams['font.family'] = 'Noto Sans TC'
            break
    matplotlib.rcParams['axes.unicode_minus'] = False
except Exception:
    pass

def radar_plot(scores: dict):
    """Create a radar chart from facet scores (expects .avg in 1-5)."""
    labels = list(scores.keys())
    values = [scores[k]["avg"] for k in labels]
    # Close the polygon
    values += values[:1]
    num_vars = len(labels)

    angles = np.linspace(0, 2*np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig = plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_rlabel_position(0)
    ax.set_ylim(0, 5)
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.1)
    return fig


def heatmap_from_dict(risk_dict: dict):
    """Draw a simple heatmap from a dict of {domain: risk_value}. Lower is better.
    Uses default colormap; no custom colors set.
    """
    import numpy as np
    import matplotlib.pyplot as plt
    labels = list(risk_dict.keys())
    values = np.array([risk_dict[k] for k in labels]).reshape(1, -1)
    fig = plt.figure(figsize=(6, 2.2))
    ax = plt.subplot(111)
    im = ax.imshow(values, aspect='auto')
    ax.set_yticks([])
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=20, ha='right')
    for j, v in enumerate(values[0]):
        ax.text(j, 0, f"{v:.1f}", ha='center', va='center')
    ax.set_title("風險熱力圖｜0 = 低風險；數值越高風險越高")
    return fig
