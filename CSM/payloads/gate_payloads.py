# payloads/gate_payloads.py

from datetime import datetime, timezone
from utils.gate_utils import (
    generate_tmod_no,
    get_current_time,
    get_time_minus_5_minutes
)
from datetime import datetime, timezone, timedelta


timestamp = (
    datetime.now(timezone.utc)
    .strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
)

def get_gate_container_list_payload(page=1, page_size=10):
    return {
        "Page": page,
        "PageSize": page_size,
        "Id": 0,
        "CurrentDate": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "IsGateOUT": False,
        "IsExceedCreditLimit": False,
        "IsTruckIn": True,
        "IsTruckOut": False,
        "IsAssignVehicleGateOut": False,
        "TModGateInCode": "",
        "TModGateOutCode": "",
        "PlnTmodWbr": "",
        "POutTmodWbr": "",
        "ContainerNo": "",
        "BookingNo": "",
        "VehicleNo": "",
        "WONO": "",
        "TModPassNo": "",
        "TmodCode": "",
        "IsSearchOnGateScreen": False,
        "IsFirstTimeDataList": False,
        "Cycle": "ECON",
        "Filters": []
    }




def _utc_now_ms():
    return (
        datetime.now(timezone.utc)
        .strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    )


def _utc_minus_5_min_ms():
    return (
        (datetime.now(timezone.utc) - timedelta(minutes=5))
        .strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    )





def get_gate_save_details_payload(context: dict):
    """
    FULL & ACCURATE Gate Save Details payload
    (NO shortcuts, UI-equivalent)
    """

    tmod_no = generate_tmod_no()

    model = {
        # ================= REQUIRED WRAPPER DATA =================
        "id": context["id"],
        "coid": context["coid"],
        "containerNo": context["container_no"],
        "uniqueNo": context["unique_no"],
        "bkno": context["bkno"],

        # ================= BACKEND REQUIRED (FROM ERROR) =================
        "ContainerCycle": context.get("container_cycle", 40),  # EMPTY IN
        "IsCargoContainer": False,

        # ================= TMOD / VEHICLE =================
        "tModNo": tmod_no,
        "vehicleNo": tmod_no,
        "tModPassID": context["tmod_pass_id"],
        "tmodCode": context["tmod_code"],
        "tmodPassActivity": context["tmod_code"],
        "tmodDesc": "LOADED TRUCK IN WITH CONTAINER",
        "transportActivity": context["transport_activity"],
        "gateOperation": context["gate_operation"],

        # ================= JOB =================
        "jobOrderID": context["job_order_id"],
        "jodid": context["jodid"],
        "jodActID": context["jod_act_id"],
        "jobcatg": "2.5",
        "jobactpCat": "Depot Gate Operation",

        # ================= CONTAINER =================
        "operatorID": context["operator_id"],
        "operatorCode": context.get("operator_code", ""),
        "coSizeTypeID": context["co_size_type_id"],
        "isoSizeType": context["iso_size_type"],
        "isoSizeTypeCode": context.get("iso_size_type_code", "22G1"),
        "tareWeight": int(context["tare_weight"]),  # MUST BE INT
        "capacity": None,
        "teu": 1,

        # ================= TIME (DYNAMIC) =================
        "tModDate": "2025-12-31T23:59:00",
        "cfsGateInDateTime": get_current_time(),
        "portOutDateTime": get_time_minus_5_minutes(),

        # ================= SEALS =================
        "sealNo": None,
        "operatorSealNo": None,
        "shipperSealNo": None,
        "customsSealNo": None,
        "lineSealNo": None,
        "washingSealNo": None,

        # ================= FLAGS =================
        "isActive": True,
        "isTModWBR": True,
        "isWBR": 0,
        "jobWBR": True,
        "isSOC": False,
        "isGOH": False,
        "isOnWheel": False,
        "isReefer": False,
        "isEdit": False,
        "isTBAContainer": False,
        "isScan": None,
        "isHold": False,
        "isWeighmentMandatory": True,
        "isSemiLBT": None,

        # ================= CYCLE / BOOKING =================
        "cocyle": "EMPTY CONTAINER IN BY TRUCK FROM PORT",
        "cO_EMXDF": "IE",
        "cO_LFCL": None,
        "cO_OPRTR": "",
        "cO_DEPSZTY": "20STD",
        "cycleType": "IE",
        "bookingType": "ECON",

        # ================= TRANSPORT =================
        "transactionNo": None,
        "tModTransportID": None,
        "transportName": None,
        "transport": None,
        "tModDriver": None,
        "transportTypeID": None,
        "transportType": None,
        "vehicleTypeID": None,
        "transporterCode": "",

        # ================= GATE CONFIG =================
        "tModGateInID": 24,
        "tModGateOutID": 24,
        "tModGateIn": "",
        "tModGateOut": "",
        "plnTmodGate": "",
        "tModInstruction": None,
        "tModPassNo": None,
        "tModWBRInID": 3,
        "tModWBROutID": 3,
        "plnTmodWbr": "",
        "pOutTmodWbr": "",

        # ================= BOOKING / DOCS =================
        "bkdate": None,
        "blno": "0",
        "bldate": None,
        "wono": "0",
        "woid": 0,

        # ================= LOCATION =================
        "geoCode": "WEST TERMINAL",
        "portOfArrival": "0",
        "portName": "0",
        "porttransno": "0",
        "portExistPassNo": "0",
        "portTime": None,
        "portTimeName": None,

        # ================= CARGO / IMO =================
        "cargoType": None,
        "imoCode": "0",
        "unoCode": "0",

        # ================= SCAN / HOLD =================
        "scanLocation": "0",
        "scanDetail": None,
        "scanDetails": None,
        "ibcIsScan": None,
        "holdid": None,
        "holdTypeID": None,
        "holdComments": None,
        "holdType": None,

        # ================= EIR =================
        "eirid": 0,
        "eirRequestNo": "",
        "canEIR": True,

        # ================= SYSTEM =================
        "creditLimitJSONResponse": None,
        "ptiDone": None,
        "raps": None,

        # ================= UI =================
        "rowNum": 1,
        "totalCount": 1
    }

    # 🔴 ABSOLUTELY REQUIRED BY BACKEND
    return {
        "models": [model]
    }