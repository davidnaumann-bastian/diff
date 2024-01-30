from dataclasses import dataclass


@dataclass
class DiffData:
    file_name: str
    link: str
    percent_match: int = 0
    html: str = ""
