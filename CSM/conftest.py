"""
Purpose:
--------
Provides shared pytest fixtures used across API automation tests.

Key Responsibilities:
---------------------
1. Defines reusable fixtures such as:
   - base_url: Base API URL for all requests
   - headers: Common request headers (Content-Type, Authorization, etc.)

2. Creates Empty Booking ONCE per module using:
   /csm/v1/IECOBooking/SaveEmptyBooking

3. Extracts and shares only relevant booking data:
   - bkid (Booking ID)
   - booking_number
   - unique_no

Usage:
------
- Acts as the single source of truth for Empty Booking creation.
- Ensures dependent tests (Sub-Booking, downstream flows) use the same booking.
- Prevents duplicate booking creation and maintains test consistency.

Scope:
------
Fixture scope is set to 'module' to guarantee:
- Booking is created once
- Data is reused across multiple test functions safely
"""



import random
from payloads.empty_booking_payload import get_empty_booking_payload
import json
from payloads.gate_payloads import get_gate_container_list_payload
import pytest
from utils.api_client import post
from payloads.import_booking_payload import *

@pytest.fixture(scope="session")
def base_url():
    return "https://prepaccsmapi.logstarerp.com"

@pytest.fixture(scope="session")
def headers():
    return {
        "Content-Type": "application/json"
        # Add Authorization header if required
        # "Authorization": "Bearer <token>"
    }




@pytest.fixture(scope="module")
def empty_booking_context(base_url, headers):
    """
    Creates Empty Booking once and shares required data
    """

    # Generate booking ref HERE
    booking_ref = f"ADI{random.randint(1000000, 9999999)}"

    payload = get_empty_booking_payload(booking_ref)

    url = f"{base_url}/csm/v1/IECOBooking/SaveEmptyBooking"
    response = post(url, headers, payload)
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["Success"] is True

    data = response_json["Data"]

    return {
        "bkid": data["ID"],
        "booking_number": data["BookingNumber"],
        "unique_no": data["UniqueNo"],
        "booking_ref": booking_ref
    }


@pytest.fixture(scope="session")
def gate_base_url():
    return "https://prepacgateapi.logstarerp.com"


@pytest.fixture(scope="session")
def gate_headers():
    return {
        "Content-Type": "application/json",
        "SiteId": "1" 
    }





@pytest.fixture(scope="module")
def adiu_container_context(gate_base_url, gate_headers):
    url = f"{gate_base_url}/Container/container-list"
    payload = get_gate_container_list_payload()

    response = post(url, gate_headers, payload)
    assert response.status_code == 200

    container_list = response.json()
    assert isinstance(container_list, list)
    assert container_list

    adiu_containers = [
        row for row in container_list
        if row.get("containerNo", "").startswith("ADIU")
    ]

    assert adiu_containers, "No ADIU container found"

    c = adiu_containers[0]

    return {
        # Required identifiers
        "id": c.get("id"),
        "coid": c.get("coid"),
        "container_no": c.get("containerNo"),
        "bkno": c.get("bkno"),
        "unique_no": c.get("uniqueNo"),

        # Gate execution
        "tmod_pass_id": c.get("tModPassID"),
        "tmod_code": c.get("tmodCode"),
        "transport_activity": c.get("transportActivity"),
        "gate_operation": c.get("gateOperation"),

        # Job linkage
        "job_order_id": c.get("jobOrderID"),
        "jodid": c.get("jodid"),
        "jod_act_id": c.get("jodActID"),

        # Container attributes
        "operator_id": c.get("operatorID"),
        "co_size_type_id": c.get("coSizeTypeID"),
        "iso_size_type": c.get("isoSizeType"),
        "tare_weight": c.get("tareWeight"),
    }


