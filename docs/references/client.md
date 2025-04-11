::: urlscan.Client

## Retry

This library provides an option for automatic retry based on [X-Rate-Limit-Reset-After HTTP header](https://urlscan.io/docs/api/#ratelimit) when a request gets `429 Too Many Requests` error.

You can enable it by:

```py
with Client("<api_key>", retry=True) as client:
    ...
```

or setting `URLSCAN_RETRY` environmental variable as `true`.

```bash
URLSCAN_RETRY=true python /path/to/script.py
```
