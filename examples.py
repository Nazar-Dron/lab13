from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def main():
    out = Path(__file__).resolve().parent / 'output' / 'examples'
    out.mkdir(parents=True, exist_ok=True)
    x = np.linspace(0, 3, 301)
    y = x**2 * np.exp(-x**2)

    fig, ax = plt.subplots()
    ax.plot(x[::15], y[::15], 'o', label='Точки')
    ax.legend(); ax.set(title='Приклад 1 — дискретні точки', xlabel='x', ylabel='y')
    fig.savefig(out/'example_1_points.png', dpi=150);plt.close(fig)

    fig, ax = plt.subplots()
    ax.plot(x, y, label='x² exp(−x²)')
    ax.legend();ax.set(title='Приклад 2 — функція', xlabel='x',ylabel='y')
    fig.savefig(out/'example_2_function.png',dpi=150);plt.close(fig)

    fig, ax = plt.subplots()
    ax.plot(x, y, color='#245a82', linewidth=2, label='Оформлена крива')
    ax.grid(alpha=.35);ax.set(title='Приклад 3 — оформлення',xlabel='x',ylabel='y');ax.legend()
    fig.savefig(out/'example_3_styled.png',dpi=150);plt.close(fig)

    fig, ax = plt.subplots()
    for degree in (2,4,6):
        ax.plot(x, x**degree * np.exp(-x**2), label=f'x^{degree} exp(−x²)')
    ax.set(title='Приклад 4 — три криві',xlabel='x',ylabel='y')
    ax.legend();ax.grid(alpha=.3)
    fig.savefig(out/'example_4_three_curves.png',dpi=150);plt.close(fig)
    print('Чотири навчальні PNG збережено в',out)

if __name__=='__main__':
    main()
