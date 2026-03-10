import csv
from datetime import datetime, date
from dataclasses import dataclass, fields, astuple
from pathlib import Path


@dataclass(kw_only=True)
class StudentInfo:
    name: str
    date: date
    coffee_spent: int
    sleep_hours: float
    study_hours: int
    mood: str
    exam: str


@dataclass(kw_only=True)
class StudentsInfo:
    headers: list[str] | None
    students: list[StudentInfo]


def parse_row(row) -> StudentInfo:
    return StudentInfo(
        name=row["student"],
        date=datetime.strptime(row["date"], "%Y-%m-%d").date(),
        coffee_spent=int(row["coffee_spent"]),
        sleep_hours=float(row["sleep_hours"]),
        study_hours=int(row["study_hours"]),
        mood=row["mood"],
        exam=row["exam"],
    )


def read_csv(path: Path) -> StudentsInfo:
    assert isinstance(path, Path)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        rows = [parse_row(r) for r in reader]
    return StudentsInfo(
        headers=list(header) if header else None,
        students=rows
    )
