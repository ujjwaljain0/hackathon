from __future__ import annotations

# Load environment variables from a .env file if present
try:  # pragma: no cover - simple import side effect
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    # If python-dotenv is not installed, skip silently
    pass
