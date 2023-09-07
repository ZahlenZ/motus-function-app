import json
import requests
import traceback

from SharedCode.Config import endpoints
from SharedCode.Decorate import log_execution
from SharedCode.LogIt import logger


@log_execution(func_name="UploadUpdate")
def main(UploadUpdatedEmployees: list) -> dict:
    """Upload all employees that need updated

    Args:
        UploadUpdatedEmployees (list): [token, employees]

    Returns:
        dict: {status, # of updated employees}
    """
    # sourcery skip: hoist-statement-from-loop
    token = UploadUpdatedEmployees[0]
    employees = UploadUpdatedEmployees[1]
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    for employee in employees:
        data = {
            "clientEmployeeId1": employee["clientEmployeeId1"],
            "programId": employee["programId"],
            "firstName": employee["firstName"],
            "lastName": employee["lastName"],
            "address1": employee["address1"],
            "city": employee["city"],
            "stateProvince": employee["stateProvince"],
            "country": "USA",
            "postalCode": employee["postalCode"],
            "email": employee["email"],
            "startDate": employee["startDate"],
            "endDate": employee["endDate"],
            "customVariables": [
                {"name": "Branch #", "value": employee["Branch #"]},
                {"name": "Branch Name", "value": employee["Branch Name"]},
            ],
        }
        body = json.dumps(data)
        try:
            r = requests.put(
                url=f"{endpoints.update_driver}/{employee['clientEmployeeId1']}",
                headers=headers,
                data=body,
            )
        except Exception as er:
            logger.func(
                f"Unknown Error in {__name__}.\n\n\
                ERROR: {str(er)}.\n\n\
                TRACEBACK: {traceback.format_exc()}"
            )

    return {}
