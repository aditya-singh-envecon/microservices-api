
import json
from urllib import response
import pytest

from payloads.import_booking_payload import (
    get_import_booking_payload,
    get_import_booking_details_payload,
    get_import_booking_cargo_payload,
    get_import_booking_container_payload,
    get_import_cargo_container_mapping_payload,
    get_import_booking_boe_payload,
    get_import_booking_ooc_payload,
    get_import_work_order_payload
)

from utils.api_client import post


def test_create_import_booking_and_save_details_success(base_url, headers):
    """
    Test Scenario:
    --------------
    1. Create Import Booking
    2. Save Import Booking Details for the same booking

    Purpose:
    --------
    - Validates Import Booking creation
    - Ensures Import Booking Details reuse IGM/BL/Line values
    - Confirms correct linkage via BkID
    """

    # =====================================================
    # STEP 1: CREATE IMPORT BOOKING
    # =====================================================

    import_booking_url = (
        f"{base_url}/csm/v1/MCNCImportBooking/SaveMCNCBookingImport"
    )

    booking_payload, context = get_import_booking_payload()

    booking_response = post(import_booking_url, headers, booking_payload)
    assert booking_response.status_code == 200

    booking_json = booking_response.json()

    assert booking_json["Success"] is True
    assert booking_json["Data"] is not None

    bkid = booking_json["Data"]["ID"]
    assert bkid > 0

    # =====================================================
    # STEP 2: SAVE IMPORT BOOKING DETAILS
    # =====================================================

    import_booking_details_url = (
        f"{base_url}/csm/v1/MCNCBookingDetails/SaveImportBookingDetails"
    )

    details_payload = get_import_booking_details_payload(
        bkid=bkid,
        context=context
    )

    details_response = post(import_booking_details_url, headers, details_payload)
    assert details_response.status_code == 200

    details_json = details_response.json()

    assert details_json["Success"] is True
    assert details_json["Data"] is not None

    details_data = details_json["Data"]

    assert details_data["ID"] > 0
    assert details_data["BkID"] == bkid

    # Store for next test via pytest cache
    pytest.import_context = {
        "bkid": bkid,
        "context": context
    }

    print("\n✅ Import Booking is created and details added successfully.")


def test_add_import_booking_cargo_success(base_url, headers):
    """
    Test Scenario:
    --------------
    3. Add Cargo to the SAME Import Booking

    Dependency:
    -----------
    - Uses Import Booking created in previous test
    - Reuses LineNumber from booking context

    Purpose:
    --------
    - Validates cargo creation
    - Confirms cargo is linked to Import Booking
    """

    # =====================================================
    # FETCH CONTEXT FROM PREVIOUS TEST
    # =====================================================

    bkid = pytest.import_context["bkid"]
    context = pytest.import_context["context"]

    # =====================================================
    # STEP 3: ADD IMPORT BOOKING CARGO
    # =====================================================

    import_cargo_url = (
        f"{base_url}/csm/v1/MCNCImportBooking/SaveImportBookingCargo"
    )

    cargo_payload = get_import_booking_cargo_payload(
        bkid=bkid,
        context=context
    )

    print("\n📤 POST Payload (Import Booking Cargo):")
    print(json.dumps(cargo_payload, indent=4))

    cargo_response = post(import_cargo_url, headers, cargo_payload)
    assert cargo_response.status_code == 200

    cargo_json = cargo_response.json()

    print("\n📥 Response (Import Booking Cargo):")
    print(json.dumps(cargo_json, indent=4))

    # --- Essential Assertions ---
    assert cargo_json["Success"] is True
    assert cargo_json["Data"] is not None

    cargo_data = cargo_json["Data"]

    assert cargo_data["ID"] > 0
    assert cargo_data["BkID"] == bkid

    pytest.import_context["cargo_id"] = cargo_data["ID"]
    pytest.import_context["cargo_unique_no"] = cargo_data["UniqueNo"] 

    print("\n✅ Import Booking Cargo added successfully.")



def test_add_import_booking_container_success(base_url, headers):
    """
    Test Scenario:
    --------------
    Add Container to existing Import Booking
    """

    bkid = pytest.import_context["bkid"]

    container_url = (
        f"{base_url}/csm/v1/MCNCBookingContainer/SaveImportBookingContainer"
    )

    container_payload = get_import_booking_container_payload(bkid)

    response = post(container_url, headers, container_payload)
    assert response.status_code == 200

    response_json = response.json()

    assert response_json["Success"] is True
    assert response_json["Data"] is not None

    data = response_json["Data"]

    assert data["ID"] > 0
    assert data["BkID"] == bkid
    assert data["OperatorID"] == 16185

    pytest.import_context["container_id"] = data["ID"]
    pytest.import_context["container_no"] = data["ContainerNo"]

    print("\n✅ Import Booking Container added successfully.")





def test_map_import_cargo_container_success(base_url, headers):
    """
    Test Scenario:
    --------------
    4. Map Import Cargo with Import Container

    Dependency:
    -----------
    - Uses Cargo & Container created in previous tests

    Purpose:
    --------
    - Validates cargo-container mapping
    """

    # =====================================================
    # FETCH CONTEXT
    # =====================================================
    cargo_id = pytest.import_context["cargo_id"]
    container_id = pytest.import_context["container_id"]
    container_no = pytest.import_context["container_no"]

    # =====================================================
    # MAP CARGO ↔ CONTAINER
    # =====================================================
    map_url = (
        f"{base_url}/csm/v1/MCNCImportBooking/SaveMappedContainerPackages"
    )

    map_payload = get_import_cargo_container_mapping_payload(
        cargo_id=cargo_id,
        container_id=container_id,
        container_no=container_no
    )

    print("\n📤 POST Payload (Cargo-Container Mapping):")
    print(json.dumps(map_payload, indent=4))

    map_response = post(map_url, headers, map_payload)
    assert map_response.status_code == 200

    map_json = map_response.json()

    print("\n📥 Response (Cargo-Container Mapping):")
    print(json.dumps(map_json, indent=4))

    # --- Essential Assertions ---
    assert map_json["Success"] is True
    assert map_json["Data"] is not None
    assert map_json["Data"]["ID"] == cargo_id

    print("\n✅ Import Cargo mapped with Container successfully.")




