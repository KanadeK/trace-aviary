# Trace Aviary

Trace Aviary 会把日志和堆栈聚类成“事故物种”：同一类反复出现的失败家族，并给出代表样本、共同症状、时间分布和最小复现假设。

## 快速开始

```bash
python -m pip install -e ".[dev]"
trace-aviary sample --output examples/synthetic_logs.jsonl
trace-aviary analyze examples/synthetic_logs.jsonl --clusters 5 --output dist-release/incident_catalog.json
trace-aviary demo
uvicorn trace_aviary.api:app --reload
```

## 功能

- 导入纯文本、JSONL 和 Sentry 风格 JSON。
- 规范化路径、时间戳、请求 ID、数字、邮箱和常见密钥形态。
- 使用本地 deterministic TF-IDF 聚类，不调用在线模型。
- 输出每个簇的代表堆栈、共同 token、时间桶、样本数和复现假设。
- 提供 CLI、FastAPI Web UI、SQLite 保存适配器和 500 条合成样例日志。

## 测试

```bash
python scripts/verify.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -p pytest_cov -q --cov=src --cov-report=term-missing --cov-fail-under=80
make verify
make demo
make package
make release-check
```

合成样例包含 5 个已知根因，测试会验证聚类 ARI、动态 request id 不会误分簇、导出结果和 Web/CLI 主路径。

## 隐私边界

项目本地优先运行，并会在导出前掩码常见 token/password/API key 形态。但它不是完整 DLP 产品，公开分享前仍应人工复核日志与 catalog。
