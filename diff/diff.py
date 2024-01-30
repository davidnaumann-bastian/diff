from typing import Optional
from pathlib import Path
from diff.file import collect_files
from diff.output import generate_output

def generate_diff(
    base_path: Path,
    secondary_path: Path,
    regex: Optional[str] = '.*',
    output_path: Optional[Path] = Path('htmldiff')
):
    # Collect all files
    base_files, secondary_files = collect_files(
        base_path=base_path,
        secondary_path=secondary_path,
        regex=regex
    )
    # Compare same files against each other and generate HTML
    # Check for and generate output directory
    generate_output(
        output_path=output_path,
        base_files=base_files,
        secondary_files=secondary_files
    )
    return
