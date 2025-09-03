import numpy as np
import matplotlib.pyplot as plt

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
