import json
import pytest
from payloads.export_booking_payload import (
    get_export_booking_payload,
    get_export_booking_details_payload,
    get_export_cargo_payload,
    get_export_container_payload,
    get_export_cargo_container_mapping_payload,
    get_export_job_order_payload
)
from utils.api_client import post
import json
import pytest
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

    pytest.export_context = {
        "bkid": data["ID"],
        "sb_number": data["SBNumber"],
        "sb_date": data["SBDate"],

        "booking_type_id": data["BookingTypeID"],
        "container_cycle_id": data["ContainerCycleID"],
        "cargo_cycle_id": data["CargoCycleID"],

        "exporter_id": data["ExporterID"],
        "cha_id": data["CHAID"],
        "cha_code": data["CHACode"],

        "port_of_discharge": data["PortOfDischarge"]
    }

    # Primary identity
    assert data["ID"] > 0

    # Business-critical fields
    assert data["BookingTypeID"] == payload["BookingTypeID"]
    assert data["SBNumber"] == payload["SBNumber"]


def test_save_export_booking_details_success(base_url, headers):
    ctx = pytest.export_context

    url = (
        f"{base_url}/csm/v1/XCNCBookingDetails/SaveExportBookingDetails"
    )

    payload = get_export_booking_details_payload(ctx)

    response = post(url, headers, payload)
    assert response.status_code == 200

    response_json = response.json()

    assert response_json["Success"] is True
    assert response_json["Data"] is not None

    data = response_json["Data"]

    # --- Business sanity checks ---
    assert data["BkID"] == ctx["bkid"]
    assert data["SBNumber"] == ctx["sb_number"]
    assert data["OperatorID"] == payload["OperatorID"]

    # 🔒 Store for next steps (cargo/container)
    pytest.export_context.update({
        # Booking Details identity
        "booking_details_id": data["ID"],
        "booking_details_unique_no": data["UniqueNo"],

        # Cross-check / linkage
        "bkid": data["BkID"],
        "sb_number": data["SBNumber"],
        "sb_date": data["SBDate"],

        # Reused downstream
        "ach_id": data["ACHID"],
        "operator_id": data["OperatorID"]
    })


def test_create_export_booking_cargo_success(base_url, headers):
    """
    Test Scenario:
    --------------
    Create Export Booking Cargo (Shipping Bill Sub-Line)

    Purpose:
    --------
    - Attaches cargo to existing Export Booking
    - Validates SB and Booking linkage
    - Stores Cargo identifiers for downstream flows
    """

    # =====================================================
    # FETCH CONTEXT
    # =====================================================
    ctx = pytest.export_context

    url = (
        f"{base_url}/csm/v1/XCNCBookingCargo/saveExportBookingCargo"
    )

    payload = get_export_cargo_payload(ctx)

    print("\n📤 POST Payload (Export Booking Cargo):")
    print(json.dumps(payload, indent=4))

    # =====================================================
    # API CALL
    # =====================================================
    response = post(url, headers, payload)
    assert response.status_code == 200

    response_json = response.json()

    print("\n📥 Response (Export Booking Cargo):")
    print(json.dumps(response_json, indent=4))

    # =====================================================
    # ASSERTIONS (BUSINESS-CRITICAL ONLY)
    # =====================================================
    assert response_json["Success"] is True
    assert response_json["Data"] is not None

    data = response_json["Data"]

    # Identity & linkage
    assert data["BkID"] == ctx["bkid"]

    # Cargo existence
    assert data["ID"] > 0

    # =====================================================
    # STORE FOR NEXT STEPS
    # =====================================================
    pytest.export_context.update({
        "cargo_id": data["ID"],
        "cargo_unique_no": data.get("UniqueNo")
    })

    print("\n✅ Export Booking Cargo created successfully.")


