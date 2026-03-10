from logging import getLogger
from pathlib import Path

from .cli import RunInfo, create_run_info
from .reader import read_csv, StudentsInfo
from .printer import StudentsInfoPrinter

logger = getLogger()


def _read_csv(path: Path) -> StudentsInfo | None:
    pass


def cli_main() -> None:
    return main(create_run_info())


def main(
    run_info: RunInfo
) -> None:
    assert isinstance(run_info, RunInfo)
    students = StudentsInfo()
    for path in run_info.files:
        if not path.exists():
            logger.warning(f"Файл {path} не существует")
        if path.is_dir():
            logger.warning(f"Путь {path} указывает на папку")
        new_students = read_csv(path)
        students += new_students
    printer = StudentsInfoPrinter(students)
    printer.print()
