import base64
import io
import mimetypes
import zipfile
from typing import Any, Dict, List, Literal, Optional

import urllib3

from evaluer.common.clients.base import AuthenticationStrategy, BaseAPIClient
from evaluer.common.models.hive import (
    Assignment,
    AssignmentResponse,
    AssignmentResponseFiles,
    ClearanceLevel,
    CourseUser,
    Exercise,
    FileInfo,
    Module,
    Subject,
    TokenObtainRequest,
    TokenObtainResponse,
)


class HiveAuthenticationStrategy(AuthenticationStrategy[TokenObtainResponse]):

    def get_auth_endpoint(self) -> str:
        return "/api/core/token/"

    def prepare_auth_payload(self, credentials: TokenObtainRequest) -> Dict[str, Any]:
        return credentials.model_dump()

    def prepare_auth_headers(self) -> Dict[str, str]:
        return {"Content-Type": "application/json"}

    def parse_token_response(
        self, response_data: Dict[str, Any]
    ) -> TokenObtainResponse:
        return TokenObtainResponse(**response_data)

    def get_authorization_header(self, token: TokenObtainResponse) -> str:
        return f"Bearer {token.access}"


HiveResourceType = Literal[
    "user", "assignment", "assignment_response", "exercise", "module", "subject"
]


