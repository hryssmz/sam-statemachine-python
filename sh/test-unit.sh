#!/bin/sh
pytest \
    --cov=functions \
    --cov-report=term \
    tests/unit
