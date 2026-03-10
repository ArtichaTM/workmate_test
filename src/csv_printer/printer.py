from typing import Sequence
from datetime import date
from dataclasses import fields, astuple

from .reader import (
    StudentInfo,
    StudentExamsInfo,
    StudentsInfo
)


class StudentsInfoPrinter:
    __slots__ = (
        'students',
        'sizes',
        'alignments',
    )
    students: StudentsInfo
    sizes: dict[str, int] | None
    alignments: list[str]

    def __init__(
        self,
        students: StudentsInfo
    ) -> None:
        self.students = students
        self.sizes = None
        self.alignments = [
            '>'
        ] * len(students.students)
    
    def _init_sizes(self) -> None:
        if self.sizes:
            return
        student_fields = fields(StudentInfo)
        result: dict[str, int] = {
            field.name: len(field.name) for field in student_fields
        }
        for student_session in self.students.students.values():
            for student in student_session.exams.values():
                for field in student_fields:
                    name = field.name
                    result[name] = max(result[name], len(str(getattr(
                        student, name
                    ))))
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
        data: Sequence[str] | StudentsInfo,
        alignments: Sequence[str] | None = None,
        separator: str = '|',
    ) -> None:
        assert self.sizes is not None
        assert isinstance(separator, str)
        assert len(separator) == 1
        assert isinstance(data, (list, tuple)), type(data)
        print(separator, end='')
        if alignments is None:
            alignments = self.alignments
        for length, align, line in zip(
            self.sizes.values(), alignments, data
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

    def print(
        self,
        columns: tuple[str, ...] | None = None
    ) -> None:
        if columns is None:
            columns = tuple(StudentsInfo.columns)
        assert isinstance(columns, tuple)
        assert all((isinstance(i, str) for i in columns))
        self._init_sizes()
        self._print_separator()
        if self.students.columns is not None:
            self._print_data_line(
                self.students.columns,
                alignments=('^', ) * len(self.students.columns)
            )
            self._print_separator(line='=')
        for line in self.students.students.values():
            self._print_data_line(line.get_row())
            self._print_separator()
