# /// script
# requires-python = ">=3.10"
# dependencies = [
#    "typer",
#    "urlscan-python",
# ]
# ///

# this script demonstrates how to do bulk scan.
# usage: uv run examples/bulk_scan.py URL...
#        (e.g. uv run examples/bulk_scan.py http://example.com http://example.org)

import os

import typer

import urlscan

API_KEY = os.getenv("URLSCAN_API_KEY")


def main(
    url: list[str] = typer.Argument(..., help="URL(s) to scan"),  # noqa: B008
    api_key: str | None = typer.Option(None, help="Your API key"),
    visibility: str = typer.Option("public", help="Visibility of scan(s)"),
) -> None:
    api_key = api_key or API_KEY
    assert api_key

    with urlscan.Client(api_key) as client:
        uuids: list[str] = [
            client.scan(u, visibility=visibility)["uuid"]  # type: ignore
            for u in url
        ]

        for uuid in uuids:
            client.wait_for_result(uuid)

        results = [client.get_result(uuid) for uuid in uuids]
        for result in results:
            print(result["task"]["reportURL"])  # noqa: T201


if __name__ == "__main__":
    typer.run(main)
