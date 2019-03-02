import csv
import dataclasses
import hashlib
import pathlib
from typing import Iterator, List

import bs4

SRC_DIR = pathlib.Path("symfony-docs/_build/html")
DEST_FILE = pathlib.Path("output.csv")


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
class CSVRow:
    source: pathlib.Path
    position: int
    code: str

    @property
    def identifier(self) -> str:
        identifier_str = f"{self.source}-{self.position}"
        return hashlib.sha1(identifier_str.encode()).hexdigest()

    def __iter__(self) -> Iterator[str]:
        return iter((self.identifier, str(self.source), self.code))


def create_csv_rows(doc_files: List[DocFile]) -> Iterator[CSVRow]:
    for doc_file in doc_files:
        for position, code_example in enumerate(doc_file.code_examples):
            yield CSVRow(doc_file.path, position, code_example)


def main() -> None:
    src_files = SRC_DIR.glob("**/*.html")
    doc_files = [create_doc_file(path) for path in src_files]
    csv_rows = create_csv_rows(doc_files)
    with open(DEST_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(csv_rows)


if __name__ == "__main__":
    main()
