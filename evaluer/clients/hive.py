from typing import Any, Dict, List, Optional

from evaluer.clients.base import AuthenticationStrategy, BaseAPIClient
from evaluer.core.models.hive import (
    Assignment,
    AssignmentResponse,
    ClearanceLevel,
    CourseUser,
    Exercise,
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
        auth_strategy = auth_strategy
        super().__init__(base_url, auth_strategy)

    def get_subjects(self) -> List[Subject]:
        response = self._make_request(method="GET", endpoint=self.SUBJECTS_ENDPOINT)
        subjects_data = response.json()
        return [Subject(**subject_data) for subject_data in subjects_data]

    def get_modules(self) -> List[Module]:
        response = self._make_request(method="GET", endpoint=self.MODULES_ENDPOINT)
        modules_data = response.json()
        return [Module(**module_data) for module_data in modules_data]

    def get_exercises(self) -> List[Exercise]:
        response = self._make_request(method="GET", endpoint=self.EXERCISES_ENDPOINT)
        exercises_data = response.json()
        return [Exercise(**exercise_data) for exercise_data in exercises_data]

    def get_modules_by_subject(self, subject_id: int) -> List[Module]:
        params = {"subject": subject_id}
        response = self._make_request(
            method="GET", endpoint=self.MODULES_ENDPOINT, params=params
        )
        modules_data = response.json()
        return [Module(**module_data) for module_data in modules_data]

    def get_exercises_by_module(self, module_id: int) -> List[Exercise]:
        params = {"parent_module": module_id}
        response = self._make_request(
            method="GET", endpoint=self.EXERCISES_ENDPOINT, params=params
        )
        exercises_data = response.json()
        return [Exercise(**exercise_data) for exercise_data in exercises_data]

    def get_users_by_clearance(self, clearance: ClearanceLevel) -> List[CourseUser]:
        params = {"clearance": clearance.value}
        response = self._make_request(
            method="GET", endpoint=self.USERS_ENDPOINT, params=params
        )
        users_data = response.json()
        return [
            CourseUser(**user_data) for user_data in users_data if user_data.get("id")
        ]

    def get_student_assignments(self, student_id: int) -> List[Assignment]:
        params = {"user__id__in": student_id}
        response = self._make_request(
            method="GET",
            endpoint=self.ASSIGNMENTS_ENDPOINT,
            params=params,
        )
        assignments_data = response.json()
        return [Assignment(**assignment_data) for assignment_data in assignments_data]

    def get_student_assignment(
        self, student_id: int, assignment_id: int
    ) -> Optional[Assignment]:
        params = {"user__id__in": student_id, "id": assignment_id}
        response = self._make_request(
            method="GET",
            endpoint=self.ASSIGNMENTS_ENDPOINT,
            params=params,
        )
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
        assignments_data = response.json()
        return Assignment(**assignments_data[0]) if assignments_data else None

    def get_assignments_for_students(self, student_ids: List[int]) -> List[Assignment]:
        params = {"user__id__in": ",".join(map(str, student_ids))}
        response = self._make_request(
            method="GET",
            endpoint=self.ASSIGNMENTS_ENDPOINT,
            params=params,
        )
        assignments_data = response.json()
        return [Assignment(**assignment_data) for assignment_data in assignments_data]

    def get_assignment(self, assignment_id: int) -> Assignment:
        endpoint = f"{self.ASSIGNMENTS_ENDPOINT}{assignment_id}/"
        response = self._make_request(method="GET", endpoint=endpoint)
        assignment_data = response.json()
        return Assignment(**assignment_data)

    def get_assignment_responses(self, assignment_id: int) -> List[AssignmentResponse]:
        endpoint = self.ASSIGNMENT_RESPONSES_ENDPOINT.format(
            assignment_id=assignment_id
        )
        response = self._make_request(method="GET", endpoint=endpoint)
        responses_data = response.json()
        return [AssignmentResponse(**response_data) for response_data in responses_data]

    def get_exercise_details(self, exercise_id: int) -> Exercise:
        endpoint = f"{self.EXERCISES_ENDPOINT}{exercise_id}/"
        response = self._make_request(method="GET", endpoint=endpoint)
        exercise_data = response.json()
        return Exercise(**exercise_data)

    def get_student_info(self, student_id: int) -> CourseUser:
        endpoint = f"{self.USERS_ENDPOINT}{student_id}/"
        response = self._make_request(method="GET", endpoint=endpoint)
        user_data = response.json()
        return CourseUser(**user_data)

    def get_student_info_raw(self, student_id: int) -> Dict[str, Any]:
        endpoint = f"{self.USERS_ENDPOINT}{student_id}/"
        response = self._make_request(method="GET", endpoint=endpoint)
        return response.json()

    def get_assignment_response(
        self, assignment_id: int, response_id: int
    ) -> Dict[str, Any]:
        endpoint = self.ASSIGNMENT_RESPONSE_ENDPOINT.format(
            assignment_id=assignment_id, response_id=response_id
        )
        response = self._make_request(method="GET", endpoint=endpoint)
        return response.json()

    def get_assignment_responses_files(
        self, assignment_id: int, response_id: int
    ) -> bytes:
        endpoint = self.ASSIGNMENT_RESPONSE_FILES_ENDPOINT.format(
            assignment_id=assignment_id, response_id=response_id
        )
        response = self._make_request(method="GET", endpoint=endpoint)
        return response.content

    def get_student_assignment_for_exercise(
        self, student_id: int, exercise_id: int
    ) -> List[Assignment]:
        params = {"user__id__in": [student_id], "exercise__id": exercise_id}
        response = self._make_request(
            method="GET",
            endpoint=self.ASSIGNMENTS_ENDPOINT,
            params=params,
        )
        assignments_data = response.json()
        return [Assignment(**assignment_data) for assignment_data in assignments_data]

    # def get_assignment_with_responses(
    #     self, assignment_id: int
    # ) -> Tuple[Assignment, List[AssignmentResponse]]:
    #     endpoint = f"{self.ASSIGNMENTS_ENDPOINT}{assignment_id}/"
    #     response = self._make_request(method="GET", endpoint=endpoint)
    #     assignment_data = response.json()
    #     assignment = Assignment(**assignment_data)
    #     responses = self.get_assignment_responses(assignment_id)
    #     return assignment, responses

    # def get_student_assignments_with_responses(
    #     self, student_id: int
    # ) -> List[Tuple[Assignment, List[AssignmentResponse]]]:
    #     assignments = self.get_student_assignments(student_id)
    #     assignments_with_responses = []

    #     for assignment in assignments:
    #         try:
    #             responses = self.get_assignment_responses(assignment.id)
    #         except Exception:
    #             responses = []
    #         assignments_with_responses.append((assignment, responses))

    #     return assignments_with_responses
