import time
from pathlib import Path
from typing import Dict, List

import urllib3
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.text import Text

from evaluer.models.hive import BaseCourseComponent
from evaluer.services.hive import HiveService


GRADING_CONFIG_HEADER_COMMENT = """# Grading Configuration
#
# Rules:
# - All subject weights must sum to 1.0
# - All module weights within a subject must sum to 1.0
# - Use l values (e.g., 0.4, not 40%)
# - Missing subjects/modules will use equal distribution
#
# Generated from current Hive platform data

"""


class GradingConfigGenerator:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def __init__(self, hive_service: HiveService):
        self.hive_service = hive_service
        self.console = Console()

    def generate_config_skeleton(self) -> Dict:
        config_data = {}
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}", justify="right"),
            BarColumn(bar_width=None),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self.console,
            transient=True,
        ) as progress:

            task_subjects = progress.add_task("[cyan]Fetching subjects...", total=1)
            task_modules = progress.add_task("[magenta]Fetching modules...", total=1)
            task_exercises = progress.add_task("[yellow]Fetching exercises...", total=1)

            subjects = self.hive_service.get_subjects()
            progress.update(
                task_subjects, completed=1, description="[green]✓ Fetched Subjects"
            )

            modules = self.hive_service.get_modules()
            progress.update(
                task_modules, completed=1, description="[green]✓ Fetched Modules"
            )

            exercises = self.hive_service.get_exercises()
            progress.update(
                task_exercises, completed=1, description="[green]✓ Fetched Exercises"
            )

            task_generate = progress.add_task("[blue]Generating config...", total=1)
            config_data = {
                "grading": {
                    "weights": {
                        "subject": self._generate_weights(subjects),
                        "module": self._generate_weights(modules),
                        "exercise": self._generate_weights(exercises),
                    }
                }
            }
            time.sleep(0.25)
            progress.update(
                task_generate, completed=1, description="[bold green]✓ Config Generated"
            )
            time.sleep(0.5)

        self.console.print("[bold green]Generation complete.[/bold green]")
        return config_data

    def _generate_weights(
        self, components: List[BaseCourseComponent]
    ) -> Dict[str, float]:
        if not components:
            return {}

        equal_weight = 1.0 / len(components)
        return {component.name: equal_weight for component in components}

    def save_config(self, config_data: Dict, output_path: Path):
        yaml_str = yaml.dump(
            config_data,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
        )
        output_path.write_text(
            GRADING_CONFIG_HEADER_COMMENT + yaml_str, encoding="utf-8"
        )

        success_message = Text.from_markup(
            f"[bold green]✅ Configuration saved to: [cyan]{output_path}[/cyan][/bold green]\n\n"
            f"📝 [yellow]Next steps:[/] Edit the weights in the file as needed.\n"
            f"   Remember that all weights for a given category (subject, module, etc.) must sum to [bold]1.0[/bold]."
        )
        self.console.print(
            Panel(
                success_message,
                title="[bold bright_magenta]Success![/bold bright_magenta]",
                border_style="green",
                expand=False,
                padding=(1, 2),
            )
        )
