from pathlib import Path
from typing import Dict, List

import yaml
from pydantic import BaseModel, Field


class WeightConfig(BaseModel):
    name: str
    weight: float = Field(default=1.0, ge=0.0)


class WeightsConfiguration(BaseModel):
    subject: Dict[int, WeightConfig] = Field(default_factory=dict)
    module: Dict[int, WeightConfig] = Field(default_factory=dict)
    exercise: Dict[int, WeightConfig] = Field(default_factory=dict)

    @classmethod
    def from_yaml(cls, config_path: str) -> "WeightsConfiguration":
        weights_file = Path(config_path)
        if not weights_file.exists():
            return cls()

        with weights_file.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}

        return cls(**data)


class WeightProvider:
    def __init__(self, weights_configuration: WeightsConfiguration):
        self._weights_configuration = weights_configuration

    def get_weights_for_items(
        self, item_type: str, item_ids: List[int]
    ) -> Dict[int, float]:
        if not item_ids:
            return {}
        
        if item_type == "exercise":
            weights_dict = self._weights_configuration.exercise
        elif item_type == "module":
            weights_dict = self._weights_configuration.module
        elif item_type == "subject":
            weights_dict = self._weights_configuration.subject
        else:
            raise ValueError("Invalid weight item type")

        return {
            item_id: weight_config.weight
            for item_id, weight_config in weights_dict.items()
        }
