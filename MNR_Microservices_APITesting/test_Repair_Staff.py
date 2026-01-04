import requests
import json
import random
import string
from datetime import datetime

BASE_URL = "http://172.16.23.54:9884"
HEADERS = {
    "Content-Type": "application/json",
    "SiteID": "04"
}

LIST_ENDPOINT = "/mnr/v1/repair-staff/list"
CRUD_ENDPOINT = "/mnr/v1/repair-staff"

created_staff_code = None
created_staff_name = None
created_staff_id = None


def test_create_repair_staff():
    global created_staff_code, created_staff_name

    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    created_staff_code = f"RS{suffix}"
    created_staff_name = f"Repair Staff {suffix}"

    payload = {
    "id": 0,
    "code": created_staff_code,
    "name": created_staff_name,
    "isActive": True,
    "siteID": 4,
    "crtByTokenID": 16,
    "categoryId": "1",
    "skillLevel": random.choice(["1", "2", "3", "4"])
}

    print("\n📤 CREATE PAYLOAD:")
    print(json.dumps(payload, indent=4))

    response = requests.post(f"{BASE_URL}{CRUD_ENDPOINT}", json=payload, headers=HEADERS)
    assert response.status_code == 200, f"Create failed: {response.text}"

    print({response.text})
    print("\n✅ Created Repair Staff (ID NOT RETURNED BY API)")
    print(f"Code: {created_staff_code}, Name: {created_staff_name}")




def test_get_repair_staff_id():
    global created_staff_id, created_staff_code

    response = requests.get(f"{BASE_URL}{LIST_ENDPOINT}", headers=HEADERS)
    assert response.status_code == 200

    data = response.json()

    # Search for our created record
    for staff in data:
        if staff.get("Code") == created_staff_code:
            created_staff_id = staff.get("Id")
            break

    assert created_staff_id is not None, "❌ Could not find ID in list for created staff"

    print(f"\n🎯 Found Staff ID: {created_staff_id} for Code: {created_staff_code}")




def test_update_repair_staff():
    global created_staff_id, created_staff_code, created_staff_name

    assert created_staff_id, "❌ No ID from previous test"

    new_name = created_staff_name + " Updated"

    payload = {
        "Id": created_staff_id,
        "CategoryId": "1",
        "SiteId": 4,
        "Code": created_staff_code,
        "Name": new_name,
        "SkillLevel": random.choice(["1", "2", "3", "4"]),
        "IsActive": True,
        "crtByTokenID": 16,
        "mdByTokenID": 16
    }

    print("\n📤 UPDATE PAYLOAD:")
    print(json.dumps(payload, indent=4))

    response = requests.put(f"{BASE_URL}{CRUD_ENDPOINT}", json=payload, headers=HEADERS)
    assert response.status_code == 200, f"Update failed: {response.text}"

    print("\n✅ Updated Staff:", created_staff_id)




