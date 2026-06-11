# Logging Guide

All scripts in this workspace share a single daily-rotating logger defined in
[lang/logger.py](logger.py).

## What it does

| Feature | Detail |
|---|---|
| Log location | `<workspace>/logs/YYYY-MM-DD.log` |
| New file cadence | One file per calendar day, automatically |
| Console output | `INFO` and above |
| File output | `DEBUG` and above (full detail for post-mortem) |
| Format | `YYYY-MM-DD HH:MM:SS \| script_name \| LEVEL \| message` |

Example log line:
```
2026-06-11 07:14:03 | scrap_pad                           | INFO     | LLM request dispatched — model=gemini-2.5-flash
```

---

## Quick start — adding logging to a new script

```python
from logger import get_logger          # adjust the import path if needed (see below)

log = get_logger(__name__)             # __name__ becomes the script identifier in the log

log.info("Step started")               # visible in console + file
log.debug("Raw value: %s", my_var)    # file only — use for verbose detail
log.warning("Unexpected state: %s", state)
log.error("Call failed: %s", err)
```

---

## Import path by location

| Script location | Import |
|---|---|
| `lang/` (same folder as `logger.py`) | `from logger import get_logger` |
| `lang/subdir/script.py` | `from lang.logger import get_logger` (run from workspace root) |
| Any other top-level folder | `import sys; sys.path.insert(0, "lang"); from logger import get_logger` |

The simplest approach is to always run scripts from the **workspace root**:
```bash
python lang/my_script.py
```
and use a relative import via `sys.path` if the script is outside `lang/`.

---

## Log levels — when to use what

| Level | Use for |
|---|---|
| `log.debug(...)` | Internal state, variable values, raw API payloads — anything noisy that you'd only need when diagnosing a bug |
| `log.info(...)` | Key steps: session start/end, decisions made, tool calls dispatched, final outputs |
| `log.warning(...)` | Something unexpected happened but execution continued |
| `log.error(...)` | A failure that broke a step; include the exception with `exc_info=True` |

### Logging exceptions

```python
try:
    result = call_api()
except Exception as e:
    log.error("API call failed", exc_info=True)   # records full traceback to file
    raise
```

---

## Recommended log structure for any script

```python
log.info("=" * 60)
log.info("my_script — execution started")
log.info("Key config: model=%s, param=%s", model, param)
log.info("=" * 60)

# ... your logic ...
log.info("Step 1 complete — result: %s", result)

log.info("=" * 60)
log.info("my_script — execution finished")
log.info("=" * 60)
```

This makes it easy to scan the log file and find exactly where each run started
and what happened, even months later.

---

## Viewing logs

```bash
# Today's log
cat logs/$(date +%F).log

# Search for a specific script's runs
grep "scrap_pad" logs/2026-06-11.log

# Watch live as a script runs
tail -f logs/$(date +%F).log
```

On Windows (PowerShell):
```powershell
Get-Content "logs\$(Get-Date -Format 'yyyy-MM-dd').log" -Wait   # live tail
Select-String "scrap_pad" "logs\2026-06-11.log"                 # grep equivalent
```
