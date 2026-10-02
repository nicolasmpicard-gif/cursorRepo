from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from linkedin_jd_bot.pipeline import ExtractionError, extract_job
from linkedin_jd_bot.company_enrich import maybe_enrich_job
from linkedin_jd_bot.urls import is_linkedin_job_url, looks_like_url

app = typer.Typer(
    add_completion=False,
    no_args_is_help=False,
    help="LinkedIn JD extractor bot with optional company-careers enrichment.",
)
console = Console()


def _read_stdin_if_piped() -> Optional[str]:
    if not sys.stdin.isatty():
        data = sys.stdin.read()
        return data if data.strip() else None
    return None


def _load_input(value: Optional[str], file: Optional[Path]) -> str:
    if file is not None:
        return file.read_text(encoding="utf-8")
    if value:
        return value
    piped = _read_stdin_if_piped()
    if piped:
        return piped
    console.print(
        Panel.fit(
            "[bold]LinkedIn JD Bot[/bold]\n"
            "Paste a LinkedIn job URL, or paste the JD text.\n"
            "End multi-line paste with an empty line (or Ctrl-D).",
            border_style="cyan",
        )
    )
    first = Prompt.ask("URL or first line of JD")
    if looks_like_url(first) or is_linkedin_job_url(first):
        return first.strip()
    lines = [first]
    console.print("[dim]Paste remaining JD text. Empty line to finish.[/dim]")
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    input_value: Optional[str] = typer.Argument(
        None, help="LinkedIn job URL or pasted JD text"
    ),
    file: Optional[Path] = typer.Option(
        None, "--file", "-f", help="Read URL/text/HTML from a file"
    ),
    browser: bool = typer.Option(
        False, "--browser", help="Fetch URL with Playwright (optional auth)"
    ),
    storage_state: Optional[Path] = typer.Option(
        None,
        "--storage-state",
        help="Playwright storage state JSON from a logged-in LinkedIn session",
    ),
    headed: bool = typer.Option(
        False, "--headed", help="Run Playwright with a visible browser"
    ),
    json_out: bool = typer.Option(False, "--json", help="Print JSON instead of text"),
    out: Optional[Path] = typer.Option(
        None, "--out", "-o", help="Write result to a file"
    ),
    enrich: bool = typer.Option(
        False,
        "--enrich",
        help="After LinkedIn extract, try employer ATS (Workable/Greenhouse/Lever)",
    ),
) -> None:
    """Extract a job description from a URL or pasted text."""
    if ctx.invoked_subcommand is not None:
        return

    try:
        raw = _load_input(input_value, file)
        is_html = bool(file and file.suffix.lower() in {".html", ".htm"})
        job = extract_job(
            raw,
            use_browser=browser,
            storage_state=str(storage_state) if storage_state else None,
            headless=not headed,
            html_file=is_html,
            enrich=False,
        )
        enrich_note = ""
        if enrich:
            job, enrich_note = maybe_enrich_job(job)
    except ExtractionError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc
    except Exception as exc:  # noqa: BLE001 - CLI boundary
        console.print(f"[red]Unexpected error:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    payload = job.model_dump(mode="json")
    text = "\n".join(job.summary_lines())
    rendered = json.dumps(payload, indent=2) if json_out else text

    if enrich and job.source.value == "company":
        console.print("[green]Enriched from company careers / ATS[/green]")
    elif enrich and enrich_note:
        console.print(f"[yellow]Enrichment:[/yellow] {enrich_note}")

    if out:
        out.write_text(rendered + "\n", encoding="utf-8")
        console.print(f"[green]Wrote[/green] {out}")
    else:
        if json_out:
            console.print_json(json.dumps(payload))
        else:
            console.print(Panel(text, title="Job Description", border_style="green"))


@app.command("interactive")
def interactive(
    browser: bool = typer.Option(False, "--browser"),
    storage_state: Optional[Path] = typer.Option(None, "--storage-state"),
    enrich: bool = typer.Option(False, "--enrich"),
) -> None:
    """Simple REPL bot: keep feeding URLs or pastes."""
    console.print(
        Panel.fit(
            "[bold]JD Bot interactive mode[/bold]\n"
            "Commands: [cyan]quit[/cyan] to exit. "
            "Paste a URL or JD text (empty line ends a paste).",
            border_style="cyan",
        )
    )
    while True:
        try:
            first = Prompt.ask("\n[bold]you[/bold]")
        except (EOFError, KeyboardInterrupt):
            console.print("\nBye.")
            raise typer.Exit() from None
        if first.strip().lower() in {"quit", "exit", "q"}:
            console.print("Bye.")
            raise typer.Exit()
        lines = [first]
        if not looks_like_url(first):
            while True:
                try:
                    line = input()
                except EOFError:
                    break
                if line == "":
                    break
                lines.append(line)
        raw = "\n".join(lines)
        try:
            job = extract_job(
                raw,
                use_browser=browser,
                storage_state=str(storage_state) if storage_state else None,
            )
            if enrich:
                job, note = maybe_enrich_job(job)
                if job.source.value != "company" and note:
                    console.print(f"[yellow]enrichment:[/yellow] {note}")
        except ExtractionError as exc:
            console.print(f"[yellow]bot:[/yellow] {exc}")
            continue
        console.print(
            Panel("\n".join(job.summary_lines()), title="bot", border_style="green")
        )


if __name__ == "__main__":
    app()
