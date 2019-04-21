# wait_for_it.py

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
- `--timeout N` to wait N seconds before giving up, defaults to 5 seconds.
- `--retry N` to wait N seconds between attempts, defaults to 1 second.

## Why?

I kept using variations of this script in Python Docker entry points and didn't want to pull external packages or copy some impossible to understand bash code, so I decided to write this fairly simple one that people can easily adapt if needed.

## Alternatives

- [`wait-for-it.sh`](https://github.com/vishnubob/wait-for-it) and some Bash magic
- [The `wait-for-it` package in PyPI](https://pypi.org/project/wait-for-it/)

## License

MIT
