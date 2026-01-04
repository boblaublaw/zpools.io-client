import typer
import os
from rich.console import Console

console = Console()


def completion_command(
    shell: str = typer.Argument(None, help="Shell type: bash, zsh, fish, powershell"),
    install: bool = typer.Option(False, "--install", help="Install completion for current shell")
):
    """
    Generate shell completion script.
    
    Examples:
      zpools completion bash > ~/.zpools-completion.bash
      zpools completion --install  # Auto-detect and install
    """
    import subprocess
    
    if install:
        # Auto-detect shell from environment
        detected_shell = None
        
        # Try SHELL environment variable first
        shell_env = os.environ.get('SHELL', '')
        if 'bash' in shell_env:
            detected_shell = 'bash'
        elif 'zsh' in shell_env:
            detected_shell = 'zsh'
        elif 'fish' in shell_env:
            detected_shell = 'fish'
        
        # Fallback to parent process detection
        if not detected_shell:
            try:
                shell_path = subprocess.check_output(["ps", "-p", str(os.getppid()), "-o", "comm="]).decode().strip()
                if "bash" in shell_path:
                    detected_shell = "bash"
                elif "zsh" in shell_path:
                    detected_shell = "zsh"
                elif "fish" in shell_path:
                    detected_shell = "fish"
            except:
                pass
        
        if not detected_shell:
            console.print("[red]Could not detect shell. Please specify: bash, zsh, or fish[/red]")
            console.print("Usage: zpools completion bash --install")
            raise typer.Exit(1)
        
        shell = detected_shell
        console.print(f"[blue]Installing completion for {shell}...[/blue]")
    
    if not shell:
        console.print("[yellow]Please specify shell type or use --install[/yellow]")
        console.print("Examples:")
        console.print("  zpools completion bash > ~/.zpools-completion.bash")
        console.print("  zpools completion --install")
        raise typer.Exit(1)
    
    shell = shell.lower()
    if shell not in ["bash", "zsh", "fish", "powershell"]:
        console.print(f"[red]Unsupported shell: {shell}[/red]")
        console.print("Supported shells: bash, zsh, fish, powershell")
        raise typer.Exit(1)
    
    # Generate completion script using typer's built-in functionality
    try:
        # Use click's completion
        if shell == "bash":
            completion_script = """
_zpcli_completion() {
    local IFS=$'\\n'
    local response

    response=$(env COMP_WORDS="${COMP_WORDS[*]}" \\
                   COMP_CWORD=$COMP_CWORD \\
                   _ZPCLI_COMPLETE=complete_bash $1)

    for completion in $response; do
        IFS=',' read type value <<< "$completion"

        if [[ $type == 'dir' ]]; then
            COMPREPLY=()
            compopt -o dirnames
        elif [[ $type == 'file' ]]; then
            COMPREPLY=()
            compopt -o default
        elif [[ $type == 'plain' ]]; then
            COMPREPLY+=($value)
        fi
    done

    return 0
}

complete -o nosort -F _zpcli_completion zpcli
"""
        elif shell == "zsh":
            completion_script = """
#compdef zpcli

_zpcli_completion() {
    local -a completions
    local -a completions_with_descriptions
    local -a response
    (( ! $+commands[zpcli] )) && return 1

    response=("${(@f)$(env COMP_WORDS="${words[*]}" COMP_CWORD=$((CURRENT-1)) _ZPCLI_COMPLETE=complete_zsh zpcli)}")

    for type key descr in ${response}; do
        if [[ "$type" == "plain" ]]; then
            if [[ "$descr" == "_" ]]; then
                completions+=("$key")
            else
                completions_with_descriptions+=("$key":"$descr")
            fi
        elif [[ "$type" == "dir" ]]; then
            _path_files -/
        elif [[ "$type" == "file" ]]; then
            _path_files -f
        fi
    done

    if [ -n "$completions_with_descriptions" ]; then
        _describe -V unsorted completions_with_descriptions -U
    fi

    if [ -n "$completions" ]; then
        compadd -U -V unsorted -a completions
    fi
}

compdef _zpcli_completion zpcli;
"""
        elif shell == "fish":
            completion_script = """
function _zpcli_completion;
    set -l response;

    for value in (env _ZPCLI_COMPLETE=complete_fish COMP_WORDS=(commandline -cp) COMP_CWORD=(commandline -t) zpcli);
        set response $response $value;
    end;

    for completion in $response;
        set -l metadata (string split "," $completion);

        if test $metadata[1] = "dir";
            __fish_complete_directories $metadata[2];
        else if test $metadata[1] = "file";
            __fish_complete_path $metadata[2];
        else if test $metadata[1] = "plain";
            echo $metadata[2];
        end;
    end;
end;

complete --no-files --command zpcli --arguments "(_zpcli_completion)";
"""
        else:
            completion_script = "# Powershell completion not yet implemented"
        
        if install:
            home = os.path.expanduser("~")
            
            if shell == "bash":
                completion_file = os.path.join(home, ".zpcli-completion.bash")
                rc_file = os.path.join(home, ".bashrc")
                source_line = f"\n# zpcli completion\n[ -f {completion_file} ] && . {completion_file}\n"
            elif shell == "zsh":
                completion_file = os.path.join(home, ".zpcli-completion.zsh")
                rc_file = os.path.join(home, ".zshrc")
                source_line = f"\n# zpcli completion\n[ -f {completion_file} ] && . {completion_file}\n"
            elif shell == "fish":
                config_dir = os.path.join(home, ".config", "fish", "completions")
                os.makedirs(config_dir, exist_ok=True)
                completion_file = os.path.join(config_dir, "zpcli.fish")
                rc_file = None
                source_line = None
            
            # Write completion script
            with open(completion_file, "w") as f:
                f.write(completion_script)
            console.print(f"[green]✓[/green] Wrote completion script to: {completion_file}")
            
            # Add source line to RC file for bash/zsh
            if rc_file and source_line:
                with open(rc_file, "a+") as f:
                    f.seek(0)
                    content = f.read()
                    if completion_file not in content:
                        f.write(source_line)
                        console.print(f"[green]✓[/green] Added source line to: {rc_file}")
                    else:
                        console.print(f"[yellow]~[/yellow] Already sourced in: {rc_file}")
            
            console.print(f"\n[bold green]Installation complete![/bold green]")
            console.print(f"Restart your shell or run: source {rc_file if rc_file else completion_file}")
        else:
            # Just print the completion script
            print(completion_script)
            
    except Exception as e:
        console.print(f"[red]Error generating completion: {e}[/red]")
        raise typer.Exit(1)
