import difflib
from typing import List, Optional
from pathlib import Path
from diff.file import collect_files, generate_output
from diff.diff_data import DiffData
from time import time
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor


def generate_htmls(
    base_files: dict,
    secondary_files: dict
) -> List[DiffData]:
    htmls = []
    # Generate pairings
    pairings = []
    for file_name in base_files:
        pairings.append((file_name, base_files[file_name], secondary_files[file_name]))
    # Map pairings
    print(len(pairings))
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for pairing in pairings:
            future = executor.submit(generate_html, pairing[0], pairing[1], pairing[2])
            futures.append(future)
        i = 0
        for future in futures:
            start_time = time()
            html = future.result()
            htmls.append(html)
            end_time = time()
            print(f"{html.file_name}: {end_time - start_time}")
            i += 1
    return htmls


def generate_html(
    file_name: str,
    base_file: List[str],
    secondary_file: List[str]
) -> DiffData:
        html = difflib.HtmlDiff().make_file(
            fromlines=base_file,
            tolines=secondary_file,
            context=True,
            numlines=10
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
    start_time = time()
    base_files, secondary_files = collect_files(
        base_path=base_path,
        secondary_path=secondary_path,
        exts=exts
    )
    end_time = time()
    elasped_time = end_time - start_time
    print(f"Collect files: {elasped_time}")
    # Compare same files against each other and generate HTML
    start_time = time()
    htmls = generate_htmls(base_files=base_files, secondary_files=secondary_files)
    end_time = time()
    elasped_time = end_time - start_time
    print(f"Generate htmls: {elasped_time}")
    # Check for and generate output directory
    """
    start_time = time()
    generate_output(output_dir, htmls)
    end_time = time()
    elasped_time = end_time - start_time
    print(f"Generate output: {elasped_time}")
    """
    return
