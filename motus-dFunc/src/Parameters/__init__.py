import traceback

from SharedCode.Config import kv_names
from SharedCode.Decorate import log_execution
from SharedCode.KVAid import KVHelper
from SharedCode.LogIt import logger


@log_execution(func_name="Parameters")
def main(Parameters: None) -> dict:
    """Gather all credentials from Azure Key Vault

    Returns:
        dict: {motus_credentials, edw_credentials}
    """
    try:
        kv_help = KVHelper(*kv_names)
        datv_credentials = kv_help.get_datv_credentials()
        motus_credentials = {
            "user": kv_help.get_srvc_user(),
            "pass": kv_help.get_srvc_pass(),
        }
        edw_credentials = {
            "user": datv_credentials["db_user"],
            "password": datv_credentials["db_pass"],
            "port": datv_credentials["db_port"],
            "host": datv_credentials["db_host"],
            "db_name": datv_credentials["db_name"],
            "driver": "ODBC Driver 17 for SQL Server",
        }
        return {
            "motus_credentials": motus_credentials,
            "edw_credentials": edw_credentials,
        }
    except Exception as er:
        properties = {"custom_dimensions": {"app": "Motus"}}
        logger.exception(
            f"Unknown error retrieving keyvault items.\n\n\
            ERROR: {str(er)}.\n\n\
            TRACEBACK: {traceback.format_exc()}",
            extra=properties
        )
        raise er
