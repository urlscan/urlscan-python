# /// script
# requires-python = ">=3.10"
# dependencies = [
#    "tenacity",
#    "typer",
#    "urlscan-python",
# ]
# ///

# this script demonstrates how to handle rate limit with [tenacity](https://tenacity.readthedocs.io/en/latest/).
# usage: uv run examples/rate_limit_handling.py "page.domain:example.com"

import os
import time

import typer
from tenacity import TryAgain, retry

import urlscan

API_KEY = os.getenv("URLSCAN_API_KEY")


@retry
def get_result_with_retry(client: urlscan.Client, uuid: str):
    """Get the result of a scan."""
    try:
        return client.result(uuid)
    except urlscan.RateLimitError as exc:
        print(f"Rate limit error hit: {exc}")  # noqa: T201
        print(f"Wait {exc.rate_limit_reset_after} seconds before retrying...")  # noqa: T201
        time.sleep(exc.rate_limit_reset_after)
        raise TryAgain from exc


def main(
    q: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(1000, help="Limit the number of search results"),
    api_key: str | None = typer.Option(None, help="Your API key"),
) -> None:
    api_key = api_key or API_KEY
    assert api_key

    with urlscan.Client(api_key) as client:
        for result in client.search(q, limit=limit):
            uuid: str = result["_id"]
            result = get_result_with_retry(client, uuid)
            print(result["task"]["uuid"], result["task"]["url"])  # noqa: T201


if __name__ == "__main__":
    typer.run(main)
