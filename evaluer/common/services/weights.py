from pathlib import Path
from typing import Dict
import yaml
from pydantic import BaseModel, Field


class WeightConfig(BaseModel):
    name: str
    weight: float = Field(default=1.0, ge=0.0)


class ExerciseWeightConfig(WeightConfig):
    pass


class ModuleWeightConfig(WeightConfig):
    exercises: Dict[int, ExerciseWeightConfig] = Field(default_factory=dict)


class SubjectWeightConfig(WeightConfig):
    modules: Dict[int, ModuleWeightConfig] = Field(default_factory=dict)


class WeightsConfiguration(BaseModel):
    subjects: Dict[int, SubjectWeightConfig] = Field(default_factory=dict)

    @classmethod
    def from_yaml(cls, config_path: str) -> "WeightsConfiguration":
        weights_file = Path(config_path)
        if not weights_file.exists():
            return cls()

        with weights_file.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        return cls(**data)


class WeightProvider:
    def __init__(self, weights_configuration: WeightsConfiguration):
        self._weights_configuration = weights_configuration

    def get_exercise_weights_for_module(self, module_id: int) -> Dict[int, float]:
        for subject in self._weights_configuration.subjects.values():
            if module_id in subject.modules:
                module_config = subject.modules[module_id]
                return {
                    exercise_id: exercise_config.weight
                    for exercise_id, exercise_config in module_config.exercises.items()
                }
        return {}

    def get_module_weights_for_subject(self, subject_id: int) -> Dict[int, float]:
        if subject_id in self._weights_configuration.subjects:
            subject_config = self._weights_configuration.subjects[subject_id]
            return {
                module_id: module_config.weight
                for module_id, module_config in subject_config.modules.items()
            }
        return {}

    def get_subject_weights(self) -> Dict[int, float]:
        return {
            subject_id: subject_config.weight
            for subject_id, subject_config in self._weights_configuration.subjects.items()
        }
