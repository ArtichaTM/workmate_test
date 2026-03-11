from pathlib import Path

import pytest


@pytest.fixture
def one_student_path(tmp_path: Path):
    """Creates csv with one student"""
    csv_content = """
student,date,coffee_spent,sleep_hours,study_hours,mood,exam
Алексей Смирнов,2024-06-06,480,4.0,13,устал,Физика
    """.strip('\n\t ')
    csv_file = tmp_path / "grades.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    return csv_file
