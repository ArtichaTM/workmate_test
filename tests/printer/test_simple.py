import pytest

from csv_printer.printer import StudentsInfoPrinter


def assert_printer_laziness(one_student_students) -> None:
    printer = StudentsInfoPrinter(
        one_student_students,
        columns=('name', )
    )
    assert printer.sizes is None


def test_object_creation(one_student_students) -> None:
    printer = StudentsInfoPrinter(
        one_student_students,
        columns=('name', )
    )
    printer.print()


def test_different_columns(one_student_students) -> None:
    # 0 columns
    with pytest.raises(AssertionError):
        StudentsInfoPrinter(
            one_student_students,
            columns=()
        )

    # Only name
    StudentsInfoPrinter(
        one_student_students,
        columns=('name', )
    )
