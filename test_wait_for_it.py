import wait_for_it


def test_unreachable_server(httpserver):
    success, _ = wait_for_it.wait_for_service("http://localhost:1234", timeout=1)
    assert success is False


def test_requests(mocker, httpserver):
    import requests
    mocker.spy(requests, 'get')
    httpserver.serve_content('OK', 200)

    success, _ = wait_for_it.wait_for_service(httpserver.url, timeout=1)

    assert success is True
    assert requests.get.call_count == 1


def test_urllib(mocker, httpserver):
    mocker.patch('requests.get', side_effect=ImportError)
    httpserver.serve_content('OK', 200)

    success, _ = wait_for_it.wait_for_service(httpserver.url, timeout=1)

    assert success is True
