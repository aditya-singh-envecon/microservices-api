import json

from payloads.export_booking_payload import get_export_booking_payload
from utils.api_client import post


def test_create_export_booking_success(base_url, headers):
    """
    Test Case:
    ----------
    Create Export Booking (XCNC Export)

    Purpose:
    --------
    - Creates an Export Booking.
    - Validates successful API response.
    - Asserts only business-critical outcomes.
    """

    url = f"{base_url}/csm/v1/XCNCBooking/SaveExportBooking"
    payload = get_export_booking_payload()

    print("\n📤 POST Payload (Export Booking):")
    print(json.dumps(payload, indent=4))

    response = post(url, headers, payload)
    assert response.status_code == 200

    response_json = response.json()

    print("\n📥 Response (Export Booking):")
    print(json.dumps(response_json, indent=4))

    # --- Essential Assertions Only ---
    assert response_json["Success"] is True
    assert response_json["Data"] is not None

    data = response_json["Data"]

    # Primary identity
    assert data["ID"] > 0

    # Business-critical fields
    assert data["BookingTypeID"] == payload["BookingTypeID"]
    assert data["SBNumber"] == payload["SBNumber"]
