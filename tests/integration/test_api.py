from fastapi.testclient import TestClient
from trace_aviary.api import app


def test_homepage_renders_real_clusters() -> None:
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "Incident species" in response.text
    assert "Representative" not in response.text


def test_upload_analyze_path() -> None:
    client = TestClient(app)
    response = client.post(
        "/analyze",
        data={
            "pasted": (
                '{"message":"profile cache returned mismatched tenant scope",'
                '"root_cause":"cache"}'
            ),
            "clusters": "1",
        },
    )
    assert response.status_code == 200
    assert "profile" in response.text
