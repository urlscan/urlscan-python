# urlscan-python

The official Python API client for urlscan.io.

## Installation

```bash
pip install urlscan-python
```

## Usage

```py
import urlscan


with urlscan.Client("<your_api_key>") as client:
    res = client.scan("http://example.com")
    print(res)
```

See [documentation](https://urlscan.github.io/urlscan-python) for more details.
