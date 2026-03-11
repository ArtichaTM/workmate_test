from pathlib import Path

import pytest


def write_csv(
    path: Path,
    content: str
) -> Path:
    assert isinstance(content, str)
    assert isinstance(path, Path)
    assert path.exists()
    assert path.is_file()
    content = content.strip('\n\t ')
    csv_file = path / "grades.csv"
    csv_file.write_text(content, encoding="utf-8")
    return csv_file


@pytest.fixture
def one_student_path(tmp_path: Path) -> Path:
    """Creates csv with one student"""
    return write_csv(tmp_path, """
student,date,coffee_spent,sleep_hours,study_hours,mood,exam
Алексей Смирнов,2024-06-06,480,4.0,13,устал,Физика
""")


@pytest.fixture
def one_student_duplicate_path(tmp_path: Path) -> Path:
    """Creates csv with one student"""
    return write_csv(tmp_path, """
student,date,coffee_spent,sleep_hours,study_hours,mood,exam
Алексей Смирнов,2024-06-06,480,4.0,13,устал,Физика
Алексей Смирнов,2024-06-06,480,4.0,13,устал,Физика
""")


@pytest.fixture
def one_student_2exams_path(tmp_path: Path) -> Path:
    """Creates csv with one student"""
    return write_csv(tmp_path, """
student,date,coffee_spent,sleep_hours,study_hours,mood,exam
Алексей Смирнов,2024-06-06,480,4.0,13,устал,Физика
Алексей Смирнов,2024-06-07,530,3.5,15,зомби,Физика
""")
