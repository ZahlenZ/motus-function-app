import json
import logging

import azure.durable_functions as df
import azure.functions as func


def orchestrator_function(context: df.DurableOrchestrationContext):
    """This orchestration will load any new employees, and update any employee data that has changed since the last upload."""

    parameters = yield context.call_activity("Parameters")

    token = yield context.call_activity("GetToken", parameters)

    main_df = yield context.call_activity("GetMainDF", parameters)

    sub_df = yield context.call_activity("GetSubDF", token)

    payload = yield context.call_activity("CheckMissingEmployees", (main_df, sub_df))

    status = yield context.call_activity(
        "UploadNewEmployees", (token, payload, parameters)
    )

    payload = yield context.call_activity("CheckEmployeesUpdate", (main_df, sub_df))

    status = yield context.call_activity("UploadUpdatedEmployees", (token, payload))



main = df.Orchestrator.create(orchestrator_function)
