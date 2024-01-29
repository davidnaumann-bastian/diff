import difflib
from typing import List, Optional
from pathlib import Path
from dir_diff_tool.file import collect_files, generate_output
from dir_diff_tool.diff_data import DiffData


def generate_htmls(
    base_files: dict,
    secondary_files: dict
) -> List[DiffData]:
    htmls = []
    for key in base_files:
        diff_data = DiffData
        base_file = base_files[key]
        secondary_file = secondary_files[key]
        html = difflib.HtmlDiff().make_file(
            fromlines=base_file,
            tolines=secondary_file
        )
        diff_data = DiffData(
            file_name=key+".html",
            html=html
        )
        htmls.append(diff_data)
    return htmls


def get_lines_from_file(
    file_path: Path
) -> List[str]:
    if file_path.exists():
        with open(file_path, 'r') as f:
            lines = f.readlines()
    else:
        lines = []
    return lines

def generate_diff(
    base_path: Path,
    secondary_path: Path,
    exts: Optional[List[str]] = [],
    output_dir: Optional[Path] = Path('htmldiff')
):
    # Collect all files
    base_files, secondary_files = collect_files(
        base_path=base_path,
        secondary_path=secondary_path,
        exts=exts
    )
    # Compare same files against each other and generate HTML
    htmls = generate_htmls(base_files=base_files, secondary_files=secondary_files)
    # Check for and generate output directory
    generate_output(output_dir, htmls)
    pass
