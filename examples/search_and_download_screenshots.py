# /// script
# requires-python = ">=3.10"
# dependencies = [
#    "python-dotenv",
#    "typer",
#    "urlscan-python",
# ]
# ///

# this script demonstrates how to do search and download screenshots.
# usage: uv run examples/search_and_download_screenshots.py <QUERY>
#        (e.g. uv run examples/search_and_download_screenshots.py domain:example.com)

import os
from pathlib import Path
from typing import Annotated

import typer
from dotenv import load_dotenv

import urlscan

load_dotenv()

API_KEY = os.getenv("URLSCAN_API_KEY")


def main(
    query: Annotated[str, typer.Argument(help="Search query")],
    api_key: Annotated[
        str | None,
        typer.Option(help="Your API key. Defaults to URLSCAN_API_KEY env."),
    ] = None,
    limit: Annotated[int, typer.Option(help="Limit of search results")] = 10,
    dest: Annotated[
        Path, typer.Option(help="Destination directory to download screenshots")
    ] = Path("/tmp"),
) -> None:
    api_key = api_key or API_KEY
    assert api_key, "API key is required"

    with urlscan.Client(api_key) as client:
        for result in client.search(query, limit=limit):
            _id: str = result["_id"]
            screenshot = client.get_screenshot(_id)

            path = dest / f"{_id}.png"
            path.write_bytes(screenshot.read())
            print(f"Downloaded screenshot to {path}")  # noqa: T201


if __name__ == "__main__":
    typer.run(main)
