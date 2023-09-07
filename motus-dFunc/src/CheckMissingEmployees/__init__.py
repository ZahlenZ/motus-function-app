import pandas as pd

from SharedCode.Config import drop_columns
from SharedCode.Decorate import log_execution


@log_execution(func_name="CheckMissingEmployees")
def main(CheckMissingEmployees: list) -> dict:
    """Compares main_df from edw and sub_df from motus for any employees in main that aren't in sub

    Args:
        CheckMissingEmployees (list): [main_df, sub_df]

    Returns:
        dict: employees in main that aren't in sub
    """
    main = CheckMissingEmployees[0]
    sub = CheckMissingEmployees[1]

    main_df = pd.DataFrame(main)
    sub_df = pd.DataFrame(sub)

    merged_df = main_df.merge(
        sub_df, how="left", indicator=True, on="clientEmployeeId1"
    )

    merged_df = merged_df[merged_df["_merge"] == "left_only"]

    merged_df.rename(columns=drop_columns, inplace=True)
    columns_to_remove = merged_df.columns[merged_df.columns == "remove"]
    merged_df.drop(columns=columns_to_remove, inplace=True)

    merged_df.drop(["_merge"], axis=1, inplace=True)

    return merged_df.to_dict("records")
