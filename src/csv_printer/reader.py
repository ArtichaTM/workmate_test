import csv
from datetime import date as _date
from datetime import datetime
from logging import getLogger
from pathlib import Path
from typing import TypedDict

logger = getLogger()


class StudentExam(TypedDict):
    name: str
    date: _date
    coffee_spent: int
    sleep_hours: float
    study_hours: int
    mood: str
    exam: str


def parse_row(row) -> StudentExam:
    return {
        'name': row["student"],
        'date': datetime.strptime(row["date"], "%Y-%m-%d").date(),
        'coffee_spent': int(row["coffee_spent"]),
        'sleep_hours': float(row["sleep_hours"]),
        'study_hours': int(row["study_hours"]),
        'mood': row["mood"],
        'exam': row["exam"],
    }


def read_csv(*paths: Path) -> dict[str, dict[str, list[StudentExam]]]:
    output: dict[str, dict[str, list[StudentExam]]] = dict()
    seen: set[tuple] = set()
    for path in paths:
        assert isinstance(path, Path)
        with open(path, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                student = parse_row(row)
                values = tuple(student.values())
                if values in seen:
                    logger.warning(
                        f"Студент {student['name']} от "
                        f"{student['date']} повторяется"
                    )
                    continue
                seen.add(values)
                name = student['name']
                exam = student['exam']
                if name not in output:
                    output[name] = dict()
                if exam not in output[name]:
                    output[name][exam] = []
                output[name][exam].append(student)
    return output
