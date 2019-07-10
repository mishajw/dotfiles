#!/usr/bin/env python

from typing import List
import argparse
import numpy as np
import sys

def main(modes: List[str]):
    np.set_printoptions(
        formatter={'float': format_float},
        linewidth=1e6)
    xs = get_input()

    for mode in args.modes:
        assert mode in MODE_DICT
        result = MODE_DICT[mode](xs)
        # Ensure it's a numpy array
        result = np.array(result)
        if result.shape == ():
            result = format_float(result)
        print(f"{mode}\t{result}")

def get_input() -> np.array:
    return np.array([
        [float(value_str) for value_str in line.strip().split()]
        for line in sys.stdin
        if line.strip()])

def get_correlation(xss) -> float:
    if xss.shape[1] == 2:
        return np.corrcoef([xs[0] for xs in xss], [xs[1] for xs in xss])[0, 1]
    else:
        return np.corrcoef(xss.transpose())

def get_avg_ratio(xss) -> float:
    assert xss.shape[1] == 2
    return sum(
        xs[0] / xs[1] if xs[1] != 0 else 0
        for xs in xss) / len(xss)

def get_quantiles(xs) -> List[float]:
    return [np.percentile(xs, i) for i in range(0, 101, 10)]

MODE_DICT = {
    "sum": np.sum,
    "mean": np.mean,
    "med": np.median,
    "std": np.std,
    "min": np.min,
    "max": np.max,
    "corr": get_correlation,
    "ratio": get_avg_ratio,
    "quant": get_quantiles,
    "shape": np.shape,
}

def format_float(f: float) -> str:
    return "{0:0.3f}".format(f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("math")
    parser.add_argument(
        "modes", choices=MODE_DICT.keys(), nargs="+")
    args = parser.parse_args()
    main(args.modes)
