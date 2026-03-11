from pathlib import Path

import pytest

from csv_printer.reader import StudentExam, read_csv


@pytest.fixture
def one_student_students(
    one_student_path: Path
) -> dict[str, dict[str, list[StudentExam]]]:
    return read_csv(one_student_path)
