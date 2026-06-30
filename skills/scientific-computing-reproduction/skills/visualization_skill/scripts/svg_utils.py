from __future__ import annotations

from html import escape
from pathlib import Path


def _scale(values: list[float], low: float, high: float, reverse: bool = False) -> list[float]:
    if not values:
        return []
    vmin = min(values)
    vmax = max(values)
    if vmax == vmin:
        return [(low + high) / 2 for _ in values]
    scaled = [low + (value - vmin) * (high - low) / (vmax - vmin) for value in values]
    return [high - (value - low) for value in scaled] if reverse else scaled


def write_line_chart(path: Path, title: str, x_values: list[float], series: dict[str, list[float]], y_label: str = "") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    width, height = 720, 420
    left, right, top, bottom = 70, 30, 50, 60
    plot_w = width - left - right
    plot_h = height - top - bottom
    colors = ["#2563eb", "#dc2626", "#16a34a", "#9333ea", "#ea580c"]
    xs = _scale(x_values, left, left + plot_w)
    all_y = [value for values in series.values() for value in values]
    y_scaled = {name: _scale(values, top, top + plot_h, reverse=True) for name, values in series.items()}
    y_min = min(all_y) if all_y else 0
    y_max = max(all_y) if all_y else 1
    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width / 2}" y="28" text-anchor="middle" font-family="Arial" font-size="18" font-weight="700">{escape(title)}</text>',
        f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#111827"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#111827"/>',
        f'<text x="{left + plot_w / 2}" y="{height - 18}" text-anchor="middle" font-family="Arial" font-size="12">iteration / trial</text>',
        f'<text x="18" y="{top + plot_h / 2}" text-anchor="middle" font-family="Arial" font-size="12" transform="rotate(-90 18 {top + plot_h / 2})">{escape(y_label)}</text>',
        f'<text x="{left - 8}" y="{top + 5}" text-anchor="end" font-family="Arial" font-size="10">{y_max:.3g}</text>',
        f'<text x="{left - 8}" y="{top + plot_h}" text-anchor="end" font-family="Arial" font-size="10">{y_min:.3g}</text>',
    ]
    for index, (name, ys) in enumerate(y_scaled.items()):
        points = " ".join(f"{x:.2f},{y:.2f}" for x, y in zip(xs, ys))
        color = colors[index % len(colors)]
        elements.append(f'<polyline fill="none" stroke="{color}" stroke-width="2.2" points="{points}"/>')
        legend_y = top + 20 + index * 18
        elements.append(f'<line x1="{left + plot_w - 150}" y1="{legend_y}" x2="{left + plot_w - 130}" y2="{legend_y}" stroke="{color}" stroke-width="2.2"/>')
        elements.append(f'<text x="{left + plot_w - 124}" y="{legend_y + 4}" font-family="Arial" font-size="12">{escape(name)}</text>')
    elements.append("</svg>")
    path.write_text("\n".join(elements))
    return path
