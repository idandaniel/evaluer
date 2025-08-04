from http import HTTPStatus
from typing import Any, Dict, Tuple

from fastapi import Depends, HTTPException

from evaluer.common.clients.hive import HiveClient
from evaluer.common.models.hive import TokenObtainRequest
from evaluer.common.settings import Settings, get_settings


def get_hive_client(settings: Settings = Depends(get_settings)) -> HiveClient:
    hive_client = HiveClient(base_url=settings.hive.base_url)
    hive_client.authenticate(
        credentials=TokenObtainRequest(
            username=settings.hive.username,
            password=settings.hive.password,
        )
    )
    return hive_client


class HiveResourceValidation:

    def __init__(
        self, resource_type: str, field_name: str, depends_on: Dict[str, Any] = None
    ):
        self.resource_type = resource_type
        self.field_name = field_name
        self.depends_on = depends_on or {}


def validate_hive_resources(
    request_dict: Dict[str, Any],
    hive_client: HiveClient,
    validations: Tuple[HiveResourceValidation, ...],
):
    for validation in validations:
        resource_id = request_dict.get(validation.field_name)
        if resource_id is None:
            continue

        kwargs = {}
        for dep_field, dep_value in validation.depends_on.items():
            if isinstance(dep_value, str) and dep_value.startswith("field:"):
                field_ref = dep_value.replace("field:", "")
                kwargs[dep_field] = request_dict.get(field_ref)
            else:
                kwargs[dep_field] = dep_value

        if not hive_client.is_resource_exist(
            validation.resource_type, resource_id, **kwargs
        ):
            field_display_name = (
                validation.field_name.replace("_id", "").replace("_", " ").title()
            )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"{field_display_name} with ID {resource_id} does not exist.",
            )
