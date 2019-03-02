.PHONY: code-quality

code-quality:
	black symfony_to_csv.py
	mypy --ignore-missing-imports symfony_to_csv.py
	pylint --disable=missing-docstring,too-few-public-methods symfony_to_csv.py

symfony-docs/_build/html: symfony-docs
	pip install --requirement symfony-docs/_build/.requirements.txt
	make --directory=symfony-docs/_build html

symfony-docs:
	git clone --branch master --depth 1 https://github.com/symfony/symfony-docs.git
