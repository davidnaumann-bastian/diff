from pathlib import Path
from typing import List
from diff.diff_data import DiffData
import os
from jinja2 import Environment, PackageLoader
import shutil
from multiprocessing import Pool
from functools import partial
import difflib

STATIC_FILES = [
    "bootstrap.min.css",
    "bootstrap.min.js",
    "sortable.min.css",
    "sortable.min.js"
]

env = Environment(
    loader=PackageLoader("diff")
)

def generate_output(
    output_path: Path,
    base_files: dict,
    secondary_files: dict
):
    # Ensure creation and cleaning of output folder
    _ensure_output_folder(output_path=output_path)
    # Generate static files
    _generate_static_files(output_path=output_path)
    # Generate index.html
    htmls = _generate_htmls(
        base_files=base_files,
        secondary_files=secondary_files
    )
    _generate_index(
        output_path=output_path,
        htmls=htmls
    )
    # Generate difference pages
    # TODO: at some point want to migrate this
    # to custom templated .html files
    _generate_diff_pages(
        output_path=output_path,
        htmls=htmls
    )
    return

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

def _generate_htmls(
    base_files: dict,
    secondary_files: dict
) -> List[DiffData]:
    htmls = []
    # Generate pairings
    pairings = []
    for file_name in base_files:
        pairings.append((file_name, base_files[file_name], secondary_files[file_name]))
    # Map pairings
    with Pool(processes=5) as pool:
        map_result = pool.starmap_async(_generate_html, pairings)
        for result in map_result.get():
            htmls.append(result)
    return htmls


def _generate_html(
    file_name: str,
    base_file: List[str],
    secondary_file: List[str]
) -> DiffData:
        html = difflib.HtmlDiff().make_file(
            fromlines=base_file,
            tolines=secondary_file
        )
        ratio = difflib.SequenceMatcher(
            a=base_file,
            b=secondary_file
        ).quick_ratio()
        diff_data = DiffData(
            file_name=file_name,
            link=file_name+".html",
            percent_match=ratio*100,
            html=html
        )
        return diff_data

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
