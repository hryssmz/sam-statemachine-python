@echo off
pytest ^
    --cov=functions ^
    --cov-report=term ^
    tests\unit
