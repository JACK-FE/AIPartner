#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    import config.py314_patch  # noqa: E402  Python 3.14 compat
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
