# /// script
# requires-python = ">=3.10"
# dependencies = [
#    "itables",
#    "pandas",
#    "typer",
#    "urlscan-python",
# ]
# ///

# this script converts search results into a Pandas dataframe & shows it as an HTML table.
# usage: uv run examples/search_to_dataframe.py <QUERY>
#        (e.g. uv run examples/search_to_dataframe.py domain:example.com)

import os
import webbrowser
from pathlib import Path

import itables
import pandas as pd
import typer

import urlscan

API_KEY = os.getenv("URLSCAN_API_KEY")


def main(
    query: str = typer.Argument(..., help="Search query"),
    limit: int = typer.Option(10, help="Limit of search results"),
    api_key: str | None = typer.Option(None, help="Your API key"),
    path: Path = typer.Option(  # noqa: B008
        Path("report.html"),
        help="Path to save a dataframe as an HTML file",
    ),
) -> None:
    api_key = api_key or API_KEY
    assert api_key

    with urlscan.Client(api_key) as client:
        results = list(client.search(query, limit=limit))

    df = pd.json_normalize(results)
    html = itables.to_html_datatable(df)
    path.write_text(html)

    webbrowser.open(path.absolute().as_uri())


if __name__ == "__main__":
    typer.run(main)
