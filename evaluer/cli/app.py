from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from evaluer.cli.generator import GradingConfigGenerator
from evaluer.clients.hive import HiveClient
from evaluer.core.settings import get_settings
from evaluer.core.models.hive import TokenObtainRequest
from evaluer.services.hive import HiveService


DEFAULT_OUTPUT_FILE = Path.joinpath(Path("config"), "weights.yaml")

app = typer.Typer(
    help="CLI for generating grading configurations from the Hive platform.",
    pretty_exceptions_show_locals=False,
)
console = Console()


@app.callback()
def main(ctx: typer.Context):
    ctx.obj = {"console": console}


@app.command()
def generate(
    ctx: typer.Context,
    output: Path = typer.Option(
        Path(DEFAULT_OUTPUT_FILE),
        "--output",
        "-o",
        help="Output file path for the YAML configuration.",
        writable=True,
        resolve_path=True,
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Overwrite existing file."
    ),
):
    """
    Generate a new grading_config.yaml from the Hive platform.
    """
    console = ctx.obj["console"]
    if output.exists() and not force:
        console.print(
            f"[bold red]❌ Error:[/] File [cyan]'{output}'[/cyan] already exists. Use [yellow]--force[/yellow] to overwrite."
        )
        raise typer.Exit(1)

    try:
        console.print(
            Panel(
                f"🚀 Starting configuration generation for [cyan]{output.name}[/cyan]",
                title="[bold blue]Evaluer Config Generator[/bold blue]",
                border_style="blue",
            )
        )
        settings = get_settings()
        hive_client = HiveClient(base_url=settings.hive.base_url)
        hive_client.authenticate(
            credentials=TokenObtainRequest(
                username=settings.hive.username, password=settings.hive.password
            )
        )
        hive_service = HiveService(hive_client)

        generator = GradingConfigGenerator(hive_service)
        config_data = generator.generate_config_skeleton()
        generator.save_config(config_data, output)

    except Exception as e:
        console.print(f"[bold red]❌ An unexpected error occurred:[/] {e}")
        raise typer.Exit(code=1)


def run():
    app()
