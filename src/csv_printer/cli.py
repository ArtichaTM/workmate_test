from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, kw_only=True, slots=True)
class RunInfo:
    files: tuple[Path, ...]
    columns: tuple[str, ...]


def _create_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "--files",
        nargs="+",
        type=Path,
        help="List of paths to files",
        required=True,
    )
    parser.add_argument(
        "--report",
        nargs="+",
        type=str,
        help="Additional columns",
        default=('name', 'coffee_spent', 'mean_coffee_spent')
    )
    return parser


def create_run_info() -> RunInfo:
    parser = _create_parser()
    ns = parser.parse_args()
    files = ns.files
    report = ns.report
    return RunInfo(
        files=tuple(files),
        columns=tuple(report)
    )
