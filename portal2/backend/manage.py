#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from dotenv import load_dotenv


def main():
    load_dotenv()
    """Run administrative tasks."""
    try:
        if os.environ["DJANGO_DEVELOPMENT"] == "true":
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
        else:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
    except KeyError as exc:
        raise KeyError(
            f"Env key {exc} not found! Maybe you forgot of env."
        )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
