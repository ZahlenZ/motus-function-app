import pandas as pd

from flatten_json import flatten

from SharedCode.Decorate import log_execution


@log_execution(func_name="CheckEmployeesUpdate")
def main(CheckEmployeesUpdate: list) -> list:
    """Acquire list of employees that need to be updated in motus

    Args:
        CheckEmployeesUpdate (list): [main_df, sub_df]

    Returns:
        dict: [employees]
    """
    

    main_df = pd.DataFrame(CheckEmployeesUpdate[0])
    sub_df = pd.DataFrame([flatten(employee) for employee in CheckEmployeesUpdate[1]])

    sub_df.drop(
        columns=[
            "clientEmployeeId2",
            "address2",
            "country",
            "phone",
            "alternatePhone",
            "leaveStartDate",
            "leaveEndDate",
            "annualBusinessMiles",
            "commuteDeductionType",
            "commuteDeductionCap",
            "customVariables",
            "customVariables_0_name",
            "customVariables_1_name",
        ],
        inplace=True
    )

    sub_df.rename(
        columns={
            "customVariables_0_value": "Branch #",
            "customVariables_1_value": "Branch Name"
        },
        inplace=True
    )

    sub_df = sub_df.merge(main_df, on="clientEmployeeId1", how="right")

    sub_df.drop(
        columns=[
            "programId_y",
            "firstName_y",
            "lastName_y",
            "address1_y",
            "city_y",
            "stateProvince_y",
            "postalCode_y",
            "email_y",
            "startDate_y",
            "endDate_y",
            "Branch #_y",
            "Branch Name_y"
        ],
        inplace=True
    )

    sub_df.rename(
        columns={
            "programId_x": "programId",
            "firstName_x": "firstName",
            "lastName_x": "lastName",
            "address1_x": "address1",
            "city_x": "city",
            "stateProvince_x": "stateProvince",
            "postalCode_x": "postalCode",
            "email_x": "email",
            "startDate_x": "startDate",
            "endDate_x": "endDate",
            "Branch #_x": "Branch #",
            "Branch Name_x": "Branch Name"
        },
        inplace=True
    )


    rows_to_update = []
    for column in main_df.columns:
        if column != "programId":
            different_values = main_df[column].isin(sub_df[column])
            update_index = [index for index, value in enumerate(different_values) if value is False]
            rows_to_update.extend(update_index)

    distinct_rows = list(set(rows_to_update))

    different_rows = main_df.iloc[distinct_rows]



    return different_rows.to_dict("records")
    