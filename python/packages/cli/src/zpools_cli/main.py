import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from zpools import ZPoolsClient
from zpools._generated.api.authentication import get_hello
from zpools_cli.commands import zpool, sshkey, pat, job, billing, zfs
from zpools_cli.config import build_client_config
from zpools_cli.utils import format_error_response
from zpools_cli.shell_completion import completion_command

app = typer.Typer(no_args_is_help=True, add_completion=False)
app.add_typer(zpool.app, name="zpool")
app.add_typer(sshkey.app, name="sshkey")
app.add_typer(pat.app, name="pat")
app.add_typer(job.app, name="job")
app.add_typer(billing.app, name="billing")
app.add_typer(zfs.app, name="zfs")
console = Console()


@app.callback()
def main_callback(
    ctx: typer.Context,
    rcfile: Optional[Path] = typer.Option(
        None,
        "--rcfile",
        help="Path to zpoolrc config file (default: ~/.config/zpools.io/zpoolrc)",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True
    )
):
    """zpools.io CLI - Manage zpools, jobs, SSH keys, and billing."""
    # Build config once at startup and store in context
    ctx.obj = build_client_config(rc_file=rcfile)

@app.command()
def hello(ctx: typer.Context):
    """
    Test connectivity to the API.
    """
    try:
        from zpools_cli.utils import get_authenticated_client
        client = get_authenticated_client(ctx.obj)
        
        auth_client = client.get_authenticated_client()
        response = get_hello.sync_detailed(client=auth_client)
        
        if response.status_code == 200:
            console.print(f"[green]Success:[/green] {response.parsed.message}")
        else:
            error_msg = format_error_response(response.status_code, response.content, json_mode=False)
            console.print(f"[red]Error {response.status_code}:[/red] {error_msg}")
            
    except Exception as e:
        console.print(f"[red]An error occurred:[/red] {e}")

@app.command()
def version():
    """
    Show the CLI version.
    """
    console.print("zpools-cli v0.1.0")

@app.command()
def completion(
    shell: str = typer.Argument(None, help="Shell type: bash, zsh, fish, powershell"),
    install: bool = typer.Option(False, "--install", help="Install completion for current shell")
):
    """
    Generate shell completion script.
    
    Examples:
      zpools completion bash > ~/.zpools-completion.bash
      zpools completion --install  # Auto-detect and install
    """
    completion_command(shell, install)

if __name__ == "__main__":
    app()
