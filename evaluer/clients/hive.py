from typing import Any, Dict, List, Optional, Tuple

from evaluer.clients.base import BaseAPIClient, AuthenticationStrategy
from evaluer.core.models import (
    Assignment,
    AssignmentResponse,
    ClearanceLevel,
    CourseTokenObtainPair,
    CourseTokenObtainPairRequest,
    CourseUser,
    Exercise,
)


class HiveAuthenticationStrategy(AuthenticationStrategy[CourseTokenObtainPair]):

    def get_auth_endpoint(self) -> str:
        return "/api/core/token/"

    def prepare_auth_payload(self, credentials: CourseTokenObtainPairRequest) -> Dict[str, Any]:
        return credentials.model_dump()

    def prepare_auth_headers(self) -> Dict[str, str]:
        return {"Content-Type": "application/json"}

    def parse_token_response(self, response_data: Dict[str, Any]) -> CourseTokenObtainPair:
        return CourseTokenObtainPair(**response_data)

    def get_authorization_header(self, token: CourseTokenObtainPair) -> str:
        return f"Bearer {token.access}"


class HiveClient(BaseAPIClient[CourseTokenObtainPair]):
    ASSIGNMENTS_ENDPOINT = "/api/core/assignments/"
    USERS_ENDPOINT = "/api/core/management/users/"
    EXERCISES_ENDPOINT = "/api/core/course/exercises/"
    ASSIGNMENT_RESPONSES_ENDPOINT = "/api/core/assignments/{assignment_id}/responses/"
    ASSIGNMENT_RESPONSE_ENDPOINT = (
        "/api/core/assignments/{assignment_id}/responses/{response_id}/"
    )
    ASSIGNMENT_RESPONSE_FILES_ENDPOINT = (
        "/api/core/assignments/{assignment_id}/responses/{response_id}/student_files/"
    )
    UPDATE_RESPONSE_GRADE_ENDPOINT = "/api/core/assignments/responses/{response_id}/"

    def __init__(
        self,
        base_url: str = "https://localhost",
        auth_strategy: Optional[
            AuthenticationStrategy[CourseTokenObtainPair]
        ] = HiveAuthenticationStrategy(),
    ):
        auth_strategy = auth_strategy
        super().__init__(base_url, auth_strategy)

    def _create_assignment(self, assignment_data: dict) -> Assignment:
        return Assignment(**assignment_data)

    def get_users_by_clearance(self, clearance: ClearanceLevel) -> List[CourseUser]:
        params = {"clearance": clearance.value}
        response = self._make_request(
            method="GET", endpoint=self.USERS_ENDPOINT, params=params
        )
        users_data = response.json()
        return [CourseUser(**user_data) for user_data in users_data if user_data.get("id")]

    def get_student_assignments(self, student_id: int) -> List[Assignment]:
        params = {"user__id__in": student_id}

        response = self._make_request(
            method="GET",
            endpoint=self.ASSIGNMENTS_ENDPOINT,
            params=params,
        )
        assignments_data = response.json()
        return [
            self._create_assignment(assignment_data=assignment_data)
            for assignment_data in assignments_data
        ]

    def get_assignments_for_students(self, student_ids: List[int]) -> List[Assignment]:
        params = {"user__id__in": ",".join(map(str, student_ids))}

        response = self._make_request(
            method="GET",
            endpoint=self.ASSIGNMENTS_ENDPOINT,
            params=params,
        )
        assignments_data = response.json()
        return [
            self._create_assignment(assignment_data=assignment_data)
            for assignment_data in assignments_data
        ]

    def get_assignment(self, assignment_id: int) -> Assignment:
        endpoint = f"{self.ASSIGNMENTS_ENDPOINT}{assignment_id}/"
        response = self._make_request(method="GET", endpoint=endpoint)
        assignment_data = response.json()
        return self._create_assignment(assignment_data)

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

    def update_assignment_response_grade(
        self,
        response_id: int,
        grading_status: str,
        grade: Optional[int],
        feedback: Optional[str],
    ) -> None:
        endpoint = self.UPDATE_RESPONSE_GRADE_ENDPOINT.format(response_id=response_id)

        payload = {
            "grading_status": grading_status,
            "manual_grade": grade,
            "feedback": feedback,
        }

        self._make_request(method="PUT", endpoint=endpoint, json=payload)

    def get_assignment_response(self, assignment_id: int, response_id: int) -> Dict[str, Any]:
        endpoint = self.ASSIGNMENT_RESPONSE_ENDPOINT.format(assignment_id=assignment_id, response_id=response_id)
        response = self._make_request(method="GET", endpoint=endpoint)
        return response.json()

    def get_assignment_responses_files(self, assignment_id: int, response_id: int) -> bytes:
        endpoint = self.ASSIGNMENT_RESPONSE_FILES_ENDPOINT.format(
            assignment_id=assignment_id, response_id=response_id
        )
        response = self._make_request(method="GET", endpoint=endpoint)
        return response.content

    def get_assignment_with_responses(self, assignment_id: int) -> Tuple[Assignment, List[AssignmentResponse]]:
        endpoint = f"{self.ASSIGNMENTS_ENDPOINT}{assignment_id}/"
        response = self._make_request(method="GET", endpoint=endpoint)
        assignment_data = response.json()
        assignment = self._create_assignment(assignment_data)
        
        responses = self.get_assignment_responses(assignment_id)
        
        return assignment, responses

    def get_student_assignments_with_responses(self, student_id: int) -> List[Tuple[Assignment, List[AssignmentResponse]]]:
        assignments = self.get_student_assignments(student_id)
        assignments_with_responses = []
        
        for assignment in assignments:
            try:
                responses = self.get_assignment_responses(assignment.id)
            except Exception:
                responses = []
            assignments_with_responses.append((assignment, responses))
            
        return assignments_with_responses
