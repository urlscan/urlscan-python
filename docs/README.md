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

- [Client](./references/client/)
- [Iterator](./references/iterator/)
- [Errors](./references/errors/)
