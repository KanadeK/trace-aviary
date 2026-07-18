from trace_aviary.domain.parsing import parse_records


def test_parse_jsonl_records() -> None:
    events = parse_records('{"message": "boom", "level": "ERROR", "root_cause": "x"}\nplain line\n')
    assert len(events) == 2
    assert events[0].level == "ERROR"
    assert events[0].expected_root == "x"
    assert events[1].message == "plain line"


def test_parse_sentry_style_export() -> None:
    body = {
        "events": [
            {
                "message": "Checkout failed",
                "exception": {
                    "values": [
                        {
                            "value": "KeyError customer_tier",
                            "stacktrace": {
                                "frames": [
                                    {
                                        "filename": "/srv/app/pay.py",
                                        "lineno": 12,
                                        "function": "decode",
                                    }
                                ]
                            },
                        }
                    ]
                },
            }
        ]
    }
    events = parse_records(__import__("json").dumps(body))
    assert events[0].message == "KeyError customer_tier"
    assert "pay.py" in (events[0].stack or "")
