# Release Checklist

- Confirm `gh auth status` is authenticated as `KanadeK`.
- Set local Git identity to `KanadeK <121669563+KanadeK@users.noreply.github.com>`.
- Run `python -m pip install -e ".[dev]"`.
- Run `python scripts/verify.py`.
- For raw pytest, run with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` and `-p pytest_cov`.
- Run `python -m trace_aviary.cli demo`.
- Run `python scripts/package_release.py`.
- Run `git diff --check`.
- Run `git status --short`.
- Run `python scripts/release_check.py` after committing and packaging.
- Push `main` only after local checks pass.
- Enable GitHub Pages with GitHub Actions and wait for Pages deployment success.
- Create `v0.1.0` only after CI and Pages are green.
