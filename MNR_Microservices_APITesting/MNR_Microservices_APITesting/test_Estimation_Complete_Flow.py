import requests
import json
import uuid

import os
import pytest
from datetime import datetime, timedelta

# ============================
#  BASE CONFIG
# ============================

BASE_URL = "http://172.16.23.54:9884"

LIST_ENDPOINT = "/mnr/v1/estimate-creation/pending-estimates"
ENDPOINT = "/mnr/v1/estimate-creation/save-estimatesa"
RP_ENDPOINT = "/mnr/v1/estimate-creation/estimate"
IN_LIST_ENDPOINT = "/mnr/v1/estimate-creation/view-pending-estimation-detail"
APPROVAL_ENDPOINT = "/mnr/v1/pending-estimate-approval/status"
ASSIGN_STAFF_ENDPOINT = "/mnr/v1/pending-estimate-approval/assign-job-order-to-staff"
JOB_ORDER_ENDPOINT = "/mnr/v1/pending-job-order-completion"


JWT_TOKEN = """i5VBlxyIg7rBjIDRo19FLwp6n9aX86GsdaAzMv19q6Y1N5_D_f1d6aSZpqplOyDHbT_Eir0MQvb-lWCeqH9N2mBJpkLDI6_y28vwZDon4aWL5J4B6XF44osJbm1sy7i5tLFaScVZ-9A0pUs0SDckV9X2BEmb9UrhbNu2qQc2SIbsOjgumt58xYpglrIwTdat3uy94GIIRl63GiF95ZceZpejcKwScav5A"""

headers = {
    "Authorization": f"Bearer {JWT_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "SiteID": "04"
}



created_container_no = None
created_estimate_id = None
created_estimate_no = None


# ============================
#  BASE PAYLOAD TEMPLATE (METHOD 1)
# ============================

BASE_PAYLOAD = {
    "ACEPNo": "",
    "CSCPlateNo": "",
    "ContPayLoad": 0,
    "ContTareWt": 0,
    "ContainerNo": "",
    "CrtBy": "",
    "DamageId": "932",
    "DriverLSCNo": "",
    "DriverName": "",
    "EIRNo": "",
    "EstimateType": "X",
    "GeoId": 4,
    "MFgCode": "0",
    "ManfMonthYr": "",
    "MfgName": "0",
    "OPSSizeType": "2190",
    "OperatorId": 1,
    "PhysicalInFlw": "",
    "QualityId": "943",
    "SzTypeId": "2349",
    "TranspName": "",
    "TruckNo": ""
}


# ============================
#  FUNCTION TO GENERATE DYNAMIC PAYLOAD
# ============================

def get_dynamic_payload(container_no):
    payload = BASE_PAYLOAD.copy()

    payload["ContainerNo"] = container_no
    payload["PhysicalInFlw"] = datetime.now().strftime("%Y-%m-%dT%H:%M")

    return payload


# ============================
#  TEST 1 — External Estimation
# ============================

def test_external_estimation_creation():
    global container_no, created_container_no

    container_no = "APTU" + str(uuid.uuid4().int)[:7]
    created_container_no = container_no   # store for next test

    payload = get_dynamic_payload(container_no)
    url = f"{BASE_URL}{ENDPOINT}"

    print("\n📤 POST Payload:")
    print(json.dumps(payload, indent=4))
    
    response = requests.post(url, headers=headers, json=payload)

    try:
        data = response.json()
    except:
        data = response.text

    assert response.status_code in [200, 201], f"Expected 200/201, got {response.status_code}, response: {data}"

    print(" Used ContainerNo:", container_no)
    print(" Server Response:", data)




def test_pending_estimates_list():
    global created_container_no, created_estimate_id

    url = f"{BASE_URL}{LIST_ENDPOINT}"
    response = requests.get(url, headers=headers)

    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"

    try:
        raw = response.json()
        data = json.loads(raw) if isinstance(raw, str) else raw
    except Exception as e:
        assert False, f"JSON parsing failed: {e}\nRaw response: {response.text}"

    assert isinstance(data, list), "API did not return a list"

    print(f"\n✅ Total Pending Estimates: {len(data)}")

    # Search for the container created in test 1
    matched = None
    for item in data:
        if item.get("ContainerNo") == created_container_no:
            matched = item
            break

    assert matched is not None, f"❌ Container {created_container_no} not found in pending list"

    created_estimate_id = matched.get("ID") or matched.get("EstimateID")

    print(f"\n🎯 Found Matching Entry!")
    print(f"Container: {created_container_no}")
    print(f"Estimate ID: {created_estimate_id}")




