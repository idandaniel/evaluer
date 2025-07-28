import base64
import io
import mimetypes
import zipfile
from typing import List, Optional

from evaluer.clients.hive import HiveClient
from evaluer.core.models.hive import (
    Assignment,
    AssignmentResponse,
    AssignmentResponseFiles,
    ClearanceLevel,
    CourseUser,
    Exercise,
    FileInfo,
    Module,
    Subject,
)


class HiveService:
    def __init__(self, hive_client: HiveClient):
        self.hive_client = hive_client

    def get_users_by_clearance(self, clearance: ClearanceLevel) -> List[CourseUser]:
        return self.hive_client.get_users_by_clearance(clearance=clearance)

    def get_student_assignment_by_exercise(
        self, student_id: int, exercise_id: int
    ) -> Optional[Assignment]:
        return self.hive_client.get_student_assignment_by_exercise(
            student_id=student_id, exercise_id=exercise_id
        )

    def get_assignment_responses(self, assignment_id: int) -> List[AssignmentResponse]:
        return self.hive_client.get_assignment_responses(assignment_id=assignment_id)

    def get_student_assignment(
        self, student_id: int, assignment_id: int
    ) -> Optional[Assignment]:
        return self.hive_client.get_student_assignment(
            student_id=student_id, assignment_id=assignment_id
        )

    def get_subjects(self) -> List[Subject]:
        return self.hive_client.get_subjects()

    def get_modules(self) -> List[Module]:
        return self.hive_client.get_modules()

    def get_exercises(self) -> List[Exercise]:
        return self.hive_client.get_exercises()

    def get_modules_by_subject(self, subject_id: int) -> List[Module]:
        return self.hive_client.get_modules_by_subject(subject_id)

    def get_exercises_by_module(self, module_id: int) -> List[Exercise]:
        return self.hive_client.get_exercises_by_module(module_id)

    def get_assignment_response_files(
        self,
        assignment_id: int,
        response_id: int,
        response_filename: Optional[str] = None,
    ) -> AssignmentResponseFiles:
        try:
            student_files_bytes = self.hive_client.get_assignment_responses_files(
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
                filename = response_filename or "student_files"
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
