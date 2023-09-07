import json
import pandas as pd
import requests
import traceback

from SharedCode.Config import endpoints
from SharedCode.Decorate import log_execution
from SharedCode.LogIt import logger
from SharedCode.Patch import teams_notification


@log_execution(func_name="UploadNewEmployee")
def main(UploadNewEmployees: list) -> dict:
    """Upload new employees to Motus

    Args:
        UploadNewEmployees (list): [{employee, employee}]

    Returns:
        dict: {status, # of uploaded employees}
    """
    # sourcery skip: hoist-statement-from-loop
    count_bad = 0

    count = 0
    token = UploadNewEmployees[0]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    for new_emp in UploadNewEmployees[1]:
        data = {
            "clientEmployeeId1": new_emp["clientEmployeeId1"],
            "programId": new_emp["programId_x"],
            "firstName": new_emp["firstName_x"],
            "lastName": new_emp["lastName_x"],
            "address1": new_emp["address1_x"],
            "city": new_emp["city_x"],
            "stateProvince": new_emp["stateProvince_x"],
            "country": "USA",
            "postalCode": new_emp["postalCode_x"],
            "email": new_emp["email_x"],
            "startDate": new_emp["startDate_x"],
            "endDate": new_emp["endDate_x"],
            "customVariables": [
                {"name": "Branch #", "value": new_emp["Branch #"]},
                {"name": "Branch Name", "value": new_emp["Branch Name"]},
            ],
        }
        data = json.dumps(data)
        try:
            r = requests.post(url=endpoints.post_driver, headers=headers, data=data)
            if r.status_code == 204:
                count += 1
            elif r.status_code == 500:
                count_bad += 1
        except Exception as er:
            logger.func(
                f"Unknown error in {__name__}.\n\n\
                ERROR: {str(er)}.\n\n\
                TRACEBACK: {traceback.format_exc()}"
            )

    teams_notification(
        status={
            "employees_updated": count,
            "message": f"{count_bad}: Employees failed to upload to Motus."
        },
        params=UploadNewEmployees[2]
    )
    return {
        "employees_updated": len(UploadNewEmployees[1]),
        "message": "All new employees uploaded to MOTUS",
    }
