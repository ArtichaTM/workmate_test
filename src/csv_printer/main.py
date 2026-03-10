from logging import getLogger
from pathlib import Path

from .cli import RunInfo, create_run_info
from .reader import read_csv
from .printer import StudentsInfoPrinter

logger = getLogger()


def cli_main() -> None:
    return main(create_run_info())


def main(
    run_info: RunInfo
) -> None:
    assert isinstance(run_info, RunInfo)
    new_paths = []
    for path in run_info.files:
        if not path.exists():
            logger.warning(f"Файл {path} не существует")
        elif path.is_dir():
            logger.warning(f"Путь {path} указывает на папку")
        else:
            new_paths.append(path)
    if not new_paths:
        print("Нет валидных файлов. Выход")
        return
    students = read_csv(*new_paths)
    printer = StudentsInfoPrinter(students, run_info.columns)
    printer.print()
