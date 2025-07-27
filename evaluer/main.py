import urllib3
import json

from evaluer.core.settings import settings
from evaluer.clients.hive import HiveClient
from evaluer.core.models import CourseTokenObtainPairRequest, ClearanceLevel


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    credentials = CourseTokenObtainPairRequest(
        username=settings.hive_username, password=settings.hive_password
    )
    hive_client = HiveClient(base_url=settings.hive_base_url)
    hive_client.authenticate(credentials)

    try:
        students = hive_client.get_users_by_clearance(ClearanceLevel.HANICH)
        all_student_data = []

        for student in students:
            student_data = {
                "student_id": student.id,
                "student_name": student.display_name,
                "username": student.username,
                "assignments": [],
            }

            assignments_with_responses = (
                hive_client.get_student_assignments_with_responses(student.id)
            )

            for assignment, responses in assignments_with_responses:
                assignment_data = {
                    "assignment_id": assignment.id,
                    "exercise_id": assignment.exercise,
                    "status": assignment.assignment_status,
                    "student_status": assignment.student_assignment_status,
                    "description": assignment.description,
                    "submission_count": assignment.submission_count,
                    "flagged": assignment.flagged,
                    "responses": [],
                }

                for response in responses:
                    print(
                        f"DEBUG: Processing response {response.id}, file_name: {response.file_name}"
                    )
                    response_data = {
                        "response_id": response.id,
                        "response_type": response.response_type,
                        "date": response.date.isoformat() if response.date else None,
                        "file_name": response.file_name,
                        "dear_student": response.dear_student,
                        "hide_checker_name": response.hide_checker_name,
                        "contents": [
                            {"field": content.field, "content": content.content}
                            for content in response.contents
                        ],
                        "files": [],
                    }

                    if response.file_name:
                        try:
                            file_content = hive_client.get_assignment_responses_files(
                                assignment.id, response.id
                            )
                            response_data["files"] = [
                                {
                                    "name": response.file_name,
                                    "available": True,
                                    "size_bytes": len(file_content),
                                }
                            ]
                        except Exception as e:
                            response_data["files"] = [
                                {
                                    "name": response.file_name,
                                    "available": False,
                                    "error": str(e),
                                }
                            ]

                    assignment_data["responses"].append(response_data)

                student_data["assignments"].append(assignment_data)

            all_student_data.append(student_data)

        all_student_data = [
            data for data in all_student_data if data.get("assignments")
        ]
        print(json.dumps(all_student_data, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
