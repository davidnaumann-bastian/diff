from pathlib import Path
from typing import Tuple, List
from diff.diff_data import DiffData
import os
from jinja2 import Environment, PackageLoader
import shutil
from multiprocessing import Pool
from time import time
from functools import partial
import re

STATIC_FILES = [
    "bootstrap.min.css",
    "bootstrap.min.js",
    "sortable.min.css",
    "sortable.min.js"
]

env = Environment(
    loader=PackageLoader("diff")
)

def collect_files(
    base_path: Path,
    secondary_path: Path,
    regex: str
) -> Tuple[dict, dict]:
    base_files = collect_files_from_path(base_path, regex=regex)
    secondary_files = collect_files_from_path(secondary_path, regex=regex)
    keys = set(base_files.keys()).union(set(secondary_files.keys()))
    for key in keys:
        if key not in base_files:
            base_files[key] = []
        if key not in secondary_files:
            secondary_files[key] = []
    return base_files, secondary_files


def collect_files_from_path(path: Path, regex: str):
    pattern = re.compile(regex)
    file_paths = [
        file_path for file_path in path.iterdir() if file_path.is_file() and pattern.search(file_path.name)
    ]
    files = {}
    with Pool(processes=5) as pool:
        map_result = pool.map_async(_read_file, file_paths)
        for result in map_result.get():
            files[result[0].name] = result[1]
    return files

def _read_file(file_path: Path):
    lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return (file_path, lines)

def _ensure_output_folder(
    output_path: Path,
):
    output_path.mkdir(parents=True, exist_ok=True)
    file_paths = [file_path for file_path in output_path.iterdir() if file_path.is_file()]
    for file_path in file_paths:
        os.remove(file_path)

def _generate_static_files(
    output_path: Path
):
    for static_file in STATIC_FILES:
        static_dir = os.path.join(os.path.dirname(__file__), "templates")
        static_path = os.path.join(static_dir, static_file)
        shutil.copyfile(static_path, os.path.join(output_path, static_file))
    with open(output_path.joinpath('.gitignore'), 'w') as gitignore:
        gitignore.write("*\n")

def _generate_index(
    output_path: Path,
    htmls: List[DiffData]
):
    template = env.get_template("index.html")
    content = template.render(
        htmls=htmls
    )
    with open(output_path.joinpath("index.html"), 'w') as index_file:
        index_file.write(content)
    return

def _generate_diff_pages(
    output_path: Path,
    htmls: List[DiffData]
):
    partial_gen_diff_page = partial(_generate_diff_page, output_path=output_path)
    with Pool(processes=5) as pool:
        map_result = pool.map_async(partial_gen_diff_page, htmls)
        for _ in map_result.get():
            pass
    return

def _generate_diff_page(
    diff_data: DiffData,
    output_path: Path
):
    with open(output_path.joinpath(diff_data.link), "w") as f:
        f.write(diff_data.html)

def generate_output(
    output_path: Path,
    htmls: List[DiffData]
):
    _ensure_output_folder(output_path=output_path)
    _generate_static_files(output_path=output_path)
    _generate_index(
        output_path=output_path,
        htmls=htmls
    )
    _generate_diff_pages(
        output_path=output_path,
        htmls=htmls
    )
    return
