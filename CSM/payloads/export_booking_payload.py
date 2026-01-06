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


def get_export_booking_details_payload(export_ctx: dict):
    return {
        "ID": 0,
        "UniqueNo": None,

        # 🔑 Link to Export Booking
        "BkID": export_ctx["bkid"],
        "SBNumber": export_ctx["sb_number"],
        "SBDate": export_ctx["sb_date"],

        # ACH / Operator
        "ACHID": export_ctx["exporter_id"],
        "IsACHOpr": 0,
        "OperatorID": 16447,   # static for now (MMJ LOGISTICS)

        # System / Audit
        "IsActive": True,
        "CrtByTokenID": 101,
        "CrtDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),

        "MdByTokenID": 0,
        "MdDate": None,

        # Flags
        "IsBreakBulk": False,
        "IsDisableOperator": False,
        "CustomerTrigger": True
    }


def get_export_cargo_payload(ctx):

    sb_number = ctx["sb_number"]

    return {
        "model": {
            "ID": 0,
            "BkID": ctx["bkid"],
            "Status": 70,

            "DocumentTypeID": 513,

            "SubLineNumber": sb_number,
            "SubLineDate": ctx["sb_date"],

            "ACHNameID": ctx["ach_id"],
            "ACHName": "ADITYA LOGISTICS(ADI01)",

            "Weight": "100",
            "WeightUnit": "131",
            "Volume": "100",
            "VolumeUnit": "135",

            "PackageNumbers": "100",
            "PackageTypeID": "211",
            "CommodityID": "671",

            "IsHaz": False,
            "UNNO": "",

            "SiteID": 1,

            # 🔑 Booking linkage
            "BkSBNumber": ctx["sb_number"],
            "BkSBDate": ctx["sb_date"],

            "CHAID": ctx["ach_id"],
            "CHAName": "ADITYA LOGISTICS",
            "BkCHACode": ctx["cha_code"],

            "BkPortOfDischarge": ctx["port_of_discharge"],
            "PortOfDischarge": ctx["port_of_discharge"],

            "IsBreakBulk": False,
            "UOMsqmExport": 0,
            "AreaSqmExport": 0,

            "IsAuction": False,
            "IsHold": False,

            "IsActive": True,
            "CrtDate": datetime.utcnow().isoformat(),
            "IsDirect": False
        },
        "IsArrived": False,
        "IsLEO": False
    }


def generate_container_no(prefix: str = "ADIU") -> str:
    """
    Generates a valid Export container number.
    Example: ADIU7861238
    """
    return f"{prefix}{random.randint(1000000, 9999999)}"


def get_export_container_payload(ctx: dict):
    container_no = generate_container_no()

    return {
        "ID": 0,
        "BkID": ctx["bkid"],

        # 🔑 Dynamic container number
        "ContainerNo": container_no,

        "LFCL": "85",
        "OperatorID": ctx["operator_id"],
        "DepotSizeTypeID": "399",
        "ISOSizeTypeID": "457",

        "DecWeight": None,
        "TareWeight": None,
        "WeightUnitID": None,
        "DecVolume": None,
        "VolumeUnitID": None,

        "Commodity": "",
        "PackageNumbers": None,

        "SealNo": None,
        "ShipperSealNo": None,
        "VGMWeight": None,

        "IsHaz": False,
        "IsLRF": False,

        "SetTemp": None,
        "TempUnitID": None,
        "SetHMC": None,
        "SetVent": None,

        "IsGOH": False,
        "IsOOG": False,
        "IsLBT": False,
        "IsSemiLBT": False,

        "StatusID": 70,
        "IsActive": True,

        "EquipmentSealType": "509",

        "POL": "",
        "CONDestination": "",
        "PortID": 0,
        "HoldTypeID": None,
        "IsHold": False,

        "Mappings": [],
        "TotalCargoPackages": 0,
        "SiteID": 1
    }


