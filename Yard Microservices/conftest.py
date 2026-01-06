import requests
import pytest

@pytest.fixture(scope="session")
def yard_base_url():
    return "https://prepacyardapi.logstarerp.com"


@pytest.fixture(scope="session")
def yard_headers():
    return {
        "Content-Type": "application/json",
        "SiteId": "1"
    }


@pytest.fixture(scope="session")
def yard_rule_status(yard_base_url, yard_headers):
    """
    Fetch Yard Rule configuration ONCE per test session.
    Acts as environment capability map.
    """

    url = f"{yard_base_url}/yard/v1/yard-rule"

    response = requests.get(url, headers=yard_headers, timeout=30)
    assert response.status_code == 200

    data = response.json()
    assert data is not None

    print("\n--- Yard Rule Configuration ---")
    print(f"Site ID: {data.get('siteId')}")
    print(f"Is Auto Plan Position Feature On ? : {data.get('isAutoPlan')}")
    print(f"Is Same Size Type on Same Size Type Allowed ? : {data.get('isOnly40on40And20on20')}")
    print(f"isTabularOnYardView: {data.get('isTabularOnYardView')}")

    return {
    "siteId": data.get("siteId"),
    "isAutoPlan": bool(data.get("isAutoPlan")),
    "isOnly40on40And20on20": bool(data.get("isOnly40on40And20on20")),
    "isTabularOnYardView": bool(data.get("isTabularOnYardView")),
}