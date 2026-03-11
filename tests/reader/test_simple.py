import logging
from datetime import date
from pathlib import Path

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


def test_read_csv_duplicate(
    one_student_duplicate_path: Path,
    caplog
) -> None:
    caplog.set_level(logging.WARNING)

    result = read_csv(one_student_duplicate_path)

    # Data same
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

    # Warning raised
    assert [
        rec for rec in caplog.records
        if rec.levelno == logging.WARNING
    ], "Awaited warning of duplicate"
