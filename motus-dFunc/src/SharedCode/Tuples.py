from collections import namedtuple

KVNames = namedtuple(
    "KVNames",
    [
        "kv_name",
        "kv_user",
        "kv_password",
        "db_name",
        "db_user",
        "db_pass",
        "db_host",
        "db_port",
    ],
)

Endpoints = namedtuple(
    "Endpoints", ["get_token", "get_drivers", "post_driver", "update_driver"]
)
