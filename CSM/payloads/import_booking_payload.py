from datetime import datetime, timezone
import random
import string


def get_import_booking_payload():
    """
    Creates Import Booking payload and returns
    both payload and generated values for reuse.
    """

    utc_now = datetime.now(timezone.utc).isoformat()
    today = datetime.now().strftime("%Y-%m-%d")

    # ---- Generate once ----
    ligm_no = str(random.randint(1000000, 9999999))
    line_no = str(random.randint(10, 99))
    bl_no = f"BLADI{random.randint(10000, 99999)}"

    payload = {
        "ID": 0,
        "SiteID": 1,
        "IsActive": True,
        "CrtByTokenID": 101,
        "CrtDate": utc_now,

        "BLDate": utc_now,
        "IsLCLBooking": False,

        "BookingTypeID": 10394,
        "ContainerCycleID": 37,
        "CargoCycleID": 67,

        # ---- Generated fields ----
        "LIGMNumber": ligm_no,
        "LIGMDate": today,
        "LineNumber": line_no,
        "BLNumber": bl_no,

        "GIGMNumber": str(random.randint(1000000, 9999999)),
        "GIGMDate": today,

        "SMTPNumber": "",
        "SMTPDate": None,

        "TModeTypeID": "627",
        "TModeAgent": "",

        "PortOfLoading": "PortLD" + "".join(random.choices(string.ascii_uppercase, k=4)),
        "PortOfArrival": "PortAR" + "".join(random.choices(string.ascii_uppercase, k=4)),

        "ArrivalDate": None,
        "BreifCargoDescription": "",
        "CallName": "",

        "BerthingDate": None,
        "ActualTimeOfArrival": None,

        "InBoundVoyage": "",
        "OutBoundVoyage": "",
        "RotationalNumber": "",

        "IsBreakBulk": False,
        "IsBondedCargo": False,
        "IsBondedCargoWithContainerBooking": False,
        "BondNumber": "",

        "Status": 70
    }

    return payload, {
        "ligm_no": ligm_no,
        "line_no": line_no,
        "bl_no": bl_no
    }


def get_import_booking_details_payload(
    bkid: int,
    context: dict
):
    """
    Creates Import Booking Details payload
    using values generated during Import Booking.
    """

    return {
        "ID": 0,
        "SiteID": 1,
        "BkID": bkid,

        "TModeTypeID": 627,
        "CommodityID": 669,
        "CHAID": 173727,

        "CrtByTokenID": 101,
        "MdByTokenID": 0,

        # ---- Reused values (NO mismatch) ----
        "LIGMNo": context["ligm_no"],
        "LIGMLineNo": context["line_no"],
        "BLNo": context["bl_no"],

        "DisplayCrtDate": None,
        "DisplayMdDate": None,

        "AchName": "MAERSK INDIA PVT LTD(MSK)",
        "AchCode": "MSK",

        "CHAName": "MAERSK INDIA PVT LTD(MSK)",
        "CHACode": "MSK",
        "OperatorName": "MAERSK INDIA PVT LTD",
        "OperatorID": 16185,

        "TModeName": None,
        "ApplyPublish": "Both",

        "LIGMDate": "2025-12-21T18:30:00.000Z",

        "CrtDate": datetime.now(timezone.utc).isoformat(),
        "MdDate": datetime.now(timezone.utc).isoformat(),

        "IsAchOpr": False,
        "IsActive": True,
        "IsDomesticContainerJobExist": False,

        "AchID": 135762
    }


def get_import_booking_cargo_payload(bkid: int, context: dict):
    return {
        "ID": 0,
        "SiteID": 1,

        # 🔑 REQUIRED
        "BkID": bkid,
        "LineNumber": context["line_no"],

        "CHAID": 173727,
        "CustomAgent": "MAERSK INDIA PVT LTD",

        "CANoOfPackage": "100",
        "CAPackageTypeID": "217",

        "DECVolume": "100",
        "DECWeight": "100",

        "VolMeasUnitID": "135",
        "WtMeasUnitID": 131,

        "IsActive": True,
        "CrtByTokenID": 101,
        "StatusID": 0
    }


