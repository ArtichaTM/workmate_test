import csv
from datetime import datetime, date
from dataclasses import dataclass, field
from pathlib import Path
from logging import getLogger

logger = getLogger()


@dataclass(kw_only=True, slots=True)
class StudentInfo:
    name: str
    date: date
    coffee_spent: int
    sleep_hours: float
    study_hours: int
    mood: str
    exam: str


@dataclass(kw_only=True, slots=True)
class StudentExamsInfo:
    exams: dict[str, StudentInfo] = field(
        default_factory=lambda: dict()
    )

    def __iadd__(
        self,
        other: 'StudentInfo | StudentExamsInfo'
    ) -> 'StudentExamsInfo':
        assert isinstance(other, (
            StudentInfo,
            StudentExamsInfo,
        ))
        if isinstance(other, StudentInfo):
            other_exams = {other.exam: other}
        else:
            other_exams = other.exams
        for (
            other_exam,
            other_student_session
        ) in other_exams.items():
            if other_exam in self.exams:
                logger.warning(
                    f"Экзамен {other_exam} "
                    "уже существует для студента "
                    f"{other_student_session.name}"
                )
            self.exams[other_exam] = other_student_session
        return self

    def _first_student(self) -> StudentInfo:
        return next(iter(self.exams.values()))

    def _get_column(self, column_name: str):
        first = self._first_student()
        # TODO: add `median_*`, `max_*` and other
        return getattr(first, column_name)

    def get_row(
        self,
        columns: tuple[str, ...] | None = None
    ) -> tuple[str, ...]:
        if columns is None:
            columns = StudentsInfo.columns
        first_student = next(iter(self.exams.values()))
        return tuple(getattr(first_student, i) for i in columns)


@dataclass(kw_only=True, slots=True)
class StudentsInfo:
    columns = (
        'name', 'date',
        'coffee_spent',
        'sleep_hours', 'study_hours',
        'mood', 'exam'
    )
    students: dict[str, StudentExamsInfo] = field(
        default_factory=lambda: dict()
    )

    def __add__(self, other_students: 'StudentsInfo'):
        assert isinstance(other_students, StudentsInfo)
        new_students = type(self)()
        new_students += self
        new_students += other_students
        return new_students

    def __iadd__(self, other_students: 'StudentsInfo'):
        assert isinstance(other_students, StudentsInfo)
        for name, other_student in other_students.students.items():
            assert isinstance(name, str)
            assert isinstance(other_student, StudentExamsInfo)
            if name not in self.students:
                self.students[name] = StudentExamsInfo()
            self.students[name] += other_student
        return self


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
        rows = dict()
        for row in reader:
            student = parse_row(row)
            rows[student.name] = StudentExamsInfo(exams={
                student.exam: student
            })
    assert isinstance(rows, dict)
    assert all((isinstance(i, str) for i in rows))
    assert all((isinstance(i, StudentExamsInfo) for i in rows.values()))
    return StudentsInfo(
        students=rows
    )
