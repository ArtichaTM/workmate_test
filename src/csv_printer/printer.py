from typing import Generator, Sequence
from datetime import date

from .reader import StudentExam


class StudentsInfoPrinter:
    __slots__ = (
        'students',
        'columns',
        'sizes',
    )
    students: dict[str, dict[str, list[StudentExam]]]
    sizes: dict[str, int] | None

    def __init__(
        self,
        students: dict[str, dict[str, list[StudentExam]]],
        columns: Sequence[str]
    ) -> None:
        assert all((isinstance(i, str) for i in columns))
        self.students = students
        self.columns = columns
        self.sizes = None

    def _column_names(self) -> Generator[str, None, None]:
        values = set()
        for sessions in self.students.values():
            for student_list in sessions.values():
                for student in student_list:
                    for field_name in student:
                        yield field_name
                    break
                break
            break

    def _init_sizes(self) -> None:
        if self.sizes:
            return
        result: dict[str, int] = {
            field: len(field) for field in self._column_names()
        }
        for sessions in self.students.values():
            for student_list in sessions.values():
                for student in student_list:
                    for field_name, field_value in student.items():
                        result[field_name] = max(
                            result[field_name],
                            len(str(field_value))
                        )
        self.sizes = {k: v+2 for k, v in result.items()}

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
            print(line*i, end=edge)
        print()

    def _print_data_line(
        self,
        data: Sequence[str] | StudentExam,
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

    def print(self) -> None:
        self._init_sizes()
        self._print_separator()
        columns = tuple(self._column_names())
        self._print_data_line(
            columns,
            alignments=('^', ) * len(columns)
        )
        self._print_separator(line='=')
        for inner_iterator in self.students.values():
            for inner_iterator in inner_iterator.values():
                for student in inner_iterator:
                    self._print_data_line(student)
                    self._print_separator()
