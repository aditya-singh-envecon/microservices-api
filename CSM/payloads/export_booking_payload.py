from datetime import datetime, timezone
import random
import string

def get_export_booking_payload():
    utc_now = datetime.now(timezone.utc).isoformat()
    today = datetime.now().strftime("%Y-%m-%d")

    return {
        "ID": 0,
        "SiteID": 1,
        "IsActive": True,
        "CrtByTokenID": 101,
        "CrtDate": utc_now,

        "IsBreakBulk": False,
        "ModelState": 0,

        "CHAName": "ADITYA LOGISTICS",
        "ExporterName": "ADITYA LOGISTICS",

        "BookingTypeID": 10395,
        "ContainerCycleID": 38,
        "CargoCycleID": 68,
        "Status": 70,

        "SBNumber": str(random.randint(1000000, 9999999)),
        "SBDate": today,

        "ExporterID": 173730,
        "CHAID": 173730,
        "CHACode": "ADI01",

        "FOB_VAL": "100000",
        "PortOfDischarge": "PORT" + "".join(random.choices(string.ascii_uppercase, k=4)),

        "IsAutoCreated": False,
        "IEBIN": "",
        "TotalContainerFullIn": True,
        "IECID": None,
        "IECode": ""
    }
