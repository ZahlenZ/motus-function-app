import json

import requests

from SharedCode.Config import endpoints
from SharedCode.Decorate import log_execution


@log_execution(func_name="GetSubDF")
def main(GetSubDF: str) -> dict:
    """Get list of drivers from Motus

    Args:
        GetSubDF (str): JWT Token from Motus

    Returns:
        dict: Drivers from Motus
    """
    token = GetSubDF

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    r = requests.get(
        url=endpoints.get_drivers,
        headers=headers,
    )

    return json.loads(r.content)
