"""Analysis toolkit for predicting bankruptcy of game companies.

This module demonstrates the process outlined in the user request:
1. Load data of companies, including those that went bankrupt.
2. Group bankrupt companies into a `WorkoutGroup`.
3. Analyse common financial traits.
4. Summarise potential causes.
5. Sample companies until bankrupt detection exceeds 90%.
6. Predict bankruptcy probability for a new company using a simple
   logistic regression implemented without external dependencies.

Data is expected in CSV format with the following columns:
    company,revenue_growth,operating_margin,debt_ratio,
    product_diversity,management_issues,bankrupt

All numeric fields are floats except `management_issues` and `bankrupt`
which are 0/1 integers.
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple


@dataclass
class Company:
    name: str
    revenue_growth: float
    operating_margin: float
    debt_ratio: float
    product_diversity: float
    management_issues: int
    bankrupt: int

    @staticmethod
    def from_row(row: Dict[str, str]) -> "Company":
        return Company(
            name=row["company"],
            revenue_growth=float(row["revenue_growth"]),
            operating_margin=float(row["operating_margin"]),
            debt_ratio=float(row["debt_ratio"]),
            product_diversity=float(row["product_diversity"]),
            management_issues=int(row["management_issues"]),
            bankrupt=int(row["bankrupt"]),
        )


def load_companies(path: str) -> List[Company]:
    """Load company records from a CSV file."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [Company.from_row(row) for row in reader]


def build_workout_group(data: Iterable[Company]) -> List[Company]:
    """Filter companies that went bankrupt or closed."""
    return [c for c in data if c.bankrupt == 1]


def analyse_common_traits(group: Sequence[Company]) -> Tuple[Dict[str, float], List[str]]:
    """Compute average metrics and derive qualitative traits."""
    if not group:
        return {}, []

    features = [
        "revenue_growth",
        "operating_margin",
        "debt_ratio",
        "product_diversity",
        "management_issues",
    ]
    averages: Dict[str, float] = {}
    for f in features:
        averages[f] = sum(getattr(c, f) for c in group) / len(group)

    traits: List[str] = []
    if averages["revenue_growth"] < 0:
        traits.append("declining revenue")
    if averages["operating_margin"] < 0:
        traits.append("operating losses")
    if averages["debt_ratio"] > 1.0:
        traits.append("high debt levels")
    if averages["product_diversity"] < 0.5:
        traits.append("poor product diversification")
    if averages["management_issues"] > 0:
        traits.append("management issues")

    return averages, traits


def summarise_causes(traits: Sequence[str]) -> List[str]:
    """Translate traits into possible causes."""
    cause_map = {
        "declining revenue": "Lack of successful titles or market contraction",
        "operating losses": "High operating costs relative to revenue",
        "high debt levels": "Difficulty servicing debt and securing funding",
        "poor product diversification": "Overreliance on single hit titles",
        "management issues": "Governance problems or key staff departures",
    }
    return [cause_map.get(t, t) for t in traits]


def sampling_until_detection(group: Sequence[Company], threshold: float = 0.9, max_iter: int = 1000) -> Tuple[float, int]:
    """Randomly sample companies until bankrupt detection exceeds threshold."""
    detections = 0
    total = 0
    while total < max_iter:
        c = random.choice(group)
        total += 1
        if c.bankrupt:
            detections += 1
        if total >= 10 and detections / total >= threshold:
            break
    return detections / total if total else 0.0, total


# Logistic regression -------------------------------------------------------

FEATURES = [
    "revenue_growth",
    "operating_margin",
    "debt_ratio",
    "product_diversity",
    "management_issues",
]


def train_logistic_regression(data: Sequence[Company], iterations: int = 1000, lr: float = 0.1) -> Tuple[Dict[str, float], float]:
    """Train a simple logistic regression classifier without external libs."""
    weights = {f: 0.0 for f in FEATURES}
    bias = 0.0
    n = len(data)

    for _ in range(iterations):
        grad_w = {f: 0.0 for f in FEATURES}
        grad_b = 0.0
        for c in data:
            z = sum(weights[f] * getattr(c, f) for f in FEATURES) + bias
            pred = 1 / (1 + math.exp(-z))
            error = pred - c.bankrupt
            for f in FEATURES:
                grad_w[f] += error * getattr(c, f)
            grad_b += error
        for f in FEATURES:
            weights[f] -= lr * grad_w[f] / n
        bias -= lr * grad_b / n
    return weights, bias


def predict_probability(features: Dict[str, float], weights: Dict[str, float], bias: float) -> float:
    z = sum(weights[f] * features[f] for f in FEATURES) + bias
    return 1 / (1 + math.exp(-z))


# Command-line interface ----------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Bankruptcy analysis demo")
    parser.add_argument("data", help="Path to CSV data file")
    parser.add_argument(
        "--predict",
        metavar="NAME",
        help="Predict bankruptcy probability for a company defined in code",
    )
    args = parser.parse_args()

    companies = load_companies(args.data)
    workout_group = build_workout_group(companies)

    averages, traits = analyse_common_traits(workout_group)
    causes = summarise_causes(traits)
    rate, samples = sampling_until_detection(workout_group)
    weights, bias = train_logistic_regression(companies)

    print("WorkoutGroup size:", len(workout_group))
    print("Average metrics:")
    for k, v in averages.items():
        print(f"  {k}: {v:.2f}")
    print("Common traits:", ", ".join(traits) or "None")
    print("Possible causes:", ", ".join(causes) or "None")
    print(f"Sampling detection rate: {rate:.2%} after {samples} samples")

    if args.predict:
        # For demonstration, use a hard-coded example; in real use, replace
        # these with actual data for the company to predict.
        example = {
            "revenue_growth": -0.2,
            "operating_margin": -0.1,
            "debt_ratio": 1.5,
            "product_diversity": 0.3,
            "management_issues": 1,
        }
        prob = predict_probability(example, weights, bias)
        print(f"Predicted bankruptcy probability for {args.predict}: {prob:.2%}")


if __name__ == "__main__":
    main()
