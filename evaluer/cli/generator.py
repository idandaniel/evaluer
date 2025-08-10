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

from evaluer.common.models.hive import BaseCourseComponent
from evaluer.common.clients.hive import HiveClient


GRADING_CONFIG_HEADER_COMMENT = """# Grading Configuration
#
# Hierarchical structure: Subject -> Module -> Exercise
#
# Rules:
# - All subject weights must sum to 1.0
# - All module weights within a subject must sum to 1.0  
# - All exercise weights within a module must sum to 1.0
# - Use decimal values (e.g., 0.4, not 40%)
# - Missing subjects/modules/exercises will use equal distribution
#
# Generated from current Hive platform data

"""


class GradingConfigGenerator:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def __init__(self, hive_client: HiveClient):
        self.hive_client = hive_client
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

            subjects = self.hive_client.get_subjects()
            progress.update(
                task_subjects, completed=1, description="[green]✓ Fetched Subjects"
            )

            modules = self.hive_client.get_modules()
            progress.update(
                task_modules, completed=1, description="[green]✓ Fetched Modules"
            )

            exercises = self.hive_client.get_exercises()
            progress.update(
                task_exercises, completed=1, description="[green]✓ Fetched Exercises"
            )

            task_generate = progress.add_task("[blue]Generating config...", total=1)
            hierarchical = self._generate_hierarchical_config(subjects, modules, exercises)
            config_data = {"subjects": hierarchical}
            time.sleep(0.25)
            progress.update(
                task_generate, completed=1, description="[bold green]✓ Config Generated"
            )
            time.sleep(0.5)

        self.console.print("[bold green]Generation complete.[/bold green]")
        return config_data

    def _generate_hierarchical_config(
        self, subjects: List[BaseCourseComponent], modules: List[BaseCourseComponent], exercises: List[BaseCourseComponent]
    ) -> Dict:
        """Generate a hierarchical configuration structure: subject -> module -> exercise"""
        
        modules_by_subject = {}
        for module in modules:
            if hasattr(module, 'parent_subject'):
                subject_id = module.parent_subject
                if subject_id not in modules_by_subject:
                    modules_by_subject[subject_id] = []
                modules_by_subject[subject_id].append(module)

        exercises_by_module = {}
        for exercise in exercises:
            if hasattr(exercise, 'parent_module'):
                module_id = exercise.parent_module
                if module_id not in exercises_by_module:
                    exercises_by_module[module_id] = []
                exercises_by_module[module_id].append(exercise)
        
        config_data = {}

        if subjects:
            subject_weight = round(1.0 / len(subjects), 2)
            
            for subject in subjects:
                subject_modules = modules_by_subject.get(subject.id, [])
                module_weight = round(1.0 / len(subject_modules), 2) if subject_modules else 1.0
                
                modules_config = {}
                for module in subject_modules:
                    module_exercises = exercises_by_module.get(module.id, [])
                    exercise_weight = round(1.0 / len(module_exercises), 2) if module_exercises else 1.0
                    
                    exercises_config = {}
                    for exercise in module_exercises:
                        exercises_config[exercise.id] = {
                            "name": exercise.name,
                            "weight": exercise_weight
                        }
                    
                    modules_config[module.id] = {
                        "name": module.name,
                        "weight": module_weight,
                        "exercises": exercises_config
                    }
                
                config_data[subject.id] = {
                    "name": subject.name,
                    "weight": subject_weight,
                    "modules": modules_config
                }
        
        return config_data

    def _generate_component_weights(
        self, components: List[BaseCourseComponent]
    ) -> Dict[int, Dict[str, any]]:
        if not components:
            return {}

        equal_weight = round(1.0 / len(components), 2)
        return {
            component.id: {"name": component.name, "weight": equal_weight}
            for component in components
        }

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
            f"   Remember that all weights within each hierarchy level must sum to [bold]1.0[/bold]:\n"
            f"   - Subject weights must sum to 1.0\n"
            f"   - Module weights within each subject must sum to 1.0\n"
            f"   - Exercise weights within each module must sum to 1.0"
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
