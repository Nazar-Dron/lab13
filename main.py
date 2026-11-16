import csv
import json
import math
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from function_model import A, B, FORMULA, evaluate, sample, chord_deviation

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
RESULTS = ROOT / "results"
DATA = ROOT / "data"


def make_plot(x, y, path, points_count):
    fig, ax = plt.subplots(figsize=(9.5, 5.2), layout="constrained")
    ax.plot(x, y, color="#245a82", linewidth=1.6, label=r"$5\sin(10x)\sin(3x)/\sqrt{x}$")
    ax.axhline(0, linewidth=0.85, color="#555555", alpha=0.65)
    ax.set(xlim=(A, B), xlabel="x (радіани у аргументах sin)", ylabel="y",
           title=f"ЛР №13 — варіант 8 | {points_count} точок | x ∈ [1; 7]")
    ax.grid(True, alpha=0.28)
    ax.legend(loc="upper right")
    fig.savefig(path, dpi=170, metadata={"Title": "ЛР 13. Варіант 8", "Description": FORMULA})
    plt.close(fig)


def make_comparison(grids, path):
    fig, axes = plt.subplots(2, 1, figsize=(9, 7.3), layout="constrained", sharex=True)
    for ax, (n, x, y, error) in zip(axes, grids):
        ax.plot(x, y, linewidth=1.4, label=f"n={n}; індикатор середини = {error:.2e}")
        ax.set(ylabel="y", xlim=(A, B))
        ax.grid(True, alpha=0.28)
        ax.legend(loc="upper right")
    axes[-1].set_xlabel("x")
    fig.suptitle("Порівняння сіток | y = 5 sin(10x) sin(3x) / √x")
    fig.savefig(path, dpi=170)
    plt.close(fig)


def run():
    for folder in (OUTPUT, RESULTS, DATA):
        folder.mkdir(exist_ok=True)
    grids = []
    statistics = []
    for n in (1201, 2401):
        x, y = sample(n)
        deviation = chord_deviation(x, y)
        make_plot(x, y, OUTPUT / f"variant_08_{n}.png", n)
        grids.append((n, x, y, deviation))
        statistics.append({
            "n": n, "step": float(x[1]-x[0]), "finite": int(np.isfinite(y).sum()),
            "NaN": int(np.isnan(y).sum()), "chord_deviation": deviation,
            "xmin": float(x[0]), "xmax": float(x[-1]),
        })
    make_plot(grids[1][1], grids[1][2], OUTPUT / "variant_08.png", 2401)
    make_comparison(grids, OUTPUT / "grid_comparison.png")

    controls = [
        ("3π/4", 3*math.pi/4, -5/math.sqrt(2*(3*math.pi/4))),
        ("5π/4", 5*math.pi/4, -5/math.sqrt(2*(5*math.pi/4))),
        ("7π/4", 7*math.pi/4, +5/math.sqrt(2*(7*math.pi/4))),
    ]
    checks = []
    for name, x0, expected in controls:
        actual = evaluate(x0)
        checks.append({"x_name": name, "x": x0, "expected": expected,
                       "actual": actual, "abs_difference": abs(actual-expected)})

    np.savez(DATA / "curve_data.npz", x=grids[1][1], y=grids[1][2])
    with (DATA / "curve_data.csv").open("w", encoding="utf-8", newline="") as stream:
        w = csv.writer(stream)
        w.writerow(["x", "y"])
        w.writerows(zip(grids[1][1], grids[1][2]))
    report = {"variant": 8, "formula": FORMULA, "interval": [A, B],
              "python": sys.version.split()[0], "numpy": np.__version__,
              "matplotlib": matplotlib.__version__, "backend": matplotlib.get_backend(),
              "grids": statistics, "control_points": checks,
              "curve_data_for_lab14": "data/curve_data.npz"}
    (RESULTS / "results.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print("ЛР №13. Варіант 8")
    print("y =", FORMULA, ", x ∈ [1; 7]")
    for row in statistics:
        print(f"n={row['n']}, h={row['step']:.8f}, відхилення ламаної="
              f"{row['chord_deviation']:.9g}, NaN={row['NaN']}")
    print("Контрольні значення:")
    for row in checks:
        print(f"x={row['x_name']}: очікується {row['expected']:.12f}, "
              f"програма {row['actual']:.12f}, різниця {row['abs_difference']:.3e}")
    print("PNG:", OUTPUT / "variant_08.png")
    print("Дані для ЛР14:", DATA / "curve_data.npz")
    return report


if __name__ == "__main__":
    run()
