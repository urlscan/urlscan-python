# /// script
# requires-python = ">=3.10"
# dependencies = [
#    "pillow",
#    "python-dotenv",
#    "typer",
#    "urlscan-python",
# ]
# ///

# this script demonstrates how to get a screenshot & convert it to a PIL image.
# usage: uv run examples/screenshot_to_pil.py <UUID>

import os
from typing import Annotated

import typer
from dotenv import load_dotenv
from PIL import Image

import urlscan

load_dotenv()

API_KEY = os.getenv("URLSCAN_API_KEY")


def main(
    uuid: Annotated[str, typer.Argument(help="Result UUID")],
    api_key: Annotated[
        str | None,
        typer.Option(help="Your API key, defaults to URLSCAN_API_KEY env"),
    ] = None,
) -> None:
    api_key = api_key or API_KEY
    assert api_key

    with urlscan.Client(api_key) as client:
        screenshot = client.get_screenshot(uuid)
        image = Image.open(screenshot)
        image.show()


if __name__ == "__main__":
    typer.run(main)
