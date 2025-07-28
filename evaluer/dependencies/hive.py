from functools import lru_cache

from fastapi import Depends

from evaluer.clients.hive import HiveClient
from evaluer.core.settings import get_settings
from evaluer.models.hive import TokenObtainRequest
from evaluer.services.hive import HiveService


@lru_cache()
def get_authenticated_hive_client() -> HiveClient:
    settings = get_settings()
    hive_client = HiveClient(base_url=settings.hive.base_url)
    hive_client.authenticate(
        credentials=TokenObtainRequest(
            username=settings.hive.username, password=settings.hive.password
        )
    )
    return hive_client


def get_hive_service(
    hive_client: HiveClient = Depends(get_authenticated_hive_client),
) -> HiveService:
    return HiveService(hive_client)