def test_create_export_booking_container_success(base_url, headers):
    """
    Test Scenario:
    --------------
    Create Export Booking Container

    Purpose:
    --------
    - Attaches a container to an existing Export Booking
    - Validates persistence and correct linkage
    - Stores container identifiers for downstream flows
    """

    # =====================================================
    # FETCH CONTEXT
    # =====================================================
    ctx = pytest.export_context

    url = (
        f"{base_url}/csm/v1/XCNCBookingContainer/SaveExportBookingContainer"
    )

    payload = get_export_container_payload(ctx)

    print("\n📤 POST Payload (Export Booking Container):")
    print(json.dumps(payload, indent=4))

    # =====================================================
    # API CALL
    # =====================================================
    response = post(url, headers, payload)
    assert response.status_code == 200

    response_json = response.json()

    print("\n📥 Response (Export Booking Container):")
    print(json.dumps(response_json, indent=4))

    # =====================================================
    # ASSERTIONS (MINIMAL & STABLE)
    # =====================================================
    assert response_json["Success"] is True
    assert response_json["Data"] is not None

    data = response_json["Data"]

    # --- Persistence ---
    assert data["ID"] > 0
    assert data["UniqueNo"] is not None

    # --- Identity & linkage ---
    assert data["ContainerNo"] == payload["ContainerNo"]
    assert data["BkID"] == ctx["bkid"]

    # =====================================================
    # STORE FOR NEXT STEPS
    # =====================================================
    pytest.export_context.update({
        "container_id": data["ID"],
        "container_unique_no": data["UniqueNo"],
        "container_no": data["ContainerNo"],
    })

    print("\n✅ Export Booking Container created successfully.")


def test_save_export_cargo_container_mapping_success(base_url, headers):
    """
    Test Scenario:
    --------------
    Map Export Cargo to Export Container

    Purpose:
    --------
    - Links existing export cargo with an existing export container
    - Validates successful mapping
    - Does NOT create new entities
    """

    # =====================================================
    # FETCH CONTEXT
    # =====================================================
    ctx = pytest.export_context

    url = (
        f"{base_url}/csm/v1/XCNCBookingCargo/SaveCargoMapping"
    )

    payload = get_export_cargo_container_mapping_payload(ctx)

    print("\n📤 POST Payload (Export Cargo–Container Mapping):")
    print(json.dumps(payload, indent=4))

    # =====================================================
    # API CALL
    # =====================================================
    response = post(url, headers, payload)
    assert response.status_code == 200

    response_json = response.json()

    print("\n📥 Response (Export Cargo–Container Mapping):")
    print(json.dumps(response_json, indent=4))

    # =====================================================
    # ASSERTIONS (MINIMAL & STABLE)
    # =====================================================
    assert response_json["Success"] is True
    assert response_json.get("Data") is not None

    data = response_json["Data"]

    # --- Linkage verification ---
    # Most implementations echo CargoID back
    if isinstance(data, dict) and "CargoID" in data:
        assert data["CargoID"] == ctx["cargo_id"]

    # Some implementations return mapped rows list
    if isinstance(data, list) and data:
        row = data[0]
        assert row.get("ContainerID") == ctx["container_id"]
        assert row.get("CargoID") == ctx["cargo_id"]

    print("\n✅ Export Cargo successfully mapped to Container.")


def test_create_export_job_order_success(base_url, headers):
    """
    Test Scenario:
    --------------
    Create Job Order for Export Booking (Legacy-compatible)

    Purpose:
    --------
    - Creates Job Order using backend-required legacy fields
    - Validates successful persistence
    - Stores Job Order identifiers for downstream flows
    """

    # =====================================================
    # FETCH CONTEXT
    # =====================================================
    ctx = pytest.export_context

    url = f"{base_url}/csm/v1/JobOrder/SaveJobOrder"

    payload = get_export_job_order_payload(ctx)

    print("\n📤 POST Payload (Export Job Order):")
    print(json.dumps(payload, indent=4))

    # =====================================================
    # API CALL
    # =====================================================
    response = post(url, headers, payload)

    print("\n📥 Status Code:", response.status_code)
    print("\n📥 Raw Response:")
    print(response.text)

    assert response.status_code == 200

    response_json = response.json()

    print("\n📥 Parsed Response (Export Job Order):")
    print(json.dumps(response_json, indent=4))

    # =====================================================
    # ASSERTIONS (MINIMAL & STABLE)
    # =====================================================
    assert response_json["Success"] is True
    assert response_json["Data"] is not None

    data = response_json["Data"]

    # --- Identity ---
    assert data["ID"] > 0
    assert data["UniqueNo"] is not None

    # --- Booking linkage ---
    assert data["BkID"] == ctx["bkid"]

    # --- Container linkage ---
    assert data["JODContainerID"] == ctx["container_id"]

    # --- SB linkage ---
    assert data["SBNumber"] == ctx["sb_number"]

    # =====================================================
    # STORE FOR NEXT STEPS
    # =====================================================
    pytest.export_context.update({
        "job_order_id": data["ID"],
        "job_order_unique_no": data["UniqueNo"]
    })

    print("\n✅ Export Job Order created successfully.")
