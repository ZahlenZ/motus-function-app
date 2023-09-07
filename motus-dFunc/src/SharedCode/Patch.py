import json
import requests
import traceback

from SharedCode.Config import adaptive_card, adaptive_card_url
from SharedCode.LogIt import logger


def teams_notification(status, params, base_card=adaptive_card, url=adaptive_card_url):
    headers = {"Content-Type": "application/json"}

    base_card["attachments"][0]["content"]["body"][1]["text"] = base_card[
        "attachments"
    ][0]["content"]["body"][1]["text"].format(source=params["edw_credentials"]["host"])

    base_card["attachments"][0]["content"]["body"][2]["text"] = base_card[
        "attachments"
    ][0]["content"]["body"][2]["text"].format(worker_count=status["employees_updated"])

    base_card["attachments"][0]["content"]["body"][3]["text"] = base_card[
        "attachments"
    ][0]["content"]["body"][3]["text"].format(message=status["message"])

    try:
        r = requests.post(url=url, data=json.dumps(base_card), headers=headers)
    except Exception as er:
        logger.exception(
            f"Failed to send teams notification. \n\n\
            ERROR: {str(er)}. \n\n\
            TRACEBACK: {traceback.format_exc()}"
        )
        raise er
