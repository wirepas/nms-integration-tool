# Copyright Wirepas Oy 2026 licensed under Apache 2.0
#
# Please see file LICENSE for full license details.
import os
import sys
from unittest.mock import MagicMock

# Make example scripts importable
_scripts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "examples", "scripts"))
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

# Mock 'schedule' before postgres_import is collected by pytest.
# postgres_import.py applies @repeat(every(1).minutes) at module level, which would
# register the job and fail if schedule is not installed.
# Setting repeat.return_value to an identity decorator keeps import_job as the real function.
if "schedule" not in sys.modules:
    _mock_schedule = MagicMock()
    _mock_schedule.repeat.return_value = lambda f: f
    sys.modules["schedule"] = _mock_schedule

# Ensure LOG_LEVEL is a string so postgres_import's logging.basicConfig call
# (which does os.getenv("LOG_LEVEL", logging.INFO).upper()) does not fail on int.upper().
os.environ.setdefault("LOG_LEVEL", "INFO")
