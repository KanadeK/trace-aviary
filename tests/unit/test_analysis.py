from trace_aviary.adapters.samples import synthetic_jsonl
from trace_aviary.domain.analysis import adjusted_rand_for_expected, analyze_events
from trace_aviary.domain.parsing import parse_records


def test_synthetic_roots_are_separated_with_high_ari() -> None:
    events = parse_records(synthetic_jsonl(count=500, seed=42))
    result = analyze_events(events, n_clusters=5)
    ari = adjusted_rand_for_expected(events, result)
    assert ari is not None
    assert ari >= 0.95
    assert len(result.clusters) == 5
    assert sum(cluster.sample_count for cluster in result.clusters) == 500


def test_dynamic_request_ids_do_not_create_extra_clusters() -> None:
    events = parse_records(
        "\n".join(
            [
                (
                    '{"message":"checkout worker timed out acquiring inventory_lock '
                    'request_id=req_11111111","root_cause":"deadlock"}'
                ),
                (
                    '{"message":"checkout worker timed out acquiring inventory_lock '
                    'request_id=req_99999999","root_cause":"deadlock"}'
                ),
                (
                    '{"message":"payment payload missing required field customer_tier '
                    'request_id=req_22222222","root_cause":"schema"}'
                ),
                (
                    '{"message":"payment payload missing required field customer_tier '
                    'request_id=req_33333333","root_cause":"schema"}'
                ),
            ]
        )
    )
    result = analyze_events(events, n_clusters=2)
    assert sorted(cluster.sample_count for cluster in result.clusters) == [2, 2]
