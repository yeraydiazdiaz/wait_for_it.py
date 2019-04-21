"""
wait_for_it.py -- A pure Python implementation of wait-for-it.sh with no dependencies

Intended to be used as a lightweight dependency service check before startup of apps.
"""

import argparse
import urllib.request
import urllib.error
import sys
import time


class ServiceUnavailableError(Exception):
    pass


try:
    import requests

    def check_service(service_url: str):
        try:
            response = requests.get(service_url)
            if response.status != 200:
                raise ServiceUnavailableError()
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
        ) as exc:
            raise ServiceUnavailableError from exc


except ImportError:

    def check_service(service_url: str):
        try:
            resp = urllib.request.urlopen(service_url)
            if resp.status != 200:
                raise ServiceUnavailableError()
        except urllib.error.URLError as exc:
            raise ServiceUnavailableError from exc


def wait_for_service(service_url: str, timeout: int = 5, retry_interval: int = 1):
    """Waits for an HTTP service to respond with a 200 status code.

    Returns a 2-tuple of success, time elapsed for the service to respond.

    Args:
        - service_url: The HTTP URL where the service is expected to respond.
        - timeout: Seconds to wait for the service to respond, defaults to 5 seconds.
        - retry_interval: Number of seconds to wait between attempts, defaults to 1 second.
    """
    start = time.time()
    while True:
        elapsed_time = time.time() - start
        try:
            check_service(service_url)
            return True, elapsed_time
        except ServiceUnavailableError:
            pass

        if elapsed_time > timeout:
            return False, elapsed_time
        else:
            time.sleep(retry_interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Wait for HTTP services to be available"
    )
    parser.add_argument("service_url", help="URL of service to wait for")
    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Maximum time in seconds to wait for service, defaults to 5",
    )
    parser.add_argument(
        "--retry",
        type=int,
        default=1,
        help="Time in seconds to wait between attempts to connect, defaults to 1",
    )
    args = parser.parse_args()

    success, elapsed_time = wait_for_service(
        args.service_url, timeout=args.timeout, retry_interval=args.retry
    )
    print(
        "Service {} {} after {:.2f} seconds".format(
            args.service_url,
            "available" if success else "did not respond",
            elapsed_time,
        )
    )
    sys.exit(not success)
