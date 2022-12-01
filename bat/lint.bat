@echo off

call :lint .
exit /B 0

:lint
echo Linting '%1'...
black --quiet --check %1 >NUL 2>&1
if not %ERRORLEVEL% == 0 (
    echo black - failed >&2
    exit /B 1
) else (
    echo black - passed
)

flake8 --quiet %1 >NUL 2>&1
if not %ERRORLEVEL% == 0 (
    echo flake8 - failed >&2
    exit /B 1
) else (
    echo flake8 - passed
)

isort --check %1 >NUL 2>&1
if not %ERRORLEVEL% == 0 (
    echo isort - failed >&2
    exit /B 1
) else (
    echo isort - passed
)

mypy %1 >NUL 2>&1
if not %ERRORLEVEL% == 0 (
    echo mypy - failed >&2
    exit /B 1
) else (
    echo mypy - passed
)

exit /B 0
