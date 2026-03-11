from datetime import date

import pytest

from csv_printer.aggregations import OPERATIONS
from csv_printer.printer import StudentsInfoPrinter


def test_all_operations(one_student_students) -> None:
    """Tests all possible operations"""
    for operation in OPERATIONS:
        column_name = f'{operation}_coffee_spent'
        printer = StudentsInfoPrinter(
            one_student_students,
            columns=('name', column_name)
        )

        # Before new columns created
        assert 'name' in printer.columns
        assert 'name' not in printer._get_global_field_names()
        assert column_name not in printer._get_global_field_names(
        ), tuple(
            printer._get_global_field_names()
        )
        assert column_name in printer.columns

        assert printer._validate_columns() is None

        # After new columns is created
        assert 'name' in printer.columns
        assert 'name' not in printer._get_global_field_names()
        assert column_name in printer._get_global_field_names(
        ), tuple(
            printer._get_global_field_names()
        )
        assert column_name in printer.columns


@pytest.mark.parametrize(
    "func_name,expected",
    [
        ("median", 505),
        ("mean", 505),
        ("average", 505),
        ("min", 480),
        ("max", 530),
    ]
)
def test_operations_coffee_spent(
    one_student_2exams_students,
    func_name: str,
    expected
) -> None:
    column = f'{func_name}_coffee_spent'
    printer = StudentsInfoPrinter(
        one_student_2exams_students,
        columns=('name', column)
    )
    assert 'Алексей Смирнов' in printer.global_students
    assert column not in printer.global_students['Алексей Смирнов']
    assert printer._validate_columns() is None
    assert column in printer.global_students['Алексей Смирнов']
    result = printer.global_students['Алексей Смирнов'][column]
    assert result == expected, f"{result}=={expected}"
    assert isinstance(result, type(expected)), (
        f"{type(result)} != {type(expected)}"
    )


@pytest.mark.parametrize(
    "func_name,expected",
    [
        ("median", date(year=2024, month=6, day=7)),
        ("mean", date(year=2024, month=6, day=7)),
        ("average", date(year=2024, month=6, day=7)),
        ("min", date(year=2024, month=6, day=6)),
        ("max", date(year=2024, month=6, day=7)),
    ]
)
def test_operations_date(
    one_student_2exams_students,
    func_name: str,
    expected
) -> None:
    column = f'{func_name}_date'
    printer = StudentsInfoPrinter(
        one_student_2exams_students,
        columns=('name', column)
    )
    assert 'Алексей Смирнов' in printer.global_students
    assert column not in printer.global_students['Алексей Смирнов']
    assert printer._validate_columns() is None
    assert column in printer.global_students['Алексей Смирнов']
    result = printer.global_students['Алексей Смирнов'][column]
    assert result == expected, f"{result}=={expected}"
    assert isinstance(result, type(expected)), (
        f"{type(result)} != {type(expected)}"
    )


def test_double_operation(
    one_student_2exams_students,
):
    values: dict[str, float | int] = {
        'median_coffee_spent': 505,
        'max_coffee_spent': 530,
        'average_sleep_hours': (4.0 + 3.5) / 2,
        'min_sleep_hours': 3.5,
        'max_sleep_hours': 4,
    }
    printer = StudentsInfoPrinter(
        one_student_2exams_students,
        columns=('name', *values)
    )
    assert 'Алексей Смирнов' in printer.global_students
    assert printer._validate_columns() is None
    student = printer.global_students['Алексей Смирнов']
    assert set(values) == set(student), "Different keys"
    for name, real_value in student.items():
        assert real_value == values[name]
