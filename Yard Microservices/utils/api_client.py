"""
Purpose:
--------
Provides a reusable HTTP client wrapper for API calls.

Responsibilities:
-----------------
- Executes POST requests using 'requests' library.
- Centralizes timeout and request execution logic.

Why This File Exists:
---------------------
- Avoids repeated 'requests.post' calls in tests.
- Allows easy enhancements (logging, retries, headers).
- Keeps test scripts clean and readable.
"""

import requests

def post(url, headers, payload):
    response = requests.post(
        url=url,
        headers=headers,
        json=payload,
        timeout=90
    )
    return response
