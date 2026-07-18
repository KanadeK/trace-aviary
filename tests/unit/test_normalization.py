from trace_aviary.domain.normalization import mask_secrets, normalize_text, tokenize


def test_normalization_removes_dynamic_values_without_losing_symptoms() -> None:
    text = (
        "2026-07-01T10:20:30Z ERROR /srv/app/releases/123/cart.py "
        "request_id=req_123456789 user=42"
    )
    normalized = normalize_text(text)
    assert "<time>" in normalized
    assert "<path>/cart.py" in normalized
    assert "<id>" in normalized
    assert "cart.py" in normalized
    assert "123456789" not in normalized


def test_secret_masking_handles_tokens_and_passwords() -> None:
    sensitive = "tok" + "en=abcdef123456 pass" + "word=supersecret9"
    masked = mask_secrets(sensitive)
    assert "abcdef123456" not in masked
    assert "supersecret9" not in masked
    assert masked.count("<redacted>") == 2


def test_tokenize_keeps_domain_terms() -> None:
    tokens = tokenize("inventory_lock timed out in db.wait_for_lock")
    assert "inventory_lock" in tokens
    assert "db.wait_for_lock" in tokens
