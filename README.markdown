A script that extracts all code snippets from the Symfony documentation and exports them to a TSV file.

Useful for importing into a flashcard program or learning tool of some sort.

Python 3.7 or later is required.

```bash
# Setup

# 1. Create a virtual environment.
python3 -m venv .venv

# 2. Activate the virtual environment.
source .venv/bin/activate

# 3. Download and build the Symfony documentation.
make symfony-docs/_build/html

# 4. Install Poetry.
pip install poetry

# 5. Use Poetry to install the remaining dependencies.
poetry install

# 6. Run the script.
python symfony_to_tsv.py
```
