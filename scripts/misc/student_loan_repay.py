#!/usr/bin/env bash

# pylint: disable=missing-docstring

from typing import NamedTuple, Optional
import argparse
import matplotlib.pyplot as plt

REPAYMENTS = list(range(200, 1001, 10))
WRITE_OFF_YEAR = 30


class RepaymentResult(NamedTuple):
    months_to_repay: Optional[int]
    payment_left: float
    amount_spent: float

    def years(self) -> float:
        if self.months_to_repay is None:
            return WRITE_OFF_YEAR
        return self.months_to_repay / 12

    def __str__(self) -> str:
        if self.months_to_repay is not None:
            return f"{self.years():.2f} years, £{self.amount_spent:.2f} spent"
        return (
            f"never repaid, "
            f"£{self.amount_spent:.2f} spent, "
            f"£{self.payment_left:.2f} left"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=float, required=True)
    parser.add_argument("--interest", type=float, required=True)
    args = parser.parse_args()

    start = args.start
    assert start > 0
    interest = args.interest
    assert 0 < interest < 1

    results = []
    for repayment in REPAYMENTS:
        result = __get_repay_month(start, interest, repayment)
        print(f"For repayment £{repayment}: {result}")
        results.append(result)

    _, ax1 = plt.subplots()
    ax1.set_title("Student loan repayments")

    ax1.set_xlabel("Monthly repayment")
    ax1.set_ylabel("Total spent")
    ax1.plot(REPAYMENTS, [r.amount_spent for r in results], color="red")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Years to repay")
    ax2.plot(REPAYMENTS, [r.years() for r in results], color="blue")

    plt.show()


def __get_repay_month(
    start: float, interest: float, repayment: float
) -> RepaymentResult:
    loan = start
    spent = 0.0
    for month in range(WRITE_OFF_YEAR * 12):
        loan *= 1 + (interest / 12)
        loan -= repayment
        spent += repayment
        if loan < 0:
            return RepaymentResult(month, 0, spent + loan)
    return RepaymentResult(None, loan, spent)


if __name__ == "__main__":
    main()
