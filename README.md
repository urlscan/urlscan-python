# urlscan-python

The official Python API client for urlscan.io.

## Requirements

- Python 3.10+

## Installation

```bash
pip install urlscan-python
```

## Quickstart

Start by importing `urlscan` module

```py
>>> import urlscan
```

Create a client with your API key:

```py
>>> client = urlscan.Client("<your_api_key>")
```

Scan a URL:

```py
>>> client.scan("http://example.com")
```

Get a scan result:

```py
>>> client.get_result("<uuid>")
```

`urlscan.Client.search()` returns an iterator to iterate search results:

```py
>>> for result in client.search("page.domain:example.com"):
>>>     print(result["_id"])
```

## Examples

See [Examples](https://github.com/urlscan/urlscan-python/tree/main/examples/).

## References

- [Client](https://urlscan.github.io/urlscan-python/references/client/)
- [Iterator](https://urlscan.github.io/urlscan-python/references/iterator/)
- [Errors](https://urlscan.github.io/urlscan-python/references/errors/)

## Help Wanted?

Please feel free to to [open an issue](https://github.com/urlscan/urlscan-python/issues/new) if you find a bug or some feature that you want to see implemented.