# def test_fetch_estimate_detail_by_id():
#     global created_estimate_id

#     assert created_estimate_id is not None, "❌ No Estimate ID stored from previous test"

#     url = f"{BASE_URL}{IN_LIST_ENDPOINT}"

#     # ---- SPECIAL HEADERS FOR ONLY THIS TEST ----
#     detail_headers = {
#         "Authorization": headers["Authorization"],
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#         "SiteID": "04",
#         "EstimateID": str(created_estimate_id),
#         "IsStandAlone": "true"
#     }

#     response = requests.get(url, headers=detail_headers)

#     assert response.status_code == 200, f"❌ Expected 200, got {response.status_code}"

#     try:
#         raw = response.json()
#         data = json.loads(raw) if isinstance(raw, str) else raw
#     except:
#         assert False, f"JSON parse error: {response.text}"

#     assert isinstance(data, list), "❌ Response is not a list"
#     assert len(data) == 1, f"❌ Expected 1 record but got {len(data)}"

#     detail = data[0]

#     print("\n🎯 Single Estimation Detail Returned:")
#     print(json.dumps(detail, indent=4))

#     assert detail.get("ID") == created_estimate_id, \
#         f"❌ Expected ID {created_estimate_id}, got {detail.get('ID')}"

#     print("\n✅ Successfully fetched detail using dedicated headers!")

def test_fetch_estimate_detail_by_id():
    global created_estimate_id, created_estimate_no, created_container_no

    url = f"{BASE_URL}{IN_LIST_ENDPOINT}"

    detail_headers = {
        "Authorization": headers["Authorization"],
        "Content-Type": "application/json",
        "Accept": "application/json",
        "SiteID": "04",
        "EstimateID": str(created_estimate_id),
        "IsStandAlone": "true"
    }

    response = requests.get(url, headers=detail_headers)
    raw = response.json()
    data = json.loads(raw) if isinstance(raw, str) else raw

    detail = data[0]

    created_estimate_no = detail.get("EstimateNo")   # ⭐ STORE IT HERE

    print("Fetched Estimate No:", created_estimate_no)




def test_submit_repair_completion():
    global created_estimate_id, created_estimate_no

    assert created_estimate_id is not None, "❌ No EstimateID found from previous tests"
    assert created_estimate_no is not None, "❌ No EstimateNo found from detail API"

    url = f"{BASE_URL}{RP_ENDPOINT}"

    # Build the repair POST payload
    payload = {
        "estimateId": created_estimate_id,
        "estimateDoneBy": "7",
        "CompleteUpdate": "U",
        "ESTSTATUSTYPE": "A",
        "dmCurrencyId": 34,
        "Comments": "",
        "EstimateNo": created_estimate_no,
        "CrtBy": "2102",
        "PendingEstimationCompletion": [
            {
                "EstimateID": created_estimate_id,
                "RepairSetItemId": 7246,
                "RepairModeCode": "03-1111",
                "RepairModeCodeDesc": "Roof Panel - Patch - 150x212x1.6 mm (or 2.0 mm for first panel)",
                "LocationCode": "LT5N",
                "CompCode": "RBS",
                "RP1": "BT - Bent",
                "RP2": "AJ - Adjust",
                "Height": None,
                "Width": None,
                "Length": None,
                "Qty": 1,
                "Max": 8,
                "Parts": [
                    {"PartNo": "", "Qty": 0, "PartUOMID": 0},
                    {"PartNo": "", "Qty": 0, "PartUOMID": 0},
                    {"PartNo": "", "Qty": 0, "PartUOMID": 0},
                    {"PartNo": "", "Qty": 0, "PartUOMID": 0},
                    {"PartNo": "", "Qty": 0, "PartUOMID": 0}
                ],
                "Responsible": "O",
                "MaterialRate": 8.39,
                "LabourHrs": 0.8,
                "LabourRate": 26.01,
                "LabourValue": 20.808,
                "MaterialValue": 8.39,
                "TotalValue": 29.198
            }
        ]
    }

    print("\n📤 POST Payload:")
    print(json.dumps(payload, indent=4))

    response = requests.post(url, headers=headers, json=payload)

    try:
        data = response.json()
    except:
        data = response.text

    print("\n📥 Server Response:")
    print(json.dumps(data, indent=4) if isinstance(data, dict) else data)

    assert response.status_code in [200, 201], \
        f"❌ Expected 200/201, got {response.status_code}"



