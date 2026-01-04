import pytest
import requests
import random
import string
import json
from datetime import datetime, timedelta

BASE_URL = "http://172.16.23.54:9884/mnr/v1/"
LIST_ENDPOINT = "gas-tool"
CREATE_ENDPOINT = "gas-tool"


JWT_TOKEN = """<YOUR TOKEN HERE>"""

HEADERS = {
    "Content-Type": "application/json",
    "SiteID": "4",
    "Authorization": f"Bearer {JWT_TOKEN}"
}

# Globals shared between tests
created_desc = None
created_gas_tool_id = None


# =====================================================================
# Helper: Random Gas Tool Payload
# =====================================================================
def generate_payload():
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    control_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%dT%H:%M")
    purchase_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M")

    payload = {
        "id": 0,
        "description": f"GasTool-{suffix}",
        "nsseries": f"NS-{suffix}",
        "nPiece": f"N-{random.randint(10,99)}",
        "roleModel": random.choice(["ME", "NR", "GT", "RX"]),
        "loud": random.choice(["1", "2", "3", "4"]),
        "controlDate": control_date,
        "dateOfPurchase": purchase_date,
        "isActive": True,
        "crtByTokenID": 16,
        "mdByTokenID": 16
    }

    return payload


# =====================================================================
# 1️⃣ CREATE Gas Tool  (NO ID returned)
# =====================================================================


def test_create_gas_tool():
    global created_desc

    payload = generate_payload()

    print("\n📤 CREATE Payload:")
    print(json.dumps(payload, indent=4))

    response = requests.post(f"{BASE_URL}{CREATE_ENDPOINT}", headers=HEADERS, json=payload)
    assert response.status_code == 200, f"Create failed: {response.text}"

    # Save description to search later
    created_desc = payload["description"]

    print(f"\n✅ Created Gas Tool with Description: {created_desc}")


# =====================================================================
# 2️⃣ GET LIST → Extract ID from matching description
# =====================================================================


def test_get_and_extract_id():
    global created_desc, created_gas_tool_id

    assert created_desc is not None, "❌ No description saved from create"

    response = requests.get(f"{BASE_URL}{LIST_ENDPOINT}", headers=HEADERS)
    assert response.status_code == 200, f"List failed: {response.text}"

    data = response.json()
    assert isinstance(data, list), "❌ Expected list response"

    print("\n📋 Searching for created Gas Tool in list...")

    created_gas_tool_id = None

    for item in data:
        if item.get("Description") == created_desc:
            created_gas_tool_id = item.get("ID")
            break

    assert created_gas_tool_id is not None, f"❌ Gas Tool '{created_desc}' not found in list!"

    print(f"\n🎯 Found Gas Tool ID: {created_gas_tool_id} for Description: {created_desc}")


# =====================================================================
# 3️⃣ UPDATE Gas Tool
# =====================================================================

def test_update_gas_tool():
    global created_gas_tool_id, created_desc
    assert created_gas_tool_id, "❌ No ID found from list"

    updated_payload = {
        "ID": created_gas_tool_id,
        "Description": created_desc,
        "Nsseries": "NS-Updated",
        "NPiece": "N82",
        "RoleModel": "ME",
        "Loud": "4",
        "ControlDate": "2026-07-09T15:32:00",
        "DateOfPurchase": "2025-08-27T15:32:00",
        "IsActive": False,
        "crtByTokenID": 2102
    }

    print("\n📤 Update Payload:")
    print(json.dumps(updated_payload, indent=4))

    response = requests.put(f"{BASE_URL}{LIST_ENDPOINT}", headers=HEADERS, json=updated_payload)
    assert response.status_code == 200, f"Update failed: {response.text}"

    print(f"\n✅ Updated Gas Tool ID {created_gas_tool_id}")



