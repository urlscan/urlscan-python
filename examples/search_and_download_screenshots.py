# /// script
# requires-python = ">=3.10"
# dependencies = [
#    "typer",
#    "urlscan-python",
# ]
# ///

# this script demonstrates how to do search and download screenshots.
# usage: uv run examples/search_and_download_screenshots.py <QUERY>
#        (e.g. uv run examples/search_and_download_screenshots.py domain:example.com)

import os
from pathlib import Path

import typer

import urlscan

API_KEY = os.getenv("URLSCAN_API_KEY")


def main(
    query: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(10, help="Limit of search results"),
    api_key: str | None = typer.Option(None, help="Your API key"),
    dest: Path = typer.Option(  # noqa: B008
        Path("/tmp"), help="Destination directory to download screenshots"
    ),
) -> None:
    api_key = api_key or API_KEY
    assert api_key

    with urlscan.Client(api_key) as client:
        for result in client.search(query, limit=limit):
            _id: str = result["_id"]
            screenshot = client.get_screenshot(_id)

            path = dest / f"{_id}.png"
            path.write_bytes(screenshot.read())
            print(f"Downloaded screenshot to {path}")  # noqa: T201


if __name__ == "__main__":
    typer.run(main)