def post_estimate_update(complete_update_type):
    global created_estimate_id, created_estimate_no

    assert created_estimate_id is not None, "❌ No EstimateID from previous tests"
    assert created_estimate_no is not None, "❌ No EstimateNo from previous tests"

    url = f"{BASE_URL}{RP_ENDPOINT}"

    payload = {
        "estimateId": created_estimate_id,
        "estimateDoneBy": "7",
        "CompleteUpdate": complete_update_type,   # <-- U or C here
        "ESTSTATUSTYPE": "A",
        "dmCurrencyId": 34,
        "Comments": "",
        "EstimateNo": created_estimate_no,
        "CrtBy": "2102",
        "PendingEstimationCompletion": [
            {
                "EstimateID": created_estimate_id,
                "RepairSetItemId": 7246,
                "RepairModeCode": "03-1111",
                "RepairModeCodeDesc": "Roof Panel - Patch - 150x212x1.6 mm (or 2.0 mm for first panel)",
                "LocationCode": "LT5N",
                "CompCode": "RBS",
                "RP1": "BT - Bent",
                "RP2": "AJ - Adjust",
                "Height": None,
                "Width": None,
                "Length": None,
                "Qty": 1,
                "Max": 8,
                "Parts": [
                    {"PartNo": "", "Qty": 0, "PartUOMID": 0},
                    {"PartNo": "", "Qty": 0, "PartUOMID": 0},
                    {"PartNo": "", "Qty": 0, "PartUOMID": 0},
                    {"PartNo": "", "Qty": 0, "PartUOMID": 0},
                    {"PartNo": "", "Qty": 0, "PartUOMID": 0}
                ],
                "Responsible": "O",
                "MaterialRate": 8.39,
                "LabourHrs": 0.8,
                "LabourRate": 26.01,
                "LabourValue": 20.808,
                "MaterialValue": 8.39,
                "TotalValue": 29.198
            }
        ]
    }

    print(f"\n📤 Sending Estimate Update ({complete_update_type})")
    print(json.dumps(payload, indent=4))

    response = requests.post(url, headers=headers, json=payload)

    try:
        data = response.json()
    except:
        data = response.text

    print("\n📥 Server Response:")
    print(data)

    assert response.status_code in [200, 201], \
        f"❌ Expected 200/201, got {response.status_code}"

    return data


def test_save_estimate():
    post_estimate_update("U")
    print("\n✅ Save (U) successful")


def test_submit_estimate():
    post_estimate_update("C")
    print("\n✅ Submit (C) successful")


def test_approve_estimate():
    global created_estimate_id, created_container_no

    assert created_estimate_id is not None, "❌ No EstimateID found from previous tests"
    assert created_container_no is not None, "❌ No container number found from detail"

    url = f"{BASE_URL}{APPROVAL_ENDPOINT}"

    payload = {
        "estimateId": str(created_estimate_id),
        "containerNo": created_container_no,
        "estimateStatus": "D",   # D = Done (for approval stage)
        "flag": "A",             # A = Approve
        "siteID": 4,
        "isActive": True,
        "approvedBy": "",
        "CrtBy": 16
    }

    print("\n📤 Sending Approval Request:")
    print(json.dumps(payload, indent=4))

    response = requests.post(url, headers=headers, json=payload)

    try:
        data = response.json()
    except:
        data = response.text

    print("\n📥 Server Approval Response:")
    print(data)

    assert response.status_code in [200, 201], \
        f"❌ Approval failed: expected 200/201 but got {response.status_code}"

    print("\n✅ Estimate Approved Successfully!")



