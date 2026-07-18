# Privacy and Security

Trace Aviary is local-first and does not require online model calls. Logs can contain credentials and personal data, so the parser masks common token, password, API key, and bearer-token shapes before exporting raw examples.

Boundaries:

- The tool is not a data-loss-prevention product.
- Users should redact production data before sharing catalogs.
- The GitHub Pages demo deploys only deterministic synthetic logs.
- SQLite persistence stores exported catalog payloads locally and should not be pointed at sensitive shared locations without review.
