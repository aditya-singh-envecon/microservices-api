"""
Purpose:
--------
Centralized payload builder for Empty Booking and its child Sub-Booking APIs.

Contains:
---------
1. get_empty_booking_payload()
   - Builds request payload for creating an Empty Container Booking.
   - Dynamically generates:
     - Booking reference number (ADI + 7 digits)
     - Timestamps in ISO format
   - Used by Empty Booking creation flow.

2. get_empty_sub_booking_payload(bkid)
   - Builds request payload for creating a Sub-Booking.
   - Requires:
     - bkid (Booking ID from parent Empty Booking)
   - Ensures correct parent-child relationship.

Why This File Exists:
---------------------
- Keeps payload logic separate from test logic.
- Avoids duplication across test scripts.
- Makes maintenance easier when payload fields change.
"""


from datetime import datetime, timezone
import random
import string

booking_ref = f"ADI{random.randint(1000000, 9999999)}"
timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M")
total_conainers_sub_booking = 2

def get_empty_booking_payload(booking_ref: str):
    return {
        "ID": 0,
        "SiteID": 1,
        "BookingTypeID": None,
        "ContainerCycleID": None,
        "UniqueNo": None,
        "BookingNumber": None,
        "JobActID": "1061",
        "ACHID": 135762,
        "ACHContract": None,
        "OpreratorID": 16185,
        "StatusID": 0,
        "IsActive": True,
        "CrtByTokenID": 101,
        "CrtDate": timestamp,
        "MdByTokenID": None,
        "MdDate": timestamp,
        "WorkOrderID": None,
        "JWOID": 100,
        "CHAID": None,
        "DOValidityDate": None,
        "DONumber": None,
        "PlanDate": timestamp,
        "BookingRefrenecNumber": booking_ref,
        "dpumEmptyBookingHistory": None,
        "PositioningThroughID": None,
        "FactoryDestuffThroughID": None,
        "NextLocationID": None,
        "OwnerCodeID": None,
        "PoolCodeID": None,
        "NewOperatorID": None,
        "NewACHID": None,
        "ISPickFromSLpool": False,
        "MovementTypeID": None,
        "SalesAgentID": None,
        "ThirdPartyLogisticsID": None,
        "MIGBookingNumber": None,
        "ApplyPublish": None,
        "OperatorName": "MAERSK INDIA PVT LTD",
        "ACHName": "MAERSK INDIA PVT LTD",
        "MapKey": None,
        "CHAName": None,
        "SourceID": None,
        "SalesAgentName": None,
        "AllocationUnitID": None,
        "ThirdPartyLogisticsName": None,
        "SalesAgentCode": None,
        "ThirdPartyLogisticsCode": None
    }



def get_empty_sub_booking_payload(bkid: int):
    return {
        "ID": 0,
        "DepCOSztyID": 399,
        "TotalContainers": total_conainers_sub_booking,
        "IsUnknownContainerNos": False,
        "BKID": str(bkid),
        "IsActive": True,
        "SiteId": 1,
        "CrtByTokenID": 1,
        "CrtDate": timestamp,
        "StatusID": 0
    }


def generate_container_no():
    """
    Generates a single container number
    Example: MSKU7485677
    """
    prefix = "ADIU"
    number = random.randint(1000000, 9999999)
    return f"{prefix}{number}"


def get_add_empty_container_payload(
    bkid: int,
    booking_ref: str,
    sbkid: int
):
    """
    Payload for AddEmptyContainer API (single container)
    """

    container_no = generate_container_no()

    return {
        "model": {
            "ID": 0,
            "BKID": str(bkid),
            "BookingReferenceNo": booking_ref,
            "Code": "EITP",
            "CODONumber": None,
            "COPlanDate": datetime.now().strftime("%Y-%m-%dT%H:%M"),
            "CODOValidityDate": None,
            "DepCOSztyID": "399",
            "SBKID": sbkid,
            "ISOSizeType": 457,
            "TareWeight": 2300,
            "ContainerNo": container_no,
            "IsActive": True,
            "TotalContainers": None,
            "UniqueNo": None,
            "SiteID": 1,
            "CrtDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "MdDate": None,
            "IsAddCont": True,
            "LineSealNo": None
        },
        "containerList": container_no
    }