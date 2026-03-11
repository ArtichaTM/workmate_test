from csv_printer.aggregations import OPERATIONS
from csv_printer.printer import StudentsInfoPrinter


def test_different_operations(one_student_students) -> None:
    """Tests all possible operations"""
    for operation in OPERATIONS:
        column_name = f'{operation}_coffee_spent'
        printer = StudentsInfoPrinter(
            one_student_students,
            columns=('name', column_name)
        )
        assert column_name not in printer._get_global_field_names(
        ), tuple(
            printer._get_global_field_names()
        )
        assert column_name in printer.columns

        assert printer._validate_columns() is None
        assert column_name in printer._get_global_field_names(
        ), tuple(
            printer._get_global_field_names()
        )
