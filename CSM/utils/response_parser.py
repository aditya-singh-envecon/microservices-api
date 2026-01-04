def extract_empty_booking_data(response_json: dict) -> dict:
    assert response_json.get("Success") is True, "API returned Success = false"

    data = response_json.get("Data")
    assert data, "Response Data is missing"

    extracted = {
        "id": data["ID"],
        "booking_number": data["BookingNumber"],
        "unique_no": data["UniqueNo"],

        "site_id": data["SiteID"],
        "booking_type_id": data["BookingTypeID"],
        "container_cycle_id": data["ContainerCycleID"],

        "ach_id": data["ACHID"],
        "operator_id": data["OpreratorID"],

        "status_id": data["Status"]["ID"],
        "status_code": data["Status"]["Code"],
        "status_name": data["Status"]["Name"],

        "created_date": data["CrtDate"],
        "plan_date": data["PlanDate"]
    }

    return extracted
