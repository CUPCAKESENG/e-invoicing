"""
SENG2021 - Group Cupcake
File: json_report.py
    Description: Creates a JSON communication report
"""

import json
import os
from datetime import datetime
from jwt import encode
from src.error import FormatError
from src.config import SECRET


def create_json_report(report):
    """
    Creates JSON communication report.
        Params: report
        Returns: payload
        Errors: FormatError
    """

    required_keys = ("sender", "received_time", "save_time", "file_size", "filename", "path")

    if not all(key in report for key in required_keys):
        raise FormatError("Communication report is not in the right format.")

    payload = {
        "sender": report["sender"],
        "received_time": report["received_time"],
        "save_time": report["save_time"],
        "file_size": report["file_size"],
        "file_name": report["filename"],
        "file_type": "XML"
    }

    token = encode(payload, SECRET)
    payload["token"] = token[-10:]

    report_path = "communication_report/" + token[-10:] + ".json"

    with open(report_path, "w", encoding="ascii") as file:
        report["access_time"] = datetime.now().strftime('%m/%d/%Y, %H:%M:%S.%f')[:-3]
        json.dump(report, file, default=str)

    return payload