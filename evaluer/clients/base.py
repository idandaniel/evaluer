from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, TypeVar
from urllib.parse import urljoin

import requests

from evaluer.core.models import CourseTokenObtainPairRequest

T = TypeVar("T")


class AuthenticationStrategy(ABC, Generic[T]):

    @abstractmethod
    def get_auth_endpoint(self) -> str:
        pass

    @abstractmethod
    def prepare_auth_payload(self, credentials: CourseTokenObtainPairRequest) -> Dict[str, Any]:
        pass

    @abstractmethod
    def prepare_auth_headers(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def parse_token_response(self, response_data: Dict[str, Any]) -> T:
        pass

    @abstractmethod
    def get_authorization_header(self, token: T) -> str:
        pass


class BaseAPIClient(Generic[T]):

    def __init__(
        self,
        base_url: str,
        auth_strategy: AuthenticationStrategy[T],
    ):
        self.base_url = base_url
        self.auth_strategy = auth_strategy
        self._session: Optional[requests.Session] = None
        self._token: Optional[T] = None

    def authenticate(self, credentials: CourseTokenObtainPairRequest) -> None:
        self._token = self._login(credentials)
        self._session = requests.Session()
        auth_header = self.auth_strategy.get_authorization_header(self._token)
        self._session.headers.update({"Authorization": auth_header})

    def _login(self, credentials: CourseTokenObtainPairRequest) -> T:
        endpoint = self.auth_strategy.get_auth_endpoint()
        headers = self.auth_strategy.prepare_auth_headers()
        payload = self.auth_strategy.prepare_auth_payload(credentials)

        response = self._make_unauthenticated_request(
            method="POST", endpoint=endpoint, json=payload, headers=headers
        )
        response.raise_for_status()
        return self.auth_strategy.parse_token_response(response.json())

    def _make_unauthenticated_request(
        self,
        method: str,
        endpoint: str,
        **kwargs,
    ) -> requests.Response:
        url = urljoin(self.base_url, endpoint)
        request_kwargs = {
            "verify": False,
            **kwargs,
        }
        response = requests.request(method, url, **request_kwargs)
        response.raise_for_status()
        return response

    def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs,
    ) -> requests.Response:
        if not self._session:
            raise ValueError("Client must be authenticated before making requests")

        url = urljoin(self.base_url, endpoint)
        request_kwargs = {
            "verify": False,
            **kwargs,
        }
        response = self._session.request(method, url, **request_kwargs)
        response.raise_for_status()
        return response

    @property
    def session(self) -> requests.Session:
        if not self._session:
            raise ValueError("Client must be authenticated before accessing session")
        return self._session

    @property
    def token(self) -> T:
        if not self._token:
            raise ValueError("Client must be authenticated before accessing token")
        return self._token

    def is_authenticated(self) -> bool:
        return self._session is not None and self._token is not None
