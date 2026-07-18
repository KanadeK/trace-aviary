.PHONY: verify demo package release-check

verify:
	python -m ruff check .
	python -m mypy src
	python -m pytest -q --cov=src --cov-report=term-missing --cov-fail-under=80
	python -m build

demo:
	python -m trace_aviary.cli demo

package:
	python scripts/package_release.py

release-check:
	python scripts/release_check.py
