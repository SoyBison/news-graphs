#!/bin/sh
gunicorn --chdir app wsgi:app -b 0.0.0.0:8000