def get_import_booking_container_payload(bkid: int):
    return {
        "ID": 0,
        "SiteID": 1,

        # 🔑 Mandatory
        "BkID": bkid,
        "ContainerNo": f"ADIU{random.randint(1000000, 9999999)}",
        "OperatorID": 16185,

        "LFCL": "85",
        "COSizeTypeID": 399,
        "ISOSizeType": "457",
        "TareWeight": 2300,

        "DPD": True,
        "StatusID": 70,
        "IsActive": True,

        "Commodity": "669"
    }


def get_import_cargo_container_mapping_payload(
    *,
    cargo_id: int,
    container_id: int,
    container_no: str
):
    """
    Creates payload for mapping Import Cargo with Import Container
    """

    return {
        "mappinglist": [
            {
                "ContainerID": container_id,
                "ContainerNo": container_no,

                "SelectedColumn": False,

                "Packages": 100,
                "ExistingPackages": 0,
                "MappedWeight": 100,
                "Volume": 100,

                "CargoType": "NA",
                "MappedBalanceNoOfPackage": 0,

                "IsActive": True,
                "selected": True,

                "Weight": 100,
                "NoOfPackages": 100,

                "CargoID": str(cargo_id),
                "VolumeUnitID": 135
            }
        ],
        "CargoID": str(cargo_id),
        "UserID": 1,
        "SiteID": 1
    }


def get_import_booking_boe_payload(
    *,
    bkid: int,
    cargo_id: int,
    bk_unique_no: str,
    cargo_unique_no: str,
    line_no: str
):
    # ---- Dynamic values ----
    be_number = str(random.randint(1000000, 9999999))
    be_date = datetime.now().strftime("%Y-%m-%dT00:00:00.000Z")

    return {
        "ParentBoEDto": {
            "ID": cargo_id,
            "UniqueNo": cargo_unique_no,      # 🔑 Cargo Unique No
            "BkUniqueNo": bk_unique_no,
            "BkID": bkid,
            "LineNumber": line_no,

            "BETypeID": 96,
            "DECWeight": 100,
            "DECVolume": 100,
            "WtMeasUnitID": 131,
            "VolMeasUnitID": 135,
            "CANoOfPackage": 100,
            "CAPackageTypeID": 217,

            "StatusID": 70,
            "IsActive": True,
            "IsValidBoE": 1,

            "CHAID": 173727,
            "ACHID": 135762
        },

        "SubBoE1Dto": {
            "ParentID": cargo_id,
            "LineNumber": line_no,

            # 🔴 Dynamic
            "BENumber": be_number,
            "BEDate": be_date,

            "BETypeID": 74,
            "CANoOfPackage": 100,
            "Duty": 100,
            "CIFValue": 100000
        },

        "SubBoE2Dto": {
            "ParentID": cargo_id,
            "LineNumber": line_no,
            "BETypeID": 95
        },

        "SiteID": 1
    }


def get_import_booking_ooc_payload(cargo_id: int, be_date: str):
    """
    Payload for SaveImportBookingCargoOOC
    - BEDate MUST come from BOE update
    """

    return {
        "ID": cargo_id,
        "OOCNumber": str(random.randint(1000000000, 9999999999)),
        "OOCDate": datetime.now().strftime("%Y-%m-%dT%H:%M"),
        "OOCType": "H",
        "IsOOC": True,
        "BEDate": be_date
    }


def get_import_work_order_payload(import_context: dict):
    """
    Build Work Order payload for Import Booking
    """

    return {
        "COID": import_context["bkid"],                     # Booking ID
        "BookingNumber": import_context["booking_no"],      # Booking Number
        "ContainerNo": import_context["container_no"],      # Container No
        # Container Unique No
        "COUniqueNo": import_context["co_unique_no"],

        "ContainerCycleID": 37,                              # IMPORT
        "ContainerOperator": "MAERSK INDIA PVT LTD",
        "ContainerDepotSizeType": "20 STD",

        "BookingType": "Import Bookings",

        # Safe reference
        "ReferenceNumber": import_context["context"]["ligm_no"],
        "JCOID": None,
        # Static (working value)
        "JODID": 1068,
        "FlowTypeID": 119,                                  # Import flow

        "BLNumber": import_context["context"]["bl_no"],

        "AllocationUnitID": 148,
        "SiteID": 1
    }
