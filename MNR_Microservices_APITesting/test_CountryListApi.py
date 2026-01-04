from urllib import response
import requests
import json
import random
import string
from datetime import datetime, timezone

BASE_URL = "http://172.16.23.54:9884"
LIST_ENDPOINT = "/mnr/v1/country/list"
CRT_ENDPOINT = "/mnr/v1/country"

# This is the ID of the country to delete
Country_ID = "5";  

# Enter details for new country creation
country_code = "IRN"
country_name = "Iran"

# 🔐 Paste your valid JWT token below
JWT_TOKEN = """eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkpZaEFjVFBNWl9MWDZEQmxPV1E3SG4wTmVYRSIsImtpZCI6IkpZaEFjVFBNWl9MWDZEQmxPV1E3SG4wTmVYRSJ9.eyJhdWQiOiJhcGk6Ly9mYmU3ODE0Zi1jMjljLTQ3NWMtOWZkMi1lYjVjMzdhZjNiOTAiLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8zZWQ5YWQ4Mi01YThiLTQzY2YtOWI0YS1kMGRjNmIzZDM0YWUvIiwiaWF0IjoxNzUzOTQwMzEyLCJuYmYiOjE3NTM5NDAzMTIsImV4cCI6MTc1Mzk0NDg5MywiYWNyIjoiMSIsImFpbyI6IkFaUUFhLzhaQUFBQTdXV3pLMVlQNmtTbTJ0cVZtdU05eTZqTy9pV0hnOFhNcGs1NmlwRWNkMmQxY0M4QzRLVmxLNE9ieVlsZkoweENlTUpBSG95VEh3eSs3cGcyMHpadndOaTNWUitnaGd1aUNKMFlYVlFmYURQaE5TSjQwSldxUUNzR1B1QzRPQ1l3K3RYTmJKUzBzU2g0RnlCamJYM1hGd2x2WDZVanZnNmtXNnZuMjdWRFZzSkF3UU5HNTZVcWkrUTJEWm0rV0JIciIsImFtciI6WyJwd2QiLCJtZmEiXSwiYXBwaWQiOiIxNTM3MGExZC1lMzMwLTRjOTgtYjczMC0yNmM4MTIzZTZjYjMiLCJhcHBpZGFjciI6IjEiLCJmYW1pbHlfbmFtZSI6IlNpbmdoIiwiZ2l2ZW5fbmFtZSI6IkFkaXR5YSIsImlwYWRkciI6IjExMC41LjcyLjMiLCJuYW1lIjoiQWRpdHlhIFNpbmdoIiwib2lkIjoiNDMyODlmYmEtNTQwZi00MzJkLTg1MmItOThhYmU3ZDUwMGNjIiwib25wcmVtX3NpZCI6IlMtMS01LTIxLTI3MjU0MTY5MjAtMzI4ODczOTA0Mi0zNDA5MTAzMjA5LTEzOTA4IiwicmgiOiIxLkFWUUFncTNaUG90YXowT2JTdERjYXowMHJrLUI1X3Vjd2x4SG45THJYRGV2TzVDaUFOWlVBQS4iLCJzY3AiOiJhY2Nlc3NfTU5SIiwic2lkIjoiMDA1ZmI0MTktMTQ4Yi1kNmFhLWZhNDgtY2JjZjk0MmU4YTRlIiwic3ViIjoiRmhkWVF0X3J3WjNOeEVNYUJZbEhYb1poa180bmF0bzdJazVyUWpNU25oUSIsInRpZCI6IjNlZDlhZDgyLTVhOGItNDNjZi05YjRhLWQwZGM2YjNkMzRhZSIsInVuaXF1ZV9uYW1lIjoiYWRpdHlhLnNpbmdoQEVOVkVDT04uQ09NIiwidXBuIjoiYWRpdHlhLnNpbmdoQEVOVkVDT04uQ09NIiwidXRpIjoiNU5Qd21aLXRVa0t2bDA4TGpIRlRBQSIsInZlciI6IjEuMCIsInhtc19mdGQiOiJFRG9ld0ZkTlNQUU53ZWdNRENGeFRfX05rNHZia29Xd0t0LVQxTnRZWDRFQmEyOXlaV0ZqWlc1MGNtRnNMV1J6YlhNIn0.kbDuZZSFDMeBOvjZ357o_fTJ4C8l2vcHFGSNMzTn-iwKW58wa_etegtxj3LO1T05gzMZxudCrBXY_zqME7TRmCzcBdY5PzlCgiEcCwk7tlodPHFTEkpBRnNH-G6erQM209dmlYTq2owqKDEa54bZxiNo1u1MtWX-O-Fmm4yCs55PreqFW0212IkudvsvnMmDnHP8dv6nvwGMj0Q0oyZOwpqYO0Nw2Kw3Hp3DBr47As0Hoy9uorlF411Sb8JthD1YSBjgKn2bVuRjYf0e17vgsPkyoKyoEesRaLSFSLiSi-0QReQ4EmDZYMZQba74T82mmICAVkXF_ayEAKRz9jLJxg"""

def test_country_list_api():
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}",
        "Accept": "application/json"
    }

    response = requests.get(f"{BASE_URL}{LIST_ENDPOINT}", headers=headers)
    assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}"

    try:
        raw_data = response.json()
        # Some APIs return JSON string inside JSON — check and parse accordingly
        data = json.loads(raw_data) if isinstance(raw_data, str) else raw_data
    except Exception as e:
        assert False, f"Failed to parse response JSON: {e}"

    assert isinstance(data, list), "Expected a list of country entries"

    # ✅ Output visible country list for review
    print(f"\n✅ Total Countries Found: {len(data)}")
    for item in data:
        id_ = item.get("ID", "-")
        code = item.get("Code", "-")
        name = item.get("Name", "-")
        is_active = item.get("IsActive", "-")
        print(f"ID: {id_} | Code: {code} | Name: {name} | Active: {is_active}")



def test_create_new_country():
    # Generate dynamic country data

    payload = {
    "id": 0,
    "code": country_code,
    "name": country_name,
    "isActive": True,
    "crtByTokenID": 16,
    "mdByTokenID": 16,
    "mdDate": "1992-04-03T12:58:13.468Z"
}

    url = f"{BASE_URL}{CRT_ENDPOINT}"
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)

    print("📤 Request URL:", url)
    print("📤 Payload:", json.dumps(payload, indent=2))
    print("📥 Status Code:", response.status_code)
    print("📥 Response Body:", response.text[:500])

    # ✅ Assertion for test validation
    assert response.status_code == 200 or response.status_code == 201   


def test_delete_country():

    headers = {
    "Content-Type": "application/json",
    "countryID": Country_ID   # <-- pass the countryID here
    }
    url = f"{BASE_URL}{LIST_ENDPOINT}"
    response = requests.delete(url, headers=headers)

    print("📥 Status Code:", response.status_code)
    print("📥 Reason:", response.reason)
    try:
        print("📥 Response JSON:", response.json())
    except Exception:
        print("📥 Response Text:", response.text)