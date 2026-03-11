import logging
from pathlib import Path

import pytest

from csv_printer.cli import create_run_info
from csv_printer.main import cli_main, main


def test_required_files():
    with pytest.raises(SystemExit):
        create_run_info([])
    with pytest.raises(SystemExit):
        cli_main([])


@pytest.mark.parametrize(
    "value,expected",
    [
        ("temp.csv", Path("temp.csv")),
        ("./temp.csv", Path("temp.csv")),
        ("temp/file.csv", Path("temp/file.csv")),
        ("temp\\file.csv", Path("temp/file.csv")),
    ]
)
def test_different_paths(value: str, expected: Path):
    assert isinstance(value, str)
    assert isinstance(expected, Path)
    info = create_run_info([
        "--files", value
    ])
    assert len(info.files) == 1
    assert info.files[0] == expected


def test_main(one_student_2exams_path):
    main(create_run_info([
        "--files", str(one_student_2exams_path),
    ]))


def test_main_warnings(caplog, one_student_2exams_path):
    caplog.clear()
    caplog.set_level(logging.WARNING)

    file_name = "non-existent.csv"
    main(create_run_info([
        '--files', file_name
    ]))

    assert len(caplog.records) == 2
    assert any(
        file_name in rec.getMessage() for rec in caplog.records
    ), "Missing-file warning not emitted"
    assert any(
        rec.levelno >= logging.ERROR for rec in caplog.records
    ), "No error on exit <+ no files"

    caplog.clear()
    path = one_student_2exams_path.parent
    main(create_run_info([
        '--files', str(path)
    ]))

    assert len(caplog.records) == 2
    assert any(
        path.name in rec.getMessage() for rec in caplog.records
    ), "Dir instead of folder warning not emitted"
    assert any(
        rec.levelno >= logging.ERROR for rec in caplog.records
    ), "No error on exit <+ no files"