def test_map_import_cargo_container_success(base_url, headers):
    """
    Test Scenario:
    --------------
    4. Map Import Cargo with Import Container

    Dependency:
    -----------
    - Uses Cargo & Container created in previous tests

    Purpose:
    --------
    - Validates cargo-container mapping
    """

    # =====================================================
    # FETCH CONTEXT
    # =====================================================
    cargo_id = pytest.import_context["cargo_id"]
    container_id = pytest.import_context["container_id"]
    container_no = pytest.import_context["container_no"]

    # =====================================================
    # MAP CARGO ↔ CONTAINER
    # =====================================================
    map_url = (
        f"{base_url}/csm/v1/MCNCImportBooking/SaveMappedContainerPackages"
    )

    map_payload = get_import_cargo_container_mapping_payload(
        cargo_id=cargo_id,
        container_id=container_id,
        container_no=container_no
    )

    print("\n📤 POST Payload (Cargo-Container Mapping):")
    print(json.dumps(map_payload, indent=4))

    map_response = post(map_url, headers, map_payload)
    assert map_response.status_code == 200

    map_json = map_response.json()

    print("\n📥 Response (Cargo-Container Mapping):")
    print(json.dumps(map_json, indent=4))

    # --- Essential Assertions ---
    assert map_json["Success"] is True
    assert map_json["Data"] is not None
    assert map_json["Data"]["ID"] == cargo_id

    print("\n✅ Import Cargo mapped with Container successfully.")




def test_update_import_booking_boe_success(base_url, headers):

    bkid = pytest.import_context["bkid"]
    cargo_id = pytest.import_context["cargo_id"]
    cargo_unique_no = pytest.import_context["cargo_unique_no"]
    line_no = pytest.import_context["context"]["line_no"]

    boe_url = f"{base_url}/csm/v1/MCNCImportBooking/SaveBoE"

    payload = get_import_booking_boe_payload(
        bkid=bkid,
        cargo_id=cargo_id,
        cargo_unique_no=cargo_unique_no,
        line_no=line_no
    )

    response = post(boe_url, headers, payload)
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["Success"] is True
    assert response_json["Data"] is not None

# ✅ DEFINE boe_data FIRST

    boe_data = response_json["Data"]

# ✅ STORE CONTEXT FOR NEXT STEP (OOC)

    pytest.import_context["cargo_id"] = boe_data["ID"]
    pytest.import_context["be_date"] = boe_data["BEDate"]

# Optional sanity checks
    assert boe_data["ID"] == cargo_id
    assert boe_data["BkID"] == bkid



def test_update_import_booking_ooc_success(base_url, headers):
    """
    Test Scenario:
    --------------
    Update OOC (Custom Clearance) for Import Cargo

    Dependency:
    -----------
    - Uses Cargo ID and BEDate from BOE update test
    """

    # =====================================================
    # FETCH CONTEXT FROM BOE TEST
    # =====================================================
    cargo_id = pytest.import_context["cargo_id"]
    be_date = pytest.import_context["be_date"]

    # =====================================================
    # STEP: UPDATE OOC
    # =====================================================
    ooc_url = (
        f"{base_url}/csm/v1/MCNCImportBooking/SaveImportBookingCargoOOC"
    )

    payload = get_import_booking_ooc_payload(
        cargo_id=cargo_id,
        be_date=be_date
    )

    print("\n📤 POST Payload (Import Cargo OOC):")
    print(json.dumps(payload, indent=4))

    response = post(ooc_url, headers, payload)
    assert response.status_code == 200

    response_json = response.json()

    print("\n📥 Response (Import Cargo OOC):")
    print(json.dumps(response_json, indent=4))

    # =====================================================
    # ASSERTIONS
    # =====================================================
    assert response_json["Success"] is True
    assert response_json["Data"] is not None

    data = response_json["Data"]

    assert data["ID"] == cargo_id
    assert data["IsOOC"] is True

    print("\n✅ Import Cargo OOC updated successfully.")


def test_create_import_work_order_success(base_url, headers):
    """
    Test Scenario:
    --------------
    Create Work Order for Import Booking Container
    """

    # =====================================================
    # FETCH CONTEXT
    # =====================================================
    import_context = pytest.import_context

    work_order_url = (
        f"{base_url}/csm/v1/WOWUnassignedContainers/SaveWorkOrder"
    )

    payload = get_import_work_order_payload(import_context)

    print("\n📤 POST Payload (Import Work Order):")
    print(json.dumps(payload, indent=4))

    response = post(work_order_url, headers, payload)
    assert response.status_code == 200

    response_json = response.json()

    print("\n📥 Response (Import Work Order):")
    print(json.dumps(response_json, indent=4))

    # =====================================================
    # ASSERTIONS
    # =====================================================
    assert response_json["Success"] is True
    assert response_json["Data"] is not None

    work_order_data = response_json["Data"]

    assert work_order_data["ID"] > 0
    assert work_order_data["ContainerNo"] == import_context["container_no"]
    assert work_order_data["BookingNumber"] == import_context["booking_no"]

    print("\n✅ Import Work Order created successfully.")    


