from enum import Enum


class Tag(Enum):
    user = "Current user endpoints."
    account = "Account"
    session = "Session"
    monitoring = "Monitoring"


tags_metadata = [
    {
        "name": Tag.user.value,
        "description": "Current user endpoints.",
    },
    {
        "name": Tag.account.value,
        "description": "Account endpoints.",
    },
    {
        "name": Tag.account.value,
        "description": "Session endpoints.",
    },
    {
        "name": Tag.monitoring.value,
        "description": "Monitoring endpoints.",
    },
]
