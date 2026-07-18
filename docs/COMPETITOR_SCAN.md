# Competitor Scan

Date: 2026-07-18

GitHub identity check before scan:

- `gh auth status`: logged in to `github.com` as `KanadeK`
- `gh api user --jq '{login: .login, id: .id}'`: `{"login":"KanadeK","id":121669563}`

## Naming Checks

| Query | Result |
| --- | --- |
| `Trace Aviary` | No repositories returned by `gh search repos` |
| `trace-aviary` | No repositories returned by `gh search repos` |

The project keeps the planned name `Trace Aviary` and repository slug `trace-aviary`.

## Related Repository Sampling

| Repository | Stars | Updated | Main function | Overlap |
| --- | ---: | --- | --- | --- |
| [tj/spotlight](https://github.com/tj/spotlight) | 40 | 2025-12-07 | Elasticsearch log querying frontend | Query UI overlaps logs, not incident clustering |
| [laban254/ml-for-infrastructure](https://github.com/laban254/ml-for-infrastructure) | 21 | 2026-07-11 | SRE/DevOps ML notebooks | Adjacent ML analysis, not packaged incident catalog workflow |
| [fluency03/logclustering-py](https://github.com/fluency03/logclustering-py) | 13 | 2024-11-19 | Log similarity clustering | Core clustering overlap, less focused on reproduction hypotheses and web/CLI workflow |
| [maria-grigorieva/ClusterLog](https://github.com/maria-grigorieva/ClusterLog) | 9 | 2026-03-21 | Error log clusterization | Similar clustering theme, no Sentry import or release catalog emphasis found in summary |
| [drylikov/Spotlight](https://github.com/drylikov/Spotlight) | 7 | 2026-03-04 | Elasticsearch log frontend fork | Query/tailing overlap only |
| [happyvives/Windows-IR](https://github.com/happyvives/Windows-IR) | 4 | 2026-06-05 | Incident-response log collection scripts | Incident response overlap, collection rather than clustering |
| [arshahin/well_log_clustering](https://github.com/arshahin/well_log_clustering) | 4 | 2022-07-29 | Geological well log clustering | Shares clustering term, different domain |
| [zontiveros/hiveary-logs](https://github.com/zontiveros/hiveary-logs) | 3 | 2021-10-30 | Hiveary log clustering algorithm | Algorithmic overlap, older and narrower |
| [darvinpatel/soc-automation-lab](https://github.com/darvinpatel/soc-automation-lab) | 2 | 2026-01-26 | SOC automation and log management | Security workflow overlap, not developer stack clustering |
| [pswaldia/Automatic-Server-Logs-Clustering-](https://github.com/pswaldia/Automatic-Server-Logs-Clustering-) | 2 | 2024-07-31 | Server log intent grouping | Similar clustering idea, not packaged as an on-call catalog/export tool |

## Differentiation

Public repository sampling did not find an active same-name project or a highly isomorphic project above roughly 70 percent MVP overlap. Trace Aviary narrows on developer/on-call incident triage: deterministic local parsing, dynamic-value normalization, explainable TF-IDF clustering, representative stack samples, common symptom tokens, time buckets, and a reproduction-hypothesis template.
