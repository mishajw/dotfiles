#!/usr/bin/env python

"""
Time budgetting

Checks how many hours in a day are taken up by regular events, in order to
check the "time expense" of picking up a new hobbie (possibly the saddest thing
in my dotfiles) (how much time do I spend time budgetting?).
"""

# pylint: disable=missing-docstring

from datetime import timedelta
from enum import Enum
from typing import Dict, List


def main():
    tasks: TaskMap = combine(
        UNAVOIDABLE + SHOULD_AVOID + PRODUCTIVE + WANT_TO_DO
    )
    days: DayMap = transpose(tasks)
    print_days(days)
    print()
    print_tasks(tasks)


class Day(Enum):
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6
    SUN = 7


TaskMap = Dict[str, Dict[Day, timedelta]]
DayMap = Dict[Day, Dict[str, timedelta]]


def hours(hours_float: float) -> timedelta:
    return timedelta(hours=hours_float)


def time_fmt(time: timedelta) -> str:
    if time < hours(24):
        return f"{time.total_seconds() / 60 / 60:.2f}h"
    return f"{time.total_seconds() / 60 / 60 / 24:.2f}d"


def every_day(task: str, time: timedelta) -> TaskMap:
    return {task: dict((d, time) for d in Day)}


def on_weekdays(task: str, time: timedelta) -> TaskMap:
    return {task: dict((Day(d), time) for d in range(1, 6))}


def on_weekends(task: str, time: timedelta) -> TaskMap:
    return {task: dict((Day(d), time) for d in range(6, 8))}


def on_day(day: Day, task: str, time: timedelta) -> TaskMap:
    return {task: {day: time}}


def combine(task_maps: List[TaskMap]) -> TaskMap:
    tasks: TaskMap = {}
    for task_map in task_maps:
        for task in task_map:
            if task not in tasks:
                tasks[task] = {}
            for day in task_map[task]:
                if day not in tasks[task]:
                    tasks[task][day] = hours(0)
                tasks[task][day] += task_map[task][day]
    return tasks


def transpose(tasks: TaskMap) -> DayMap:
    days: DayMap = {}
    for task in tasks:
        for day in tasks[task]:
            if day not in days:
                days[day] = {}
            if task not in days[day]:
                days[day][task] = hours(0)
            days[day][task] += tasks[task][day]
    return days


def print_days(days: DayMap) -> None:
    print("DAY", "OCC%", "OCC", "FREE", "TASKS", sep="\t")
    for day in days:
        occupied = sum(days[day].values(), hours(0))
        remaining = hours(24) - occupied
        percent_occupied = int(
            occupied.total_seconds() / hours(24).total_seconds() * 100
        )
        task_strs = [
            f"{task}: {time_fmt(days[day][task])}" for task in days[day]
        ]
        print(
            str(day.name.lower()),
            f"{percent_occupied}%",
            time_fmt(occupied),
            time_fmt(remaining),
            *task_strs,
            sep="\t",
        )


def print_tasks(tasks: TaskMap) -> None:
    print("DAY", "PER W", "PER Y", "DAYS", sep="\t")
    for task in tasks:
        per_week = sum(tasks[task].values(), hours(0))
        per_year = per_week * 52
        day_strs = [
            f"{day.name.lower()}: {time_fmt(tasks[task][day])}"
            for day in tasks[task]
        ]
        print(task, time_fmt(per_week), time_fmt(per_year), *day_strs, sep="\t")


UNAVOIDABLE = [
    every_day("faff", hours(1)),
    every_day("sleep", hours(9)),
    on_weekdays("work", hours(7.5)),
    on_weekdays("commute", hours(0.5) * 2),
    every_day("food", hours(0.25 + 1 + 1)),
]

SHOULD_AVOID = [every_day("tv", hours(0.5))]

PRODUCTIVE = [
    on_weekdays("proj", hours(1)),
    on_weekends("proj", hours(3)),
    every_day("reading", hours(0.5)),
]

WANT_TO_DO = [
    on_weekdays("gym", hours(0.5)),
    every_day("spanish", hours(0.5)),
    on_day(Day.SUN, "climb", hours(2 + 0.75 * 2)),
]

if __name__ == "__main__":
    main()
