import sys

import packaging.version


def main(version: str):
    """convert semver version to PEP 440 styled version"""
    parsed = packaging.version.parse(version)
    print(parsed)  # noqa: T201


if __name__ == "__main__":
    main(sys.argv[1])