def get_export_cargo_container_mapping_payload(ctx: dict):
    return {
        "model": [
            {
                "ContainerID": ctx["container_id"],
                "ContainerNo": ctx["container_no"],

                # Cargo reference
                "SourceID": ctx["cargo_id"],
                "CargoID": ctx["cargo_id"],

                "SelectedColumn": 1,
                "selected": True,

                "Packages": 0,
                "ExistingPackages": 0,

                "NoOfPackages": 100,
                "Weight": 100,
                "MappedWeight": 100,
                "Volume": 100,

                "SiteID": 1
            }
        ],
        "CargoID": ctx["cargo_id"],
        "SiteID": 1
    }


def get_export_cargo_container_mapping_payload(ctx: dict):
    return {
        "model": [
            {
                "ContainerID": ctx["container_id"],
                "ContainerNo": ctx["container_no"],

                # Cargo reference

                "SourceID": ctx["cargo_id"],
                "CargoID": ctx["cargo_id"],

                "SelectedColumn": 1,
                "selected": True,

                "Packages": 0,
                "ExistingPackages": 0,

                "NoOfPackages": 100,
                "Weight": 100,
                "MappedWeight": 100,
                "Volume": 100,

                "SiteID": 1
            }
        ],
        "CargoID": ctx["cargo_id"],
        "SiteID": 1
    }


def get_export_cargo_container_mapping_payload(ctx: dict):
    return {
        "model": [
            {
                "ContainerID": ctx["container_id"],
                "ContainerNo": ctx["container_no"],

                # Cargo reference
                "SourceID": ctx["cargo_id"],
                "CargoID": ctx["cargo_id"],

                "SelectedColumn": 1,
                "selected": True,

                "Packages": 0,
                "ExistingPackages": 0,

                "NoOfPackages": 100,
                "Weight": 100,
                "MappedWeight": 100,
                "Volume": 100,

                "SiteID": 1
            }
        ],
        "CargoID": ctx["cargo_id"],
        "SiteID": 1
    }


def get_export_job_order_payload(ctx: dict):
    return {
        "ID": 0,
        "SiteID": 1,
        "IsActive": True,

        # Legacy audit (REQUIRED)
        "CrtByTokenID": 0,
        "CrtDate": "0001-01-01T00:00:00",

        # Transport flags (REQUIRED)
        "IsWORequired": False,
        "IsDualTransport": False,
        "IsOnWheel": False,
        "IsTransportUpdate": False,

        # Legacy null holders
        "MapKey": None,
        "SourceID": None,
        "CAUniqueNo": None,

        # Planning
        "PlanDate": "2026-01-05T23:59",

        # Booking
        "BkTypeID": 10395,
        "BkID": ctx["bkid"],
        "FullInContainer": True,

        # System-generated UniqueNo is allowed to be blank or auto
        "UniqueNo": ctx.get("job_order_unique_no", None),

        # Documents (REQUIRED but empty)
        "HBL": "",
        "OOCNumber": "",
        "LEONumber": "",

        # Parties
        "ACHID": ctx["ach_id"],
        "ACHName": "ADITYA LOGISTICS",
        "OperatorID": ctx["operator_id"],
        "AchContract": None,

        # Job configuration
        "JOBCatID": "98",
        "JODID": "1078",

        # 🔑 Container
        "JODContainerID": str(ctx["container_id"]),
        "CoUniqueNo": ctx["container_unique_no"],

        # 🔑 Cargo (LEGACY PATTERN)
        "JODCargoID": None,
        "DuplicateJODCargoID": ctx["cargo_id"],
        "CargoUniqueNo": "",

        # Cycle & activity
        "CycleID": 38,
        "JOBACTPCatID": "102",
        "JODActivityID": 477,

        # Transport
        "TMODEPassID": 7,
        "MAPDActivityID": None,

        # Flags (ALL REQUIRED)
        "IsCargoOptional": False,
        "JODWBR": False,
        "MAPDWBR": False,
        "JODMulti": True,
        "NOTBillable": False,
        "JODLBR": True,
        "JODEQP": True,
        "JODMTL": True,
        "IsNOCPrint": False,
        "IsSealCuttingCOValidation": False,

        # Size / reference
        "SizeType": "20 STD",
        "BLNumber": None,

        # Booking refs
        "SBNumber": ctx["sb_number"],
        "Number": ctx["sb_number"],
        "SBDate": ctx["sb_date"],
        "Date": ctx["sb_date"]
    }
