import pandas as pd
from sqlalchemy import create_engine, select, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from SharedCode.Config import edw_columns
from SharedCode.Decorate import log_execution


@log_execution(func_name="GetMainDF")
def main(GetMainDF: dict) -> dict:
    """Acquire main df to compare to from edw

    args:
        GetMainDF (dict): parameters

    Returns:
        dict: employee dict from edw
    """
    edw_credentials = GetMainDF["edw_credentials"]
    # NOTE: Check address, city, state, zip actual column names
    query = text(
        """
        SELECT 
            employee_id
            ,group_id
            ,first_name
            ,last_name
            ,street_address 
            ,city
            ,state
            ,zip_code
            ,COALESCE(work_email, personal_email) AS work_email
            ,motus_start_date
            ,motus_end_date
            ,work_loc_code
            ,work_loc_desc
        FROM adp.stg_hr_workers
        WHERE motus_start_date IS NOT NULL AND group_id IS NOT NULL
        """
    )
    driver = edw_credentials["driver"]
    host = edw_credentials["host"]
    db_name = edw_credentials["db_name"]
    user = edw_credentials["user"]
    password = edw_credentials["password"]

    connection_string = (
        f"Driver={driver};Server={host};Database={db_name};Uid={user};Pwd={password}"
    )
    connection_url = URL.create(
        "mssql+pyodbc", query={"odbc_connect": connection_string}
    )

    engine = create_engine(connection_url, echo=False)
    Session = sessionmaker(bind=engine)

    with Session.begin() as session:
        result = session.execute(query)
        rows = result.fetchall()
        employee_df = pd.DataFrame(rows)

    employee_df = employee_df.rename(columns=edw_columns)

    return employee_df.to_dict()
