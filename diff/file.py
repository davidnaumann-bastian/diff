from pathlib import Path
from typing import Tuple, List
from diff.diff_data import DiffData

def collect_files(
    base_path: Path,
    secondary_path: Path,
    exts: List[str]
) -> Tuple[dict, dict]:
    base_files = collect_files_from_path(base_path, exts=exts)
    secondary_files = collect_files_from_path(secondary_path, exts=exts)
    keys = set(base_files.keys()).union(set(secondary_files.keys()))
    for key in keys:
        if key not in base_files:
            base_files[key] = []
        if key not in secondary_files:
            secondary_files[key] = []
    return base_files, secondary_files


def collect_files_from_path(path: Path, exts: List[str]):
    file_paths = [
        file_path for file_path in path.iterdir() if file_path.is_file() and any(ext in file_path.name for ext in exts)
    ]
    files = {file_path.name: _read_file(file_path) for file_path in file_paths}
    return files

def _read_file(file_path: Path):
    lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return lines

def generate_output(
    output_path: Path,
    htmls: List[DiffData]
):
    output_path.mkdir(parents=True, exist_ok=True)
    with open(output_path.joinpath('.gitignore'), 'w') as gitignore:
        gitignore.write("*\n")
    for diff_data in htmls:
        with open(output_path.joinpath(diff_data.file_name), "w") as f:
            f.write(diff_data.html)
    return
