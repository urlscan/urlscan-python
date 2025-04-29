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
>>> res = client.scan("<url>", visibility="public")
>>> uuid: str = res["uuid"]
```

Wait for a scan result:

```py
>>> client.wait_for_result(uuid)
```

Get a scan result:

```py
>>> result = client.get_result(uuid)
```

Bulk scan:

```py
>>> client.bulk_scan(["<url>", "<url>"], visibility="public")
```

Alternatively, you can use `_and_get_result(s)` suffixed methods to do scan, wait and get at once.

```py
>>> client.scan_and_get_result("<url>", visibility="public")
>>> client.bulk_scan_and_get_results(["<url>", "<url>"], visibility="public")
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
