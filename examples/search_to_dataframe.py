# /// script
# requires-python = ">=3.10"
# dependencies = [
#    "itables",
#    "pandas",
#    "python-dotenv",
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
from typing import Annotated

import itables
import pandas as pd
import typer
from dotenv import load_dotenv

import urlscan

load_dotenv()

API_KEY = os.getenv("URLSCAN_API_KEY")


def main(
    query: Annotated[str, typer.Argument(help="Search query")],
    api_key: Annotated[
        str | None,
        typer.Option(help="Your API key, defaults to URLSCAN_API_KEY env"),
    ] = None,
    limit: Annotated[int, typer.Option(help="Limit of search results")] = 100,
    path: Annotated[
        Path, typer.Option(help="Path to save a dataframe as an HTML file")
    ] = Path("report.html"),
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
