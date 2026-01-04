import requests
import json
import uuid
import os
import pytest
from datetime import datetime

BASE_URL = "http://172.16.23.54:9884"
ENDPOINT = "/mnr/v1/component-code"

# 🔐 Paste your valid JWT token below
JWT_TOKEN = """eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkNOdjBPSTNSd3FsSEZFVm5hb01Bc2hDSDJYRSIsImtpZCI6IkNOdjBPSTNSd3FsSEZFVm5hb01Bc2hDSDJYRSJ9.eyJhdWQiOiJhcGk6Ly9mYmU3ODE0Zi1jMjljLTQ3NWMtOWZkMi1lYjVjMzdhZjNiOTAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8zZWQ5YWQ4Mi01YThiLTQzY2YtOWI0YS1kMGRjNmIzZDM0YWUvIiwiaWF0IjoxNzQ5Nzk0NDk5LCJuYmYiOjE3NDk3OTQ0OTksImV4cCI6MTc0OTc5OTAxOSwiYWNyIjoiMSIsImFpbyI6IkFaUUFhLzhaQUFBQVRIRmExOTM2OTRaQXZGUHZwOWZKRzd3WlFmZEZCcEpiTXpQVWQxYUpGd1g2UW84aGpYY0tYaTVWbmpQSkNSais0SHlCWXV1VG1IU2M2QUFtTlhwVXRscXF3QktnQnN5Y01pb0pJaDA4cDVmRGE0L0dRTHVNRG52dm44KytjK01xb2RheFFnTFQ0Q2ZCRzdlRUdGbHp1QU1JMllPbWV2TklVS0h4UDZ2OW1DOThtSi9iWEpyMWhOcXFQMTM4OHZQOCIsImFtciI6WyJwd2QiLCJtZmEiXSwiYXBwaWQiOiIxNTM3MGExZC1lMzMwLTRjOTgtYjczMC0yNmM4MTIzZTZjYjMiLCJhcHBpZGFjciI6IjEiLCJmYW1pbHlfbmFtZSI6IlNpbmdoIiwiZ2l2ZW5fbmFtZSI6IkFkaXR5YSIsImlwYWRkciI6IjExMC41LjcyLjMiLCJuYW1lIjoiQWRpdHlhIFNpbmdoIiwib2lkIjoiNDMyODlmYmEtNTQwZi00MzJkLTg1MmItOThhYmU3ZDUwMGNjIiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTI3MjU0MTY5MjAtMzI4ODczOTA0Mi0zNDA5MTAzMjA5LTEzOTA4IiwicmgiOiIxLkFWUUFncTNaUG90YXowT2JTdERjYXowMHJrLUI1X3Vjd2x4SG45THJYRGV2TzVDaUFOWlVBQS4iLCJzY3AiOiJhY2Nlc3NfTU5SIiwic2lkIjoiMDA1ZDkxMzktOWU2Mi0wZWNiLTRlYmYtOTUwYzg0MGRhOWJmIiwic3ViIjoiRmhkWVF0X3J3WjNOeEVNYUJZbEhYb1poa180bmF0bzdJazVyUWpNU25oUSIsInRpZCI6IjNlZDlhZDgyLTVhOGItNDNjZi05YjRhLWQwZGM2YjNkMzRhZSIsInVuaXF1ZV9uYW1lIjoiYWRpdHlhLnNpbmdoQEVOVkVDT04uQ09NIiwidXBuIjoiYWRpdHlhLnNpbmdoQEVOVkVDT04uQ09NIiwidXRpIjoiMG9uQ1UyYXlKa2VKVlNmci1sY3ZBQSIsInZlciI6IjEuMCIsInhtc19mdGQiOiJLdlozQ0FnUEs5QWVFRWliQUZ6TnktTHVHWWs3NnFKMTNKMXhiT00tWXVZQmEyOXlaV0Z6YjNWMGFDMWtjMjF6In0.Du-NQnGDGwmDKF2g_d893NGHDV9Rmy5tgRG4UGOdOVA-pj_07b5wyXFTIha0KJVmZ-StmuZMtj1jil5T0dEC9qoCaProzfAsh5g--j-ehs7slPA0j9-DGi5VBlxyIg7rBjIDRo19FLwp6n9aX86GsdaAzMv19q6Y1N5_D_f1d6aSZpqplOyDHbT_Eir0MQvb-lWCeqH9N2mBJpkLDI6_y28vwZDon4aWL5J4B6XF44osJbm1sy7i5tLFaScVZ-9A0pUs0SDckV9X2BEmb9UrhbNu2qQc2SIbsOjgumt58xYpglrIwTdat3uy94GIIRl63GiF95ZceZpejcKwScav5A"""

def test_component_code_api():
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}",
        "Accept": "application/json"
    }

    component_name= "Auto Part " + str(uuid.uuid4().int)[:4]

    payload = {
        "id": 0,
        "code": "",
        "name": component_name,
        "longName": component_name,
        "isActive": True,
        "crtByTokenID": 16  # 🔁 Use a valid user ID if needed
    }

    url = f"{BASE_URL}{ENDPOINT}"
    response = requests.post(url, headers=headers, json=payload)

    print("📥 Full Response:", response.text)
    print("📤 Request URL:", url)
    print("📤 Payload:", json.dumps(payload, indent=2))
    print("📥 Status Code:", response.status_code)
    print("📥 Response Body:", response.text[:500])  # Print first 500 chars

    # Basic validations
    assert response.status_code in [200, 201], f"Expected 200/201 OK but got {response.status_code}"

    try:
        data = response.json()
    except Exception as e:
        assert False, f"Failed to parse JSON response: {e}"

    # Verify response type is ERROR or SUCCESS
    assert data["messages"][0]["type"] in ["ERROR", "SUCCESS"], f"Unexpected type: {data['messages'][0]['type']}"



# CREATE REPORT

if __name__ == "__main__":
    import pytest
    import os
    from datetime import datetime
 
    # Create reports directory if it doesn't exist
    # reports_dir = "AppointmentManagement_TestScenarios/reports"
    reports_dir = "MNR_Microservices_APITesting/MNR_Reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
 
    # Generate timestamp for report name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = f"Configuration_TestReport_{timestamp}.html"
    report_path = os.path.join(reports_dir, report_name)
 
    # Run all tests and generate combined HTML report
    pytest.main([
        __file__,
        "-v",
        f"--html={report_path}",
        "--self-contained-html"
    ])
 
    print(f"\nTest execution completed.")
    print(f"Combined test report generated at: {report_path}")
