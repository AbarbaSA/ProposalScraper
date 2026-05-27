@echo off
REM Run the proposal scraper using the local virtual environment.
IF "%1"=="dry-run" (
  .venv\Scripts\python.exe -m scraper.run --dry-run
) ELSE (
  .venv\Scripts\python.exe -m scraper.run %*
)
