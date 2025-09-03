import numpy as np
import matplotlib.pyplot as plt

def heatmap_plot(scores: dict):
    labels = list(scores.keys())
    values = [scores[k]["avg"] for k in labels]

    fig, ax = plt.subplots(figsize=(5, 3))
    cax = ax.imshow([values], cmap="RdYlGn", vmin=0, vmax=5)

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=20)
    ax.set_yticks([])
    ax.set_title("風險熱力圖 (分數越低風險越高)")

    fig.colorbar(cax, orientation="vertical", label="平均分數(1-5)")
    return fig
