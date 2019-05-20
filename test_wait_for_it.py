import wait_for_it


def test_requests(mocker, httpserver):
    import requests

    mocker.spy(requests, "get")
    httpserver.serve_content("OK", 200)

    success, _ = wait_for_it.wait_for_service(httpserver.url, timeout=1)

    assert success is True
    assert requests.get.call_count == 1


def test_urllib(mocker, httpserver):
    mocker.patch("requests.get", side_effect=ImportError)
    httpserver.serve_content("OK", 200)

    success, _ = wait_for_it.wait_for_service(httpserver.url, timeout=1)

    assert success is True


def test_unreachable_server(httpserver):
    success, _ = wait_for_it.wait_for_service("http://localhost:1234", timeout=1)
    assert success is False


def test_non_200(httpserver):
    httpserver.serve_content("Bad Request", 500)
    success, _ = wait_for_it.wait_for_service(httpserver.url, timeout=1)
    assert success is False


def test_max_attempts(mocker, httpserver):
    mocker.spy(wait_for_it, "check_service")
    httpserver.serve_content("Bad Request", 500)

    success, _ = wait_for_it.wait_for_service(httpserver.url, max_attempts=3)

    assert success is False
    assert wait_for_it.check_service.call_count == 3


def test_max_attempts_zero(mocker, httpserver):
    mocker.spy(wait_for_it, "check_service")
    httpserver.serve_content("Bad Request", 500)

    success, _ = wait_for_it.wait_for_service(httpserver.url, max_attempts=0)

    assert success is False
    assert wait_for_it.check_service.call_count == 1


def test_retry_interval(mocker, httpserver):
    mocker.spy(wait_for_it, "check_service")
    httpserver.serve_content("Bad Request", 500)

    success, _ = wait_for_it.wait_for_service(httpserver.url, timeout=0, max_attempts=3)

    assert success is False
    assert wait_for_it.check_service.call_count == 1
