import csv
import dataclasses
import hashlib
import html
import pathlib
from typing import Iterator, List

import bs4

SRC_DIR = pathlib.Path("symfony-docs/_build/html")
DEST_FILE = pathlib.Path("output.tsv")


@dataclasses.dataclass
class DocFile:
    path: pathlib.Path
    code_examples: List[str]


def create_doc_file(path: pathlib.Path) -> DocFile:
    with open(path, "r") as file:
        soup = bs4.BeautifulSoup(file.read(), "lxml")
        code_blocks = soup.select(".code pre")
        code_examples = [code_block.get_text().strip() for code_block in code_blocks]
    return DocFile(path, code_examples)


@dataclasses.dataclass
class OutputRow:
    source: pathlib.Path
    position: int
    raw_code: str

    @property
    def identifier(self) -> str:
        identifier_str = f"{self.source}-{self.position}"
        return hashlib.sha1(identifier_str.encode()).hexdigest()

    @property
    def code(self) -> str:
        escaped_code = html.escape(self.raw_code)
        lines = [
            self._replace_leading_spaces_with_nbsp(line)
            for line in escaped_code.split("\n")
        ]
        return "<br>".join(lines)

    def __iter__(self) -> Iterator[str]:
        return iter((self.identifier, str(self.source), self.code))

    @staticmethod
    def _replace_leading_spaces_with_nbsp(string: str) -> str:
        string_without_leading_spaces = string.lstrip(" ")
        leading_space_count = len(string) - len(string_without_leading_spaces)
        return "&nbsp;" * leading_space_count + string_without_leading_spaces


def create_output_rows(doc_files: List[DocFile]) -> Iterator[OutputRow]:
    for doc_file in doc_files:
        for position, code_example in enumerate(doc_file.code_examples):
            yield OutputRow(doc_file.path, position, code_example)


def main() -> None:
    src_files = SRC_DIR.glob("**/*.html")
    doc_files = [create_doc_file(path) for path in src_files]
    output_rows = create_output_rows(doc_files)
    with open(DEST_FILE, "w", newline="") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerows(output_rows)


if __name__ == "__main__":
    main()
