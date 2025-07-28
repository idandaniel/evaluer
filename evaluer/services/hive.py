from typing import List, Optional
from evaluer.clients.hive import HiveClient
from evaluer.services.cache import CacheService
from evaluer.models.hive import (
    Assignment,
    AssignmentResponse,
    CourseUser,
    ClearanceLevel,
    Subject,
    Module,
    Exercise,
)


CACHE_KEY_STUDENTS_CLEARANCE = "students_clearance:{clearance}"
CACHE_KEY_STUDENT_ASSIGNMENT = "student_assignment:{student_id}:{exercise_id}"
CACHE_KEY_ASSIGNMENT_RESPONSES = "assignment_responses:{assignment_id}"
CACHE_KEY_SUBJECTS = "subjects"
CACHE_KEY_MODULES_SUBJECT = "modules_subject:{subject_id}"
CACHE_KEY_EXERCISES_MODULE = "exercises_module:{module_id}"


class HiveService:
    def __init__(self, hive_client: HiveClient, cache_service: CacheService):
        self.hive_client = hive_client
        self.cache_service = cache_service

    def get_users_by_clearance(self, clearance: ClearanceLevel) -> List[CourseUser]:
        cache_key = CACHE_KEY_STUDENTS_CLEARANCE.format(clearance=clearance.value)
        cached_students = self.cache_service.get(cache_key)
        if cached_students:
            return [CourseUser.model_validate(student) for student in cached_students]

        students = self.hive_client.get_users_by_clearance(clearance=clearance)
        students_dict = [student.model_dump() for student in students]
        self.cache_service.set(cache_key, students_dict)
        return students

    def get_student_assignment_by_exercise(
        self, student_id: int, exercise_id: int
    ) -> Optional[Assignment]:
        cache_key = CACHE_KEY_STUDENT_ASSIGNMENT.format(
            student_id=student_id, exercise_id=exercise_id
        )
        cached_assignment = self.cache_service.get(cache_key)
        if cached_assignment:
            return Assignment.model_validate(cached_assignment)

        assignment = self.hive_client.get_student_assignment_by_exercise(
            student_id=student_id, exercise_id=exercise_id
        )
        if assignment:
            assignment_dict = assignment.model_dump()
            self.cache_service.set(cache_key, assignment_dict)
        return assignment

    def get_assignment_responses(self, assignment_id: int) -> List[AssignmentResponse]:
        cache_key = CACHE_KEY_ASSIGNMENT_RESPONSES.format(assignment_id=assignment_id)
        cached_responses = self.cache_service.get(cache_key)
        if cached_responses:
            return [
                AssignmentResponse.model_validate(response)
                for response in cached_responses
            ]

        responses = self.hive_client.get_assignment_responses(
            assignment_id=assignment_id
        )
        responses_dict = [response.model_dump() for response in responses]
        self.cache_service.set(cache_key, responses_dict)
        return responses

    def get_student_assignment(
        self, student_id: int, assignment_id: int
    ) -> Optional[Assignment]:
        return self.hive_client.get_student_assignment(
            student_id=student_id, assignment_id=assignment_id
        )

    def get_subjects(self) -> List[Subject]:
        cache_key = CACHE_KEY_SUBJECTS
        cached_subjects = self.cache_service.get(cache_key)
        if cached_subjects:
            return [Subject.model_validate(subject) for subject in cached_subjects]

        subjects = self.hive_client.get_subjects()
        subjects_dict = [subject.model_dump() for subject in subjects]
        self.cache_service.set(cache_key, subjects_dict)
        return subjects

    def get_modules_by_subject(self, subject_id: int) -> List[Module]:
        cache_key = CACHE_KEY_MODULES_SUBJECT.format(subject_id=subject_id)
        cached_modules = self.cache_service.get(cache_key)
        if cached_modules:
            return [Module.model_validate(module) for module in cached_modules]

        modules = self.hive_client.get_modules_by_subject(subject_id)
        modules_dict = [module.model_dump() for module in modules]
        self.cache_service.set(cache_key, modules_dict)
        return modules

    def get_exercises_by_module(self, module_id: int) -> List[Exercise]:
        cache_key = CACHE_KEY_EXERCISES_MODULE.format(module_id=module_id)
        cached_exercises = self.cache_service.get(cache_key)
        if cached_exercises:
            return [Exercise.model_validate(exercise) for exercise in cached_exercises]

        exercises = self.hive_client.get_exercises_by_module(module_id)
        exercises_dict = [exercise.model_dump() for exercise in exercises]
        self.cache_service.set(cache_key, exercises_dict)
        return exercises
