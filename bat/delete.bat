@echo off
set STACK_NAME=samlocal-python

samlocal delete ^
    --config-env samlocal ^
    --stack-name %STACK_NAME%
