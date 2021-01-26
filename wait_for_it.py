"""
wait_for_it.py -- A pure Python implementation of wait-for-it.sh with no dependencies

Intended to be used as a lightweight dependency service check before startup of apps.
"""

import argparse
import sys
import time
import urllib.error
import urllib.request
from typing import Tuple


class ServiceUnavailableError(Exception):
    pass



def check_service(service_url: str) -> None:
    try:  # attempt to use requests if present
        import requests
        try:
            response = requests.get(service_url)
            if response.status_code != 200:
                raise ServiceUnavailableError()
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
        ) as exc:
            raise ServiceUnavailableError from exc
    except ImportError:  # otherwise use urllib
        try:
            response = urllib.request.urlopen(service_url)
            if response.status != 200:
                raise ServiceUnavailableError()
        except urllib.error.URLError as exc:
            raise ServiceUnavailableError from exc


def wait_for_service(service_url: str, timeout: int = 5, retry_interval: int = 1) -> Tuple[bool, float]:
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


def create_parser() -> argparse.ArgumentParser:
    """Returns a preconfigured argument parser."""
    parser = argparse.ArgumentParser(
        description="Wait for HTTP services to be available"
    )
    parser.add_argument("service_url", help="URL of service to wait for")
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=5,
        help="Maximum time in seconds to wait for service, defaults to 5",
    )
    parser.add_argument(
        "-r",
        "--retry",
        type=int,
        default=1,
        help="Time in seconds to wait between attempts to connect, defaults to 1",
    )
    return parser


def main():
    parser = create_parser()
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


if __name__ == "__main__":
    main()
