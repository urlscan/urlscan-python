# Development

This doc explains how to set up dev env if you want to get involved with this project.

## Requirements

- Python 3.10+

## Setup

This project uses [uv](https://github.com/astral-sh/uv) as a project manager and [Lefthook](https://github.com/evilmartians/lefthook) as a Git hooks manager.

```bash
git clone https://github.com/urlscan/urlscan-python
cd urlscan-python

# install uv
pip install -r requirements.txt
# sync uv
uv sync
# install Lefthook
uv run lefthook install
```

## Test

This project uses [pytest](https://docs.pytest.org/en/stable/) as a testing framework.

```bash
uv run pytest
```

## Docs

This project uses [MkDocs](https://www.mkdocs.org/) as a documentation tool and uses [Mike](https://github.com/jimporter/mike) for versioning.

```bash
# run the dev server
uv run mike serve
# or build the docs
uv run mke build
```
