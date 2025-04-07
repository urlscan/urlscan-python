# /// script
# requires-python = ">=3.10"
# dependencies = [
#    "pillow",
#    "typer",
#    "urlscan-python",
# ]
# ///

# this script demonstrates how to get a screenshot & convert it to a PIL image.
# usage: uv run examples/screenshot_to_pil.py <UUID>

import os

import typer
from PIL import Image

import urlscan

API_KEY = os.getenv("URLSCAN_API_KEY")


def main(
    uuid: str = typer.Argument(..., help="Result UUID"),
    api_key: str | None = typer.Option(None, help="Your API key"),
) -> None:
    api_key = api_key or API_KEY
    assert api_key

    with urlscan.Client(api_key) as client:
        screenshot = client.screenshot(uuid)
        image = Image.open(screenshot)
        image.show()


if __name__ == "__main__":
    typer.run(main)
