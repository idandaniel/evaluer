from typing import Annotated

from fastapi import Depends

from evaluer.common.services.weights import WeightProvider, WeightsConfiguration
from evaluer.common.settings import Settings, get_settings


def get_weights_configuration(
    settings: Settings = Depends(get_settings),
) -> WeightsConfiguration:
    return WeightsConfiguration.from_yaml(str(settings.grading.weights_config_path))


def get_weight_provider(
    weights: Annotated[WeightsConfiguration, Depends(get_weights_configuration)],
) -> WeightProvider:
    return WeightProvider(weights)
