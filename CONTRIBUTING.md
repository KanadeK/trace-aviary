# Contributing

Thanks for improving Trace Aviary. Keep changes small, deterministic, and backed by tests.

1. Install Python 3.12.
2. Run `python -m pip install -e ".[dev]"`.
3. Run `python scripts/verify.py` before opening a pull request.
4. Do not include real customer logs, credentials, tokens, or unredacted personal data.

Bug fixes should include a regression test. New adapters should include deterministic fixtures.
