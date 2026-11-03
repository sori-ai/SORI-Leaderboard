#!/usr/bin/env python3
"""
Note F1 vs Delay plot generation script with broken y-axis
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import numpy as np

def main():
    # Path setup
    root_dir = Path(__file__).parent.parent
    results_path = root_dir / "data" / "benchmarks" / "results.json"
    output_path = root_dir / "assets" / "images" / "note_f1_vs_delay.png"

    # Load data
    with open(results_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    models = {m["id"]: m for m in data["models"]}

    # Extract data
    sori_realtime = []  # (delay, note_f1, name)
    sori_offline = []
    others_realtime = []
    others_offline = []

    for result in data["benchmark_results"]:
        model_id = result["model_id"]
        model = models[model_id]
        note_f1 = result["metrics"]["note"]["f1"]
        delay_ms = model.get("delay_ms")
        is_ours = model.get("is_ours", False)
        name = model["name"]

        if note_f1 is None:
            continue

        if delay_ms is None:  # Offline
            if is_ours:
                sori_offline.append((note_f1, name))
            else:
                others_offline.append((note_f1, name))
        else:  # Realtime
            if is_ours:
                sori_realtime.append((delay_ms, note_f1, name))
            else:
                others_realtime.append((delay_ms, note_f1, name))

    # Create broken axis plot
    fig, (ax_top, ax_bottom) = plt.subplots(2, 1, figsize=(14, 10), sharex=True,
                                             gridspec_kw={'height_ratios': [4, 1], 'hspace': 0.05})

    # Y-axis ranges
    top_ylim = (84, 100)
    bottom_ylim = (68, 73)

    offline_x = 400  # Offline model x position

    # Plot function for both axes
    def plot_data(ax):
        # Sori realtime models (blue circles)
        if sori_realtime:
            delays, f1s, names = zip(*sori_realtime)
            ax.scatter(delays, f1s, c='#2563eb', s=200, marker='o', zorder=5, edgecolors='white', linewidths=2)

        # Other realtime models (gray triangles)
        if others_realtime:
            delays, f1s, names = zip(*others_realtime)
            ax.scatter(delays, f1s, c='#6b7280', s=160, marker='^', zorder=4, edgecolors='white', linewidths=1.5)

        # Sori offline models (blue squares)
        if sori_offline:
            f1s, names = zip(*sori_offline)
            ax.scatter([offline_x] * len(f1s), f1s, c='#2563eb', s=200, marker='s', zorder=5, edgecolors='white', linewidths=2)

        # Other offline models (gray squares)
        if others_offline:
            f1s, names = zip(*others_offline)
            for i, (f, n) in enumerate(zip(f1s, names)):
                x_offset = offline_x + (i % 3 - 1) * 15
                ax.scatter([x_offset], [f], c='#6b7280', s=160, marker='s', zorder=4, edgecolors='white', linewidths=1.5)

    # Plot on both axes
    plot_data(ax_top)
    plot_data(ax_bottom)

    # Set y-axis limits
    ax_top.set_ylim(top_ylim)
    ax_bottom.set_ylim(bottom_ylim)

    # Add annotations only on top axis (for high F1 models)
    # Custom offsets to avoid overlapping (x_offset, y_offset in points)
    sori_label_offsets = {
        '62ms': (0, 14),       # Normal position (legend moved to upper left)
        '125ms': (0, 14),
        '192ms': (0, 14),
        '192ms (SS)': (0, -20),  # Move below to avoid 192ms
    }

    if sori_realtime:
        delays, f1s, names = zip(*sori_realtime)
        for d, f, n in zip(delays, f1s, names):
            if f >= top_ylim[0]:
                short_name = n.replace('Sori-Realtime4.8M_', '').replace('_SS', ' (SS)')
                offset = sori_label_offsets.get(short_name, (0, 14))
                ax_top.annotate(short_name, (d, f), textcoords="offset points", xytext=offset,
                               ha='center', fontsize=12, fontweight='bold', color='#2563eb')

    if others_realtime:
        delays, f1s, names = zip(*others_realtime)
        for d, f, n in zip(delays, f1s, names):
            if f >= top_ylim[0]:
                ax_top.annotate(n, (d, f), textcoords="offset points", xytext=(0, 14),
                               ha='center', fontsize=11, color='#6b7280')

    if sori_offline:
        f1s, names = zip(*sori_offline)
        for f, n in zip(f1s, names):
            if f >= top_ylim[0]:
                short_name = n.replace('Sori-', '')
                ax_top.annotate(short_name, (offline_x, f), textcoords="offset points", xytext=(0, 14),
                               ha='center', fontsize=12, fontweight='bold', color='#2563eb')

    # Custom positions for offline models to avoid overlap (relative offsets in points)
    if others_offline:
        f1s, names = zip(*others_offline)
        # Manual positioning for each model (x_offset, y_offset in points)
        offline_label_offsets = {
            'Bytedance': (0, 14),
            'Google': (-30, -20),
            'Semi-CRF': (30, -20),
        }
        for i, (f, n) in enumerate(zip(f1s, names)):
            x_offset = offline_x + (i % 3 - 1) * 15
            if f >= top_ylim[0]:
                pos = offline_label_offsets.get(n, (0, 14))
                ax_top.annotate(n, (x_offset, f), textcoords="offset points", xytext=pos,
                               ha='center', fontsize=11, color='#6b7280')

    # Annotations for bottom axis (Spotify-light)
    if others_realtime:
        delays, f1s, names = zip(*others_realtime)
        for d, f, n in zip(delays, f1s, names):
            if bottom_ylim[0] <= f <= bottom_ylim[1]:
                ax_bottom.annotate(n, (d, f), textcoords="offset points", xytext=(0, 12),
                                  ha='center', fontsize=11, color='#6b7280')

    # Hide spines between axes
    ax_top.spines['bottom'].set_visible(False)
    ax_bottom.spines['top'].set_visible(False)
    ax_top.tick_params(bottom=False)

    # Add break marks
    d = 0.015
    kwargs = dict(transform=ax_top.transAxes, color='k', clip_on=False, linewidth=1.5)
    ax_top.plot((-d, +d), (-d, +d), **kwargs)
    ax_top.plot((1 - d, 1 + d), (-d, +d), **kwargs)
    kwargs.update(transform=ax_bottom.transAxes)
    ax_bottom.plot((-d, +d), (1 - d, 1 + d), **kwargs)
    ax_bottom.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

    # Offline region line
    ax_top.axvline(x=350, color='#e5e7eb', linestyle='--', linewidth=2, zorder=1)
    ax_bottom.axvline(x=350, color='#e5e7eb', linestyle='--', linewidth=2, zorder=1)
    ax_top.text(405, 85.5, 'Offline', ha='center', fontsize=13, color='#9ca3af', style='italic')

    # Axis settings
    ax_bottom.set_xlabel('Delay (ms)', fontsize=14, fontweight='bold')
    fig.text(0.02, 0.5, 'Note F1 (%)', va='center', rotation='vertical', fontsize=14, fontweight='bold')
    ax_top.set_title('Note F1 vs Latency Trade-off\nMAESTRO v3 Test Set', fontsize=16, fontweight='bold', pad=20)

    # X-axis range and ticks
    ax_bottom.set_xlim(0, 450)
    ax_bottom.set_xticks([0, 50, 100, 150, 200, 250, 300, 350])
    ax_bottom.set_xticklabels(['0', '50', '100', '150', '200', '250', '300', '350'], fontsize=12)

    # Y-axis ticks
    ax_top.set_yticks([85, 90, 95, 100])
    ax_top.set_yticklabels(['85', '90', '95', '100'], fontsize=12)
    ax_bottom.set_yticks([69, 71])
    ax_bottom.set_yticklabels(['69', '71'], fontsize=12)

    # Grid
    ax_top.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    ax_bottom.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    ax_top.set_axisbelow(True)
    ax_bottom.set_axisbelow(True)

    # Legend removed for cleaner look - model names are shown as annotations

    # Style
    ax_top.spines['top'].set_visible(False)
    ax_top.spines['right'].set_visible(False)
    ax_bottom.spines['right'].set_visible(False)

    plt.tight_layout()

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Plot saved to {output_path}")

    plt.close()

if __name__ == "__main__":
    main()
