import re
import secrets

BUILD_ID_PREFIX = "VX-"
BUILD_ID_PATTERN = re.compile(r"^VX-[0-9A-F]{5}$")


def generate_build_id() -> str:
    """Random public build ID such as VX-8F29A (cryptographically secure)."""
    return BUILD_ID_PREFIX + secrets.token_hex(3)[:5].upper()


def is_valid_build_id(build_id: str) -> bool:
    return bool(BUILD_ID_PATTERN.match(build_id))
