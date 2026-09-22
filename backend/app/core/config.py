import os
import secrets
import warnings
from dotenv import load_dotenv

# Must run before any os.getenv() calls below, otherwise values set only in a
# local .env file (as opposed to a real process env var) are missed.
load_dotenv()

_env_secret_key = os.getenv("SECRET_KEY")
if _env_secret_key:
    SECRET_KEY = _env_secret_key
else:
    # No persistent SECRET_KEY configured: fall back to a random key so local
    # dev still works, but warn loudly since this breaks JWTs across restarts
    # and across multiple worker processes. Never rely on this in production.
    warnings.warn(
        "SECRET_KEY is not set — using a randomly generated, non-persistent "
        "key. All existing sessions will be invalidated on every restart, "
        "and this will break auth if you run more than one worker process. "
        "Set SECRET_KEY in your environment for any real deployment.",
        RuntimeWarning,
        stacklevel=1,
    )
    SECRET_KEY = secrets.token_hex(32)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DATABASE_URL = os.getenv("DATABASE_URL")