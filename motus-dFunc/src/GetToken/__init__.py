import json

import requests

from SharedCode.Config import endpoints
from SharedCode.Decorate import log_execution


@log_execution(func_name="GetToken")
def main(GetToken: dict) -> str:
    """Acquire JWT token from Motus Server

    Args:
        GetToken (dict): parameters

    Returns:
        str: JWT token string
    """
    parameters = GetToken["motus_credentials"]
    data = {"loginId": parameters["user"], "password": parameters["pass"]}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    r = requests.post(url=endpoints.get_token, headers=headers, data=data)

    # NOTE: remove this before launch, just to test response on payload
    content = r.content
    
    return content.decode("utf-8")
