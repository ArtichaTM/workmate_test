from pathlib import Path
from datetime import datetime, date

import pytest

from .fixtures import one_student_path
from csv_printer.reader import read_csv


def test_read_csv_single_file(one_student_path: Path) -> None:
    result = read_csv(one_student_path)
    expected = {
        'Алексей Смирнов': {
            'Физика': [
                {
                    'coffee_spent': 480,
                    'date': date(2024, 6, 6),
                    'exam': 'Физика',
                    'mood': 'устал',
                    'name': 'Алексей Смирнов',
                    'sleep_hours': 4.0,
                    'study_hours': 13,
                },
            ],
        },
    }

    assert expected == result
