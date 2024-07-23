import pytest

from page_tracker.app import redis, REDIS_PORT


@pytest.mark.timeout(1.5)
def test_should_update_redis(http_client, redis_client=redis(port=REDIS_PORT)):
    # Given
    redis_client.set("page_views", 4)

    # When
    response = http_client.get("/")

    # Then
    assert response.status_code == 200
    assert response.text == "This page has been seen 5 times."
    assert redis_client.get("page_views") == b"5"
