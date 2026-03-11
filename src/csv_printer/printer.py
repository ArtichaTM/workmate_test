from datetime import date
from logging import getLogger
from typing import Callable, Generator, Sequence

from .aggregations import OPERATIONS
from .reader import StudentExam

logger = getLogger()


class StudentsInfoPrinter:
    __slots__ = (
        'students',
        'simple_columns',
        'columns',
        'sizes',
        'global_students'
    )
    students: dict[str, dict[str, list[StudentExam]]]
    simple_columns: set[str]
    global_students: dict[str, dict[str, int | float | date | None]]
    sizes: dict[str, int] | None

    def __init__(
        self,
        students: dict[str, dict[str, list[StudentExam]]],
        columns: Sequence[str]
    ) -> None:
        assert columns
        assert all((isinstance(i, str) for i in columns))
        self.students = students
        self.global_students = {name: dict() for name in self.students}
        self.columns = tuple(columns)
        # Getting fields of first name of first exam of StudentExam
        self.simple_columns = {
            name for name in next(iter(
                next(iter(
                    students.values()
                )).values()
            ))[0]
        }
        self.sizes = None

    def _get_global_field_names(self) -> Generator[str, None, None]:
        for fields in self.global_students.values():
            for name in fields:
                yield name

    def _init_sizes(self) -> None:
        if self.sizes:
            return
        result: dict[str, int] = {
            name: len(name) for name in self._get_global_field_names()
        }
        result['name'] = 0
        for name, values in self.global_students.items():
            assert isinstance(name, str)
            result['name'] = max(
                result['name'],
                len(name)
            )
            for value_name, value in values.items():
                result[value_name] = max(
                    result[value_name],
                    len(str(value))
                )
        self.sizes = {k: v + 2 for k, v in result.items()}

    def _print_separator(
        self,
        edge: str = '+',
        line: str = '-'
    ):
        assert self.sizes is not None
        assert isinstance(edge, str)
        assert len(edge) == 1
        assert isinstance(line, str)
        assert len(line) == 1
        print(edge, end='')
        for i in self.sizes.values():
            print(line * i, end=edge)
        print()

    def _print_data_line(
        self,
        data: Sequence,
        alignments: Sequence[str] | None = None,
        separator: str = '|',
    ) -> None:
        assert self.sizes is not None
        assert isinstance(separator, str)
        assert len(separator) == 1
        assert isinstance(data, (list, tuple, dict)), type(data)
        print(separator, end='')
        if alignments is None:
            alignments = ('>', ) * len(data)
        assert len(self.sizes) == len(alignments) == len(data), (
            f"{len(self.sizes)}=={len(alignments)}=={len(data)}"
        )
        for length, align, line in zip(
            self.sizes.values(), alignments, data,
            strict=True
        ):
            if isinstance(line, date):
                string = line.strftime('%Y-%m-%d')
            else:
                string = str(line)
            string = string[:length]
            length -= 2
            print(
                f" {string:{align}{length}} ",
                end=separator
            )
        print()

    def _calculate_column(
        self,
        /,
        base_column: str,
        column: str,
        operation: Callable
    ) -> None:
        for name, sessions in self.students.items():
            global_student = self.global_students[name]
            for exams in sessions.values():
                if base_column not in exams[0]:
                    continue
                values = [i[base_column] for i in exams]
                assert column not in global_student
                global_student[column] = operation(values)
                break
            else:
                logger.error(
                    f"Колонка {column} основывается на колонке "
                    f"{base_column}, однако она не существует"
                )
                for name in self.students:
                    global_student = self.global_students[name]
                    global_student[column] = None
                return

    def _validate_columns(self) -> None:
        operations = tuple(f"{i}_" for i in OPERATIONS)
        for name in self.students:
            self.global_students[name] = dict()
        for column in self.columns:
            # Column needs calculation
            if column.startswith(operations):
                for operation_name, operation_func in OPERATIONS.items():
                    if not column.startswith(operation_name):
                        continue
                    self._calculate_column(
                        base_column=column[len(operation_name) + 1:],
                        column=column,
                        operation=operation_func
                    )
            # Simple column?
            if column in self.simple_columns:
                logger.warning(
                    f"Колонка {column} является простой, пропускается"
                )

    def print(self) -> None:
        self._validate_columns()
        self._init_sizes()
        self._print_separator()
        self._print_data_line(
            self.columns,
            alignments=('^', ) * len(self.columns)
        )
        self._print_separator(line='=')
        for name, values in self.global_students.items():
            self._print_data_line([name, *values.values()])
            self._print_separator()