def test_assign_staff_to_estimate():
    global created_estimate_id

    assert created_estimate_id is not None, "❌ No EstimateID available from previous tests"

    url = f"{BASE_URL}{ASSIGN_STAFF_ENDPOINT}"

    payload = {
        "GeoId": 4,
        "EstimateID": str(created_estimate_id),
        "StaffId": 10,   # change if needed
        "CrtBy": 16
    }

    print("\n📤 Assigning Staff for Estimate:")
    print(json.dumps(payload, indent=4))

    response = requests.post(url, headers=headers, json=payload)

    try:
        data = response.json()
    except:
        data = response.text

    print("\n📥 Response From Staff Assignment:")
    print(json.dumps(data, indent=4) if isinstance(data, dict) else data)

    assert response.status_code in [200, 201], \
        f"❌ Expected 200/201 but got {response.status_code}"

    print("\n✅ Staff Assigned Successfully!")


created_joborder_id = None
created_joborder_no = None

def test_fetch_job_order():
    global created_estimate_id, created_joborder_id, created_joborder_no

    url = f"{BASE_URL}/mnr/v1/pending-job-order-completion"

    jo_headers = {
        "Authorization": headers["Authorization"],
        "Content-Type": "application/json",
        "Accept": "application/json",
        "EstimateID": str(created_estimate_id),
        "SiteID": "04"
    }

    response = requests.get(url, headers=jo_headers)

    raw = response.json()  # WILL BE STRING
    data = json.loads(raw) if isinstance(raw, str) else raw

    print("\n📥 Raw Response:", raw)
    print("\n📦 Parsed Data:", data)

    assert isinstance(data, list), "❌ API did not return a list"
    assert len(data) > 0, "❌ No job order found"

    job = data[0]

    created_joborder_id = job.get("ID")
    created_joborder_no = job.get("JONumber")

    print("\n🎯 Job Order Fetched:", created_joborder_no)




def test_insert_timesheet():
    global created_joborder_id, created_joborder_no

    assert created_joborder_id is not None, "❌ Job order not fetched"
    assert created_joborder_no is not None, "❌ Job order number missing"

    url = f"{BASE_URL}/mnr/v1/pending-job-order-completion/insert-timesheet"

    # ⭐ Dynamic start & end time
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=10)

    start_str = start_time.strftime("%Y-%m-%dT%H:%M")
    end_str = end_time.strftime("%Y-%m-%dT%H:%M")

    payload = {
        "EstimateDtlId": created_joborder_id,
        "ArtisanStartDate": start_str,
        "ArtisanEndDate": end_str,
        "TimeSpent": "00:10",   
        "StaffId": 10,
        "CrtBy": "16",
        "GeoId": 4,
        "Flag": "Auto",
        "JONo": created_joborder_no
    }

    print("\n📤 Posting Timesheet Entry:")
    print(json.dumps(payload, indent=4))

    response = requests.post(url, headers=headers, json=payload)

    try:
        data = response.json()
    except:
        data = response.text

    print("\n📥 Timesheet Response:", data)

    assert response.status_code in [200, 201], \
        f"❌ Timesheet insert failed (status {response.status_code})"

    print("\n✅ Timesheet inserted successfully!")


def test_complete_job_order():
    global created_estimate_id, created_joborder_id, created_joborder_no

    assert created_estimate_id is not None, "❌ EstimateID missing"
    assert created_joborder_id is not None, "❌ EstimateDtlID missing"
    assert created_joborder_no is not None, "❌ JobOrderNo missing"

    url = f"{BASE_URL}/mnr/v1/pending-job-order-completion/complete-job-order"

    payload = {
        "EstimateId": str(created_estimate_id),
        "JobOrderNo": created_joborder_no,
        "EstimateDtlID": created_joborder_id
    }

    print("\n📤 Completing Job Order:")
    print(json.dumps(payload, indent=4))

    response = requests.post(url, headers=headers, json=payload)

    try:
        data = response.json()
    except:
        data = response.text

    print("\n📥 Complete Job Order Response:", data)

    assert response.status_code in [200, 201], \
        f"❌ Job order completion failed (status {response.status_code})"

    print("\n🎉 Job Order Completed Successfully!")




