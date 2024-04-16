from pathlib import Path
from typing import List, Tuple
from multiprocessing import Pool
import re
from dataclasses import dataclass, field


@dataclass
class File:
    file_path: Path = field(default_factory=Path)
    lines: List[str] = field(default_factory=list)


def collect_files(
    base_path: Path, secondary_path: Path, regex: str
) -> Tuple[List[File], List[File]]:
    base_files: List[File] = _collect_files_from_path(base_path, regex=regex)
    secondary_files: List[File] = _collect_files_from_path(secondary_path, regex=regex)
    return base_files, secondary_files


def _collect_files_from_path(path: Path, regex: str) -> List[File]:
    file_paths = [file_path for file_path in path.iterdir() if file_path.is_file()]
    file_paths = _filter_file_path_by_regex(file_paths=file_paths, regex=regex)
    files = []
    with Pool(processes=5) as pool:
        map_result = pool.map_async(_read_file, file_paths)
        for file in map_result.get():
            files.append(file)
    return files


def _filter_file_path_by_regex(file_paths: List[Path], regex: str):
    pattern = re.compile(regex)
    return [file_path for file_path in file_paths if pattern.search(file_path.name)]


def _read_file(file_path: Path) -> File:
    lines = []
    with open(file_path, "r") as f:
        lines = f.readlines()
    return File(file_path=file_path, lines=lines)
