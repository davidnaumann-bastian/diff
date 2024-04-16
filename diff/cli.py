import argparse
from pathlib import Path
from .diff import generate_diff


class DiffScript:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser(
            description="Display a diff between two directories in HTML."
        )
        parser.add_argument(
            "-d1",
            "--directory1",
            required=True,
            type=str,
            help="The path to the base directory to compare the second directory to.",
        )
        parser.add_argument(
            "-d2",
            "--directory2",
            required=True,
            type=str,
            help="The path to the second directory to compare the base directory to.",
        )
        parser.add_argument("-r", "--regex", required=False, type=str, default=".*")
        parser.add_argument(
            "-o",
            "--output",
            required=False,
            type=str,
            default="htmldiff",
            help="The path/name to the output file where the diff will be stored.",
        )
        parser.parse_args(namespace=self)

    def run(self):
        base_path = Path(self.directory1)
        secondary_path = Path(self.directory2)
        regex = self.regex
        assert base_path.exists(), f"{base_path} doesn't exist or could not be found."
        assert (
            secondary_path.exists()
        ), f"{secondary_path} doesn't exist or could not be found."
        assert base_path.is_dir(), f"{base_path} is not a directory."
        assert secondary_path.is_dir(), f"{secondary_path} is not a directory."
        generate_diff(base_path=base_path, secondary_path=secondary_path, regex=regex)


def main():
    DiffScript().run()


if __name__ == "__main__":
    main()
