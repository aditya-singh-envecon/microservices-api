from datetime import datetime, timezone, timedelta
import random
import string


def generate_tmod_no():
    """
    MHAD + 2 digits + 2 letters + 4 digits
    Example: MHAD12AB3456
    """
    return (
        "MHAD"
        + f"{random.randint(10,99)}"
        + "".join(random.choices(string.ascii_uppercase, k=2))
        + f"{random.randint(1000,9999)}"
    )


def get_current_time():
    """
    Format: 2025-12-30T10:14:58.021Z
    """
    return (
        datetime.now(timezone.utc)
        .strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    )


def get_time_minus_5_minutes():
    """
    Format: 2025-12-30T10:09:58.021Z
    """
    return (
        (datetime.now(timezone.utc) - timedelta(minutes=5))
        .strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    )
