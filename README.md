# wait_for_it.py

[![Build Status](https://travis-ci.org/yeraydiazdiaz/wait_for_it.py.svg?branch=master)](https://travis-ci.org/yeraydiazdiaz/wait_for_it.py)

A pure Python implementation of [wait-for-it.sh](https://github.com/vishnubob/wait-for-it) with no dependencies, however if [requests](https://docs.python-requests.org) is available it will be used.

Intended to be used as a lightweight dependency service checker before startup of apps.

## Requirements

Python3+

## Usage

Copy and paste the script into your deployable and prepend the startup of your app with the check for a required service:

```
python wait_for_it.py http://localhost:1234 && start_my_app
```

Optionally specify:
- `-t N` or `--timeout N` to wait N seconds before giving up, defaults to 5 seconds.
- `-m N` or `--max-attempts N` to limit the number of attempts to connect to the service, defaults to 3. Set to 0 to not retry.
- `-r N` or `--retry-every N` to wait N seconds between attempts, defaults to 1 second.

## Why?

In Docker environments you usually need a reliable healthcheck command, problem is most of the time you have to install [`curl` or a similar tool](https://blog.sixeyed.com/docker-healthchecks-why-not-to-use-curl-or-iwr/). This script will work for any image with Python 3 installed.

I kept using variations of this script in Python Docker healthchecks to avoid pulling external packages or copy some impossible to understand bash code, so I decided to write this fairly simple one that people can easily adapt if needed.

## Alternatives

- [`wait-for-it.sh`](https://github.com/vishnubob/wait-for-it) and some Bash magic
- [The `wait-for-it` package in PyPI](https://pypi.org/project/wait-for-it/)

## License

MIT
