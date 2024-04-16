from pathlib import Path
from typing import List, Dict
from .file import File
import os
from jinja2 import Environment, PackageLoader
import shutil
from multiprocessing import Pool
from functools import partial
import difflib
from dataclasses import dataclass, field

STATIC_FILES = [
    "bootstrap.min.css",
    "bootstrap.min.js",
    "sortable.min.css",
    "sortable.min.js",
    "diff.css",
]

env = Environment(loader=PackageLoader("diff"))


@dataclass
class Files:
    """Class for maintaining structure for generating HMTL"""

    base: File = field(default_factory=File)
    secondary: File = field(default_factory=File)


@dataclass
class HTML:
    file_name: str
    link: str
    content: str
    percent_match: int


def generate_output(
    output_path: Path, base_files: List[File], secondary_files: List[File]
):
    files = _create_file_structure(
        base_files=base_files, secondary_files=secondary_files
    )
    # Ensure creation and cleaning of output folder
    _ensure_output_folder(output_path=output_path)
    # Generate static files
    _generate_static_files(output_path=output_path)
    # Generate index.html
    htmls: List[HTML] = _generate_htmls(files=files)
    _generate_index(output_path=output_path, htmls=htmls)
    # Generate difference pages
    # TODO: at some point want to migrate this
    # to custom templated .html files
    _generate_diff_pages(output_path=output_path, htmls=htmls)
    return


def _create_file_structure(
    base_files: List[File], secondary_files: List[File]
) -> Dict[str, Files]:
    files: Dict[str, Files] = {}
    for file in base_files:
        file_name = file.file_path.name
        if file_name in files:
            files[file_name].base = file
        else:
            files[file_name] = Files()
            files[file_name].base = file
    for file in secondary_files:
        file_name = file.file_path.name
        if file_name in files:
            files[file_name].secondary = file
        else:
            files[file_name] = Files()
            files[file_name].secondary = file
    return files


def _ensure_output_folder(
    output_path: Path,
):
    output_path.mkdir(parents=True, exist_ok=True)
    file_paths = [
        file_path for file_path in output_path.iterdir() if file_path.is_file()
    ]
    for file_path in file_paths:
        os.remove(file_path)


def _generate_static_files(output_path: Path):
    for static_file in STATIC_FILES:
        static_dir = os.path.join(os.path.dirname(__file__), "templates")
        static_path = os.path.join(static_dir, static_file)
        shutil.copyfile(static_path, os.path.join(output_path, static_file))
    with open(output_path.joinpath(".gitignore"), "w") as gitignore:
        gitignore.write("*\n")


def _generate_index(output_path: Path, htmls: List[HTML]):
    template = env.get_template("index.html")
    content = template.render(htmls=htmls)
    with open(output_path.joinpath("index.html"), "w") as index_file:
        index_file.write(content)
    return


def _generate_htmls(files: Dict[str, Files]) -> List[HTML]:
    htmls = []
    # Generate pairings
    pairings = [
        (file_name, files[file_name].base, files[file_name].secondary)
        for file_name in files
    ]
    # Map pairings
    with Pool(processes=5) as pool:
        map_result = pool.starmap_async(_generate_html, pairings)
        for result in map_result.get():
            htmls.append(result)
    return htmls


def _generate_html(file_name: str, base_file: File, secondary_file: File) -> HTML:
    table = difflib.HtmlDiff().make_table(
        fromlines=base_file.lines,
        tolines=secondary_file.lines,
        fromdesc=base_file.file_path,
        todesc=secondary_file.file_path,
    )
    ratio = difflib.SequenceMatcher(
        a=base_file.lines, b=secondary_file.lines
    ).quick_ratio()
    percent_match = ratio * 100
    template = env.get_template("diff.html")
    content = template.render(
        file_name=file_name, percent_match=percent_match, table=table
    )
    link = "diff_" + file_name + ".html"
    html = HTML(
        file_name=file_name, link=link, content=content, percent_match=percent_match
    )
    return html


def _generate_diff_pages(output_path: Path, htmls: List[HTML]):
    partial_gen_diff_page = partial(_generate_diff_page, output_path=output_path)
    with Pool(processes=5) as pool:
        map_result = pool.map_async(partial_gen_diff_page, htmls)
        for _ in map_result.get():
            pass
    return


def _generate_diff_page(html: HTML, output_path: Path):
    with open(output_path.joinpath(html.link), "w") as f:
        f.write(html.content)
