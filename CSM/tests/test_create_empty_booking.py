"""
Test Script:
------------
test_create_empty_booking.py

Test Case:
----------
test_create_empty_container_booking_success

Purpose:
--------
Validates successful creation of an Empty Container Booking.

How It Works:
-------------
- Uses shared fixture 'empty_booking_context' from conftest.py.
- Does NOT create booking again.
- Verifies key booking attributes returned by the API:
  - Booking ID (bkid)
  - Booking Number
  - Unique Number

Why This Test Exists:
--------------------
- Confirms that Empty Booking creation is successful.
- Acts as the parent validation test for downstream flows.
- Ensures data used by Sub-Booking and other flows is valid.



Test Case:
----------
test_create_empty_sub_booking_success

Purpose:
--------
Creates a Sub-Booking under an already created Empty Booking.

How It Works:
-------------
1. Retrieves parent booking details using 'empty_booking_context'.
2. Uses Booking ID (bkid) to create Sub-Booking via:
   /csm/v1/IECOSubBooking/SaveSubBooking
3. Validates:
   - Sub-Booking creation success
   - Correct linkage to parent booking (BKID)
   - Business-critical fields only

Why This Test Exists:
--------------------
- Validates parent-child relationship between Booking and Sub-Booking.
- Ensures Sub-Booking cannot exist without a valid Empty Booking.
- Forms the foundation for container allocation and gate operations.

"""

from payloads.empty_booking_payload import get_add_empty_container_payload
from payloads.empty_booking_payload import get_empty_sub_booking_payload
from utils.api_client import post
import json


def test_create_empty_container_booking_success(empty_booking_context):
    """
    Test Case 1:
    Validate Empty Booking creation
    """

    bkid = empty_booking_context["bkid"]
    booking_number = empty_booking_context["booking_number"]
    unique_no = empty_booking_context["unique_no"]

    assert bkid > 0
    assert booking_number
    assert unique_no


def test_create_empty_sub_booking_success(
    base_url, headers, empty_booking_context
):
    """
    Test Case 2:
    Create Sub-Booking inside the SAME Empty Booking
    """

    bkid = empty_booking_context["bkid"]

    sub_url = f"{base_url}/csm/v1/IECOSubBooking/SaveSubBooking"
    sub_payload = get_empty_sub_booking_payload(bkid)

    sub_response = post(sub_url, headers, sub_payload)
    assert sub_response.status_code == 200

    sub_json = sub_response.json()

    print("\n📥 Sub-Booking Response:")
    print(json.dumps(sub_json, indent=4))

    assert sub_json["Success"] is True
    assert sub_json["Data"] is not None

    sub_data = sub_json["Data"]

    # --- THIS IS THE CRITICAL PART ---
    sbkid = sub_data["ID"]          # capture Sub-Booking ID
    assert sbkid > 0

    # validate linkage
    assert str(sub_data["BKID"]) == str(bkid)

    # --- REUSE IT ---
    empty_booking_context["sbkid"] = sbkid





def test_add_empty_container_success(base_url, headers, empty_booking_context):
    """
    Test Case 3:
    Add ONE Empty Container under the created Empty Booking & Sub-Booking
    """

    # --- Required data from previous tests ---
    bkid = empty_booking_context["bkid"]
    booking_ref = empty_booking_context["booking_ref"]
    sbkid = empty_booking_context["sbkid"]

    # NOTE: This API uses a different base URL
    add_container_url = f"{base_url}/csm/v1/EmptyContainer/AddEmptyContainer"

    payload = get_add_empty_container_payload(
        bkid=bkid,
        booking_ref=booking_ref,
        sbkid=sbkid
    )

    print("\n📤 POST Payload (Add Empty Container):")
    print(json.dumps(payload, indent=4))

    response = post(add_container_url, headers, payload)
    assert response.status_code == 200

    response_json = response.json()

    print("\n📥 Response (Add Empty Container):")
    print(json.dumps(response_json, indent=4))

    # --- Essential Assertions Only ---
    assert response_json["Success"] is True
    assert response_json["Data"] is not None

    