import numpy as np

A = 1.0
B = 7.0
FORMULA = "5*sin(10*x)*sin(3*x)/sqrt(x)"


def evaluate(x):
    try:
        values = np.asarray(x, dtype=float)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError("x має бути числом або масивом чисел") from error
    if not np.all(np.isfinite(values)) or np.any(values < A) or np.any(values > B):
        raise ValueError("Кожне x має бути скінченним числом у межах [1; 7]")
    result = 5 * np.sin(10 * values) * np.sin(3 * values) / np.sqrt(values)
    return float(result) if result.ndim == 0 else result


def sample(n=2401):
    if type(n) is not int or n < 3:
        raise ValueError("n має бути цілим числом не менше 3 (bool не допускається)")
    x = np.linspace(A, B, n)
    return x, evaluate(x)


def chord_deviation(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or len(x) < 2 or y.shape != x.shape:
        raise ValueError("Потрібні два одновимірні масиви однакової довжини >= 2")
    if not np.all(np.diff(x) > 0):
        raise ValueError("Точки x мають бути впорядковані за зростанням")
    mid = (x[:-1] + x[1:]) / 2
    reference = evaluate(mid)
    straight = (y[:-1] + y[1:]) / 2
    return float(np.max(np.abs(reference - straight)))
