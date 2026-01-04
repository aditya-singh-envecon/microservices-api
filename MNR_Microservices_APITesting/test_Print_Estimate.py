import requests
import pytest
import json

BASE_URL = "http://172.16.23.54:9884"
PRINT_ENDPOINT = "/mnr/v1/pending-approval/print-estimate"

JWT_TOKEN = """<your token>"""


def test_print_estimate_to_pdf():
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}",
        "Accept": "application/pdf",
        "SiteID": "04",
        "EstimateID": "3413"
    }

    url = f"{BASE_URL}{PRINT_ENDPOINT}"
    response = requests.post(url, headers=headers)

    print("📥 Status Code:", response.status_code)
    
    assert response.status_code == 200, "❌ Print API failed"

    # Save PDF file
    pdf_path = "print_estimate_3413.pdf"

    with open(pdf_path, "wb") as f:
        f.write(response.content)

    print(f"✅ PDF saved successfully at: {pdf_path}")

