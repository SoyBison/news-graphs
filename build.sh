#!/bin/bash

pip3 install -r requirements

gunicorn --bind 0.0.0.0:8080 wsgi:app