import json
from payloads.gate_payloads import get_gate_container_list_payload
from payloads.gate_payloads import get_gate_save_details_payload
from utils.api_client import post

def test_gate_container_list_extract_adiu_container(
    gate_base_url, gate_headers
):
    """
    Test Case:
    ----------
    1. Fetch Gate Container List
    2. Extract ONE container whose number starts with 'ADIU'
    3. Prepare it for Gate Details save
    """

    url = f"{gate_base_url}/Container/container-list"
    payload = get_gate_container_list_payload()

    print("\n📤 POST Payload (Gate Container List):")
    print(json.dumps(payload, indent=4))

    response = post(url, gate_headers, payload)
    assert response.status_code == 200

    response_json = response.json()

    print("\n📥 Full Response (Gate Container List):")
    print(json.dumps(response_json, indent=4))

    # --- Basic validations ---
    assert isinstance(response_json, list)
    assert len(response_json) > 0

    # --- Extract ADIU container ---
    adiu_container = next(
        (
            row for row in response_json
            if row.get("containerNo", "").startswith("ADIU")
        ),
        None
    )

    assert adiu_container is not None, "No ADIU container found in Gate list"

    print("\n✅ Extracted ADIU Container (to be used for Gate Details):")
    print(json.dumps(adiu_container, indent=4))

    # --- Minimal sanity assertions on extracted container ---
    assert adiu_container["containerNo"].startswith("ADIU")
    assert adiu_container["isActive"] is True
    assert adiu_container["gateOperation"] in ["Gate In", "Gate Out"]




def test_gate_save_details_success(
    gate_base_url,
    gate_headers,
    adiu_container_context
):
    """
    Test Case:
    ----------
    Save Gate-In details for an ADIU container.

    Flow:
    -----
    1. Fetch ADIU container from Gate Container List (fixture)
    2. Build FULL Save Details payload using context + dynamic values
    3. POST to Update-Transportdetails
    4. Validate successful save
    """

    url = f"{gate_base_url}/Container/Update-Transportdetails"

    payload = get_gate_save_details_payload(adiu_container_context)

    print("\n📤 POST Payload (Gate Save Details):")
    print(json.dumps(payload, indent=4))

    response = post(url, gate_headers, payload)

    print("\n📥 Response (Gate Save Details):")
    try:
        print(json.dumps(response.json(), indent=4))
    except Exception:
        print(response.text)

    # ---------------- ASSERTIONS ----------------

    assert response.status_code == 200, f"Unexpected status: {response.text}"

    response_json = response.json()

    # Gate APIs return Success flag
    assert response_json.get("Success") is True

    # Optional but useful sanity check
    assert response_json.get("Message") in (
        None,
        "",
        "Data saved successfully."
    )