class HiveClient(BaseAPIClient[TokenObtainResponse]):
    USERS_ENDPOINT = "/api/core/management/users/"
    EXERCISES_ENDPOINT = "/api/core/course/exercises/"
    SUBJECTS_ENDPOINT = "/api/core/course/subjects/"
    MODULES_ENDPOINT = "/api/core/course/modules/"
    ASSIGNMENTS_ENDPOINT = "/api/core/assignments/"
    ASSIGNMENT_RESPONSES_ENDPOINT = "/api/core/assignments/{assignment_id}/responses/"
    ASSIGNMENT_RESPONSE_ENDPOINT = (
        "/api/core/assignments/{assignment_id}/responses/{response_id}/"
    )
    ASSIGNMENT_RESPONSE_FILES_ENDPOINT = (
        "/api/core/assignments/{assignment_id}/responses/{response_id}/student_files/"
    )

    def __init__(
        self,
        base_url: str,
        auth_strategy: Optional[
            AuthenticationStrategy[TokenObtainResponse]
        ] = HiveAuthenticationStrategy(),
    ):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        auth_strategy = auth_strategy
        super().__init__(base_url, auth_strategy)

    def get_subjects(self) -> List[Subject]:
        response = self._make_request(method="GET", endpoint=self.SUBJECTS_ENDPOINT)
        response.raise_for_status()
        subjects_data = response.json()
        return [Subject(**subject_data) for subject_data in subjects_data]

    def get_modules(self) -> List[Module]:
        response = self._make_request(method="GET", endpoint=self.MODULES_ENDPOINT)
        response.raise_for_status()
        modules_data = response.json()
        return [Module(**module_data) for module_data in modules_data]

    def get_exercises(self) -> List[Exercise]:
        response = self._make_request(method="GET", endpoint=self.EXERCISES_ENDPOINT)
        response.raise_for_status()
        exercises_data = response.json()
        return [Exercise(**exercise_data) for exercise_data in exercises_data]

    def get_modules_by_subject(self, subject_id: int) -> List[Module]:
        params = {"parent_subject__id": subject_id}
        response = self._make_request(
            method="GET", endpoint=self.MODULES_ENDPOINT, params=params
        )
        response.raise_for_status()
        modules_data = response.json()
        return [Module(**module_data) for module_data in modules_data]

    def get_exercises_by_module(self, module_id: int) -> List[Exercise]:
        params = {"parent_module__id": module_id}
        response = self._make_request(
            method="GET", endpoint=self.EXERCISES_ENDPOINT, params=params
        )
        response.raise_for_status()
        exercises_data = response.json()
        return [Exercise(**exercise_data) for exercise_data in exercises_data]

    def get_users_by_clearance(self, clearance: ClearanceLevel) -> List[CourseUser]:
        params = {"clearance__in": clearance.value}
        response = self._make_request(
            method="GET", endpoint=self.USERS_ENDPOINT, params=params
        )
        response.raise_for_status()
        users_data = response.json()
        return [
            CourseUser(**user_data) for user_data in users_data if user_data.get("id")
        ]

    def get_student_assignment(
        self, student_id: int, assignment_id: int
    ) -> Optional[Assignment]:
        params = {"user__id__in": student_id, "id": assignment_id}
        response = self._make_request(
            method="GET",
            endpoint=self.ASSIGNMENTS_ENDPOINT,
            params=params,
        )
        response.raise_for_status()
        assignments_data = response.json()
        return Assignment(**assignments_data[0]) if assignments_data else None

    def get_student_assignment_by_exercise(
        self, student_id: int, exercise_id: int
    ) -> Optional[Assignment]:
        params = {"user__id__in": [student_id], "exercise__id": exercise_id}
        response = self._make_request(
            method="GET",
            endpoint=self.ASSIGNMENTS_ENDPOINT,
            params=params,
        )
        response.raise_for_status()
        assignments_data = response.json()
        return Assignment(**assignments_data[0]) if assignments_data else None

    def get_assignment_responses(self, assignment_id: int) -> List[AssignmentResponse]:
        endpoint = self.ASSIGNMENT_RESPONSES_ENDPOINT.format(
            assignment_id=assignment_id
        )
        response = self._make_request(method="GET", endpoint=endpoint)
        response.raise_for_status()
        responses_data = response.json()
        responses = []
        for response_data in responses_data:
            response_data["assignment_id"] = assignment_id
            responses.append(AssignmentResponse(**response_data))
        return responses

    def get_assignments(self) -> List[Assignment]:
        response = self._make_request(
            method="GET",
            endpoint=self.ASSIGNMENTS_ENDPOINT,
        )
        response.raise_for_status()
        assignments_data = response.json()
        return [Assignment(**assignment) for assignment in assignments_data]

    def get_assignment_response(
        self, assignment_id: int, response_id: int
    ) -> AssignmentResponse:
        endpoint = self.ASSIGNMENT_RESPONSE_ENDPOINT.format(
            assignment_id=assignment_id, response_id=response_id
        )
        response = self._make_request(method="GET", endpoint=endpoint)
        response.raise_for_status()
        response_data = response.json()
        response_data["assignment_id"] = assignment_id
        return AssignmentResponse(**response_data)

    def get_assignment_responses_files(
        self, assignment_id: int, response_id: int
    ) -> bytes:
        endpoint = self.ASSIGNMENT_RESPONSE_FILES_ENDPOINT.format(
            assignment_id=assignment_id, response_id=response_id
        )
        response = self._make_request(method="GET", endpoint=endpoint)
        response.raise_for_status()
        return response.content

    def get_assignment_response_files(
        self, assignment_id: int, response_id: int
    ) -> List[AssignmentResponseFiles]:
        try:
            student_files_bytes = self.get_assignment_responses_files(
                assignment_id=assignment_id, response_id=response_id
            )

            if not student_files_bytes:
                return AssignmentResponseFiles(
                    response_id=response_id,
                    files=[],
                    has_files=False,
                    total_size=0,
                )

            files = []
            total_size = len(student_files_bytes)

            try:
                with zipfile.ZipFile(io.BytesIO(student_files_bytes), "r") as zip_file:
                    for file_info in zip_file.infolist():
                        if file_info.is_dir():
                            continue

                        file_content = zip_file.read(file_info.filename)
                        content = base64.b64encode(file_content).decode("utf-8")
                        mime_type, _ = mimetypes.guess_type(file_info.filename)

                        files.append(
                            FileInfo(
                                name=file_info.filename,
                                size=file_info.file_size,
                                content=content,
                                mime_type=mime_type or "application/octet-stream",
                            )
                        )

            except zipfile.BadZipFile:
                assignment_response = self.get_assignment_response(
                    assignment_id=assignment_id, response_id=response_id
                )
                filename = assignment_response.file_name or "student_file"
                content = base64.b64encode(student_files_bytes).decode("utf-8")
                mime_type, _ = mimetypes.guess_type(filename)

                files.append(
                    FileInfo(
                        name=filename,
                        size=len(student_files_bytes),
                        content=content,
                        mime_type=mime_type or "application/octet-stream",
                    )
                )

            return AssignmentResponseFiles(
                response_id=response_id,
                files=files,
                has_files=len(files) > 0,
                total_size=total_size,
            )

        except Exception:
            return AssignmentResponseFiles(
                response_id=response_id,
                files=[],
                has_files=False,
                total_size=0,
            )

    def get_assignment_by_id(self, assignment_id: int) -> Assignment:
        endpoint = f"{self.ASSIGNMENTS_ENDPOINT}{assignment_id}/"
        response = self._make_request(method="GET", endpoint=endpoint)
        response.raise_for_status()
        assignment_data = response.json()
        assignment_data["exercise_id"] = assignment_data.get(
            "exercise", assignment_data.get("exercise_id")
        )
        return Assignment(**assignment_data)

    def get_module_by_id(self, module_id: int) -> Module:
        endpoint = f"{self.MODULES_ENDPOINT}{module_id}/"
        response = self._make_request(method="GET", endpoint=endpoint)
        response.raise_for_status()
        module_data = response.json()
        module_data["subject_id"] = module_data.get(
            "parent_subject", module_data.get("subject_id")
        )
        return Module(**module_data)

    def get_response_by_id(self, response_id: int) -> AssignmentResponse:
        assignments_response = self._make_request(
            method="GET", endpoint=self.ASSIGNMENTS_ENDPOINT
        )
        assignments_response.raise_for_status()
        assignments_data = assignments_response.json()

        for assignment in assignments_data:
            assignment_id = assignment["id"]
            responses_endpoint = self.ASSIGNMENT_RESPONSES_ENDPOINT.format(
                assignment_id=assignment_id
            )
            try:
                responses_response = self._make_request(
                    method="GET", endpoint=responses_endpoint
                )
                responses_response.raise_for_status()
                responses_data = responses_response.json()

                for response_data in responses_data:
                    if response_data["id"] == response_id:
                        response_data["assignment_id"] = assignment_id
                        return AssignmentResponse(**response_data)
            except Exception:
                continue

        raise ValueError(f"Response with ID {response_id} not found")

    def get_exercise_by_id(self, exercise_id: int) -> Exercise:
        endpoint = f"{self.EXERCISES_ENDPOINT}{exercise_id}/"
        response = self._make_request(method="GET", endpoint=endpoint)
        response.raise_for_status()
        exercise_data = response.json()
        exercise_data["module_id"] = exercise_data.get(
            "parent_module", exercise_data.get("module_id")
        )
        return Exercise(**exercise_data)

    def is_resource_exist(
        self, resource_type: HiveResourceType, resource_id: int, **kwargs
    ) -> bool:
        endpoint_patterns = {
            "user": f"{self.USERS_ENDPOINT}{resource_id}/",
            "assignment": f"{self.ASSIGNMENTS_ENDPOINT}{resource_id}/",
            "exercise": f"{self.EXERCISES_ENDPOINT}{resource_id}/",
            "module": f"{self.MODULES_ENDPOINT}{resource_id}/",
            "subject": f"{self.SUBJECTS_ENDPOINT}{resource_id}/",
            "assignment_response": (
                self.ASSIGNMENT_RESPONSE_ENDPOINT.format(
                    assignment_id=kwargs.get("assignment_id"), response_id=resource_id
                )
                if kwargs.get("assignment_id")
                else None
            ),
        }

        endpoint = endpoint_patterns.get(resource_type)
        if not endpoint:
            return False

        try:
            response = self._make_request(method="GET", endpoint=endpoint)
            return response.ok
        except Exception:
            return False
