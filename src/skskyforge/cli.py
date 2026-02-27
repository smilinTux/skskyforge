"""
SKSkyforge Command Line Interface.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin

This file is part of SKSkyforge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

import json
import os
import platform
import shutil
import subprocess
import textwrap
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from .models import (
    BirthData,
    BirthTimeRange,
    Location,
    UserProfile,
    CalendarRequest,
)
from .generators import generate_daily_entry
from .calculators import calculate_life_path


console = Console()

# Default paths - use ~/.skskyforge for user-level config
DEFAULT_CONFIG_DIR = Path.home() / ".skskyforge"
DEFAULT_PROFILES_DIR = DEFAULT_CONFIG_DIR / "profiles"
DEFAULT_OUTPUT_DIR = DEFAULT_CONFIG_DIR / "output"


def get_profiles_dir() -> Path:
    """Get profiles directory, creating if needed."""
    profiles_dir = DEFAULT_PROFILES_DIR
    profiles_dir.mkdir(parents=True, exist_ok=True)
    return profiles_dir


def get_output_dir() -> Path:
    """Get output directory, creating if needed."""
    output_dir = DEFAULT_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


@click.group()
@click.version_option(version="1.0.0", prog_name="SKSkyforge")
def cli():
    """
    🌟 SKSkyforge - Sovereign Alignment Calendar Generator
    
    Forge your sovereign path through the cosmos.
    
    Generate personalized daily preparation guides integrating
    moon phases, numerology, Human Design, I Ching, biorhythms,
    and wellness recommendations.
    """
    pass


# =============================================================================
# Generate Commands
# =============================================================================

@cli.command()
@click.option("--year", "-y", required=True, type=int, help="Target year (e.g., 2026)")
@click.option("--profile", "-p", default="default", help="Profile name to use")
@click.option("--month", "-m", type=int, help="Generate single month only (1-12)")
@click.option("--format", "-f", "formats", multiple=True, 
              type=click.Choice(["json", "pdf", "excel", "csv"]),
              default=["json"], help="Output format(s)")
@click.option("--output", "-o", type=click.Path(), help="Output directory")
def generate(year: int, profile: str, month: Optional[int], formats: tuple, output: Optional[str]):
    """
    Generate sovereign alignment calendar.
    
    Examples:
    
        skskyforge generate --year 2026
        
        skskyforge generate --year 2026 --month 1 --format pdf
        
        skskyforge generate --year 2026 --profile john --format json --format excel
    """
    # Load profile
    profiles_dir = get_profiles_dir()
    profile_path = profiles_dir / f"{profile}.yaml"
    
    if not profile_path.exists():
        console.print(f"[red]Error:[/red] Profile '{profile}' not found.")
        console.print(f"Create it with: [cyan]skskyforge profile create --name {profile}[/cyan]")
        raise SystemExit(1)
    
    try:
        user_profile = UserProfile.load(profile_path)
    except Exception as e:
        console.print(f"[red]Error loading profile:[/red] {e}")
        raise SystemExit(1)
    
    # Determine date range
    if month:
        import calendar
        start_date = date(year, month, 1)
        _, last_day = calendar.monthrange(year, month)
        end_date = date(year, month, last_day)
        period_name = f"{calendar.month_name[month]} {year}"
    else:
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        period_name = str(year)
    
    # Calculate total days
    total_days = (end_date - start_date).days + 1
    
    console.print(Panel(
        f"[bold cyan]Generating {period_name} Calendar[/bold cyan]\n\n"
        f"Profile: [green]{profile}[/green]\n"
        f"Days: [yellow]{total_days}[/yellow]\n"
        f"Formats: [magenta]{', '.join(formats)}[/magenta]",
        title="🌟 SKSkyforge",
    ))
    
    # Generate entries
    entries = []
    output_dir = Path(output) if output else get_output_dir()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Generating {total_days} days...", total=total_days)
        
        current = start_date
        from datetime import timedelta
        while current <= end_date:
            entry = generate_daily_entry(current, user_profile)
            entries.append(entry)
            progress.advance(task)
            current += timedelta(days=1)
    
    # Export to requested formats
    for fmt in formats:
        if fmt == "json":
            filename = f"skskyforge_{profile}_{period_name.replace(' ', '_')}.json"
            filepath = output_dir / filename
            
            # Convert to JSON-serializable format
            data = {
                "metadata": {
                    "profile": profile,
                    "year": year,
                    "month": month,
                    "generated_at": datetime.now().isoformat(),
                    "total_days": len(entries),
                },
                "entries": [entry.model_dump(mode='json') for entry in entries],
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            console.print(f"[green]✓[/green] JSON exported: {filepath}")
        
        elif fmt == "pdf":
            from .exporters import export_pdf

            filename = f"skskyforge_{profile}_{period_name.replace(' ', '_')}.pdf"
            filepath = output_dir / filename
            export_pdf(entries, filepath)
            console.print(f"[green]✓[/green] PDF exported: {filepath}")

        elif fmt == "excel":
            from .exporters import export_excel

            filename = f"skskyforge_{profile}_{period_name.replace(' ', '_')}.xlsx"
            filepath = output_dir / filename
            export_excel(entries, filepath)
            console.print(f"[green]✓[/green] Excel exported: {filepath}")

        elif fmt == "csv":
            from .exporters import export_csv

            filename = f"skskyforge_{profile}_{period_name.replace(' ', '_')}.csv"
            filepath = output_dir / filename
            export_csv(entries, filepath)
            console.print(f"[green]✓[/green] CSV exported: {filepath}")
    
    console.print(f"\n[bold green]✓ Calendar generation complete![/bold green]")


@cli.command()
@click.option("--date", "-d", "target_date", required=True, 
              help="Date to preview (YYYY-MM-DD)")
@click.option("--profile", "-p", default="default", help="Profile name to use")
def preview(target_date: str, profile: str):
    """
    Preview a single day's alignment.
    
    Example:
    
        skskyforge preview --date 2026-01-15
    """
    # Parse date
    try:
        dt = datetime.strptime(target_date, "%Y-%m-%d").date()
    except ValueError:
        console.print("[red]Error:[/red] Invalid date format. Use YYYY-MM-DD")
        raise SystemExit(1)
    
    # Load profile
    profiles_dir = get_profiles_dir()
    profile_path = profiles_dir / f"{profile}.yaml"
    
    if not profile_path.exists():
        console.print(f"[red]Error:[/red] Profile '{profile}' not found.")
        raise SystemExit(1)
    
    user_profile = UserProfile.load(profile_path)
    
    # Generate entry
    with console.status("Calculating alignment..."):
        entry = generate_daily_entry(dt, user_profile)
    
    # Display
    display_daily_entry(entry)


def display_daily_entry(entry):
    """Display a daily entry in rich format."""
    # Header
    console.print(Panel(
        f"[bold cyan]SKSKYFORGE DAILY SOVEREIGN ALIGNMENT[/bold cyan]\n"
        f"[bold]{entry.day_of_week}, {entry.date.strftime('%B %d, %Y')}[/bold] "
        f"(Day {entry.day_of_year} of 365)",
        title="🌟",
    ))
    
    # Theme
    console.print(f"\n[bold yellow]DAILY THEME:[/bold yellow] {entry.daily_theme}")
    console.print(f"[bold]OVERALL ENERGY:[/bold] {entry.biorhythm.overall_energy} | "
                  f"[bold]RISK LEVEL:[/bold] {entry.risk_analysis.overall_risk_level}")
    
    # Moon
    console.print(f"\n🌙 [bold]MOON:[/bold] {entry.moon.phase} ({entry.moon.phase_percentage:.0f}%) "
                  f"in {entry.moon.zodiac_sign}")
    console.print(f"   Element: {entry.moon.sign_element} | Modality: {entry.moon.sign_modality}")
    console.print(f"   Energy: {entry.moon.energy_theme}")
    
    # Numerology
    console.print(f"\n🔢 [bold]NUMEROLOGY:[/bold] Personal Day {entry.numerology.personal_day} "
                  f"(Universal Day {entry.numerology.universal_day})")
    console.print(f"   Theme: {entry.numerology.day_theme}")
    
    # Biorhythm
    console.print(f"\n📊 [bold]BIORHYTHM:[/bold]")
    console.print(f"   Physical: {entry.biorhythm.physical:+.0f}% ({entry.biorhythm.physical_phase})")
    console.print(f"   Emotional: {entry.biorhythm.emotional:+.0f}% ({entry.biorhythm.emotional_phase})")
    console.print(f"   Intellectual: {entry.biorhythm.intellectual:+.0f}% ({entry.biorhythm.intellectual_phase})")
    
    # Exercise
    console.print(f"\n💪 [bold]EXERCISE:[/bold] {entry.exercise.exercise_type} ({entry.exercise.intensity})")
    console.print(f"   Time: {entry.exercise.optimal_time} | Duration: {entry.exercise.duration_minutes} min")
    
    # Spiritual Reading
    console.print(f"\n📖 [bold]SPIRITUAL READING:[/bold] {entry.spiritual_reading.source_title}")
    console.print(f"   \"{entry.spiritual_reading.reading_text[:100]}...\"")
    
    # Affirmation
    console.print(f"\n💫 [bold]TODAY'S AFFIRMATION:[/bold]")
    console.print(f"   \"{entry.affirmation}\"")


# =============================================================================
# Daily Report Command
# =============================================================================


def format_daily_markdown(entry) -> str:
    """Format a daily entry as markdown text suitable for chat or file output.

    Args:
        entry: DailyPreparation model instance.

    Returns:
        str: Markdown-formatted daily report.
    """
    lines = [
        f"# SKSkyforge Daily Sovereign Alignment",
        f"## {entry.day_of_week}, {entry.date.strftime('%B %d, %Y')} "
        f"(Day {entry.day_of_year})",
        "",
        f"**Daily Theme:** {entry.daily_theme}",
        f"**Overall Energy:** {entry.biorhythm.overall_energy} | "
        f"**Risk Level:** {entry.risk_analysis.overall_risk_level}",
        "",
        f"### Moon",
        f"- Phase: {entry.moon.phase} ({entry.moon.phase_percentage:.0f}%) "
        f"in {entry.moon.zodiac_sign}",
        f"- Element: {entry.moon.sign_element} | "
        f"Modality: {entry.moon.sign_modality}",
        f"- Energy: {entry.moon.energy_theme}",
        "",
        f"### Numerology",
        f"- Personal Day {entry.numerology.personal_day} "
        f"(Universal Day {entry.numerology.universal_day})",
        f"- Theme: {entry.numerology.day_theme}",
        "",
        f"### Biorhythm",
        f"- Physical: {entry.biorhythm.physical:+.0f}% "
        f"({entry.biorhythm.physical_phase})",
        f"- Emotional: {entry.biorhythm.emotional:+.0f}% "
        f"({entry.biorhythm.emotional_phase})",
        f"- Intellectual: {entry.biorhythm.intellectual:+.0f}% "
        f"({entry.biorhythm.intellectual_phase})",
        "",
        f"### Exercise",
        f"- {entry.exercise.exercise_type} ({entry.exercise.intensity})",
        f"- Time: {entry.exercise.optimal_time} | "
        f"Duration: {entry.exercise.duration_minutes} min",
        "",
        f"### Spiritual Reading",
        f"- {entry.spiritual_reading.source_title}",
        f'- "{entry.spiritual_reading.reading_text[:200]}"',
        "",
        f"### Affirmation",
        f'> "{entry.affirmation}"',
        "",
        "---",
        "*Generated by SKSkyforge - staycuriousANDkeepsmilin*",
    ]
    return "\n".join(lines)


@cli.command()
@click.option("--profile", "-p", default="default", help="Profile name to use")
@click.option(
    "--format",
    "-f",
    "fmt",
    type=click.Choice(["text", "json", "markdown"]),
    default="text",
    help="Output format",
)
@click.option(
    "--output",
    "-o",
    "output_target",
    type=click.Choice(["stdout", "file"]),
    default="stdout",
    help="Where to send the report",
)
def daily(profile: str, fmt: str, output_target: str):
    """Generate today's sovereign alignment report.

    Designed for crontab / systemd timer use. Runs non-interactively
    and outputs the daily alignment for the given profile.

    Examples:

        skskyforge daily

        skskyforge daily --profile lumina --format markdown

        skskyforge daily --format json --output file
    """
    profiles_dir = get_profiles_dir()
    profile_path = profiles_dir / f"{profile}.yaml"

    if not profile_path.exists():
        console.print(f"[red]Error:[/red] Profile '{profile}' not found.")
        console.print(
            "Create one with: "
            f"[cyan]skskyforge profile create --name {profile} "
            "--birth-date YYYY-MM-DD[/cyan]"
        )
        raise SystemExit(1)

    user_profile = UserProfile.load(profile_path)
    today = date.today()
    entry = generate_daily_entry(today, user_profile)

    if fmt == "json":
        content = json.dumps(entry.model_dump(mode="json"), indent=2, default=str)
    elif fmt == "markdown":
        content = format_daily_markdown(entry)
    else:
        content = format_daily_markdown(entry)

    if output_target == "file":
        output_dir = get_output_dir()
        filename = f"skskyforge_daily_{today.isoformat()}.{'json' if fmt == 'json' else 'md'}"
        filepath = output_dir / filename
        with open(filepath, "w") as f:
            f.write(content)
        console.print(f"[green]Daily report written to {filepath}[/green]")
    else:
        if fmt == "text":
            display_daily_entry(entry)
        else:
            click.echo(content)


# =============================================================================
# Install / Uninstall Daily Timer
# =============================================================================

SYSTEMD_SERVICE_TEMPLATE = textwrap.dedent("""\
    [Unit]
    Description=SKSkyforge Daily Alignment Report
    After=network.target

    [Service]
    Type=oneshot
    ExecStart={exe} daily --profile {profile} --format {fmt} --output {output}
    Environment=HOME={home}
""")

SYSTEMD_TIMER_TEMPLATE = textwrap.dedent("""\
    [Unit]
    Description=SKSkyforge Daily Alignment Timer

    [Timer]
    OnCalendar=*-*-* {hour}:{minute}:00
    Persistent=true

    [Install]
    WantedBy=timers.target
""")


@cli.command("install-daily")
@click.option("--time", "-t", default="08:00", help="Time to run (HH:MM, default 08:00)")
@click.option("--profile", "-p", default="default", help="Profile name")
@click.option(
    "--format",
    "-f",
    "fmt",
    type=click.Choice(["text", "markdown", "json"]),
    default="markdown",
    help="Report format",
)
@click.option(
    "--output",
    "-o",
    "output_target",
    type=click.Choice(["stdout", "file"]),
    default="file",
    help="Output target",
)
def install_daily(time: str, profile: str, fmt: str, output_target: str):
    """Install a scheduled daily report (systemd/crontab/Task Scheduler).

    On Linux: systemd user timer (preferred) or crontab fallback.
    On macOS: launchd plist or crontab fallback.
    On Windows: Windows Task Scheduler via schtasks.

    Examples:

        skskyforge install-daily

        skskyforge install-daily --time 07:30 --profile lumina
    """
    try:
        hour, minute = time.split(":")
        int(hour)
        int(minute)
    except (ValueError, AttributeError):
        console.print("[red]Error:[/red] Invalid time format. Use HH:MM")
        raise SystemExit(1)

    exe = shutil.which("skskyforge") or "skskyforge"

    if platform.system() == "Windows":
        _install_windows_task(exe, profile, fmt, output_target, hour, minute)
        return

    # Reason: prefer systemd user timers over crontab -- more reliable, supports
    # logging, and integrates with `systemctl --user status`
    systemd_dir = Path.home() / ".config" / "systemd" / "user"
    use_systemd = systemd_dir.exists() or _can_create_systemd_dir(systemd_dir)

    if use_systemd:
        _install_systemd_timer(
            systemd_dir, exe, profile, fmt, output_target, hour, minute
        )
    else:
        _install_crontab(exe, profile, fmt, output_target, hour, minute)


def _can_create_systemd_dir(path: Path) -> bool:
    """Check if we can create the systemd user directory."""
    try:
        path.mkdir(parents=True, exist_ok=True)
        return True
    except OSError:
        return False


def _install_systemd_timer(
    systemd_dir: Path,
    exe: str,
    profile: str,
    fmt: str,
    output_target: str,
    hour: str,
    minute: str,
) -> None:
    """Install systemd user service and timer files."""
    service_content = SYSTEMD_SERVICE_TEMPLATE.format(
        exe=exe,
        profile=profile,
        fmt=fmt,
        output=output_target,
        home=str(Path.home()),
    )
    timer_content = SYSTEMD_TIMER_TEMPLATE.format(hour=hour, minute=minute)

    service_path = systemd_dir / "skskyforge-daily.service"
    timer_path = systemd_dir / "skskyforge-daily.timer"

    service_path.write_text(service_content)
    timer_path.write_text(timer_content)

    subprocess.run(["systemctl", "--user", "daemon-reload"], check=False)
    subprocess.run(
        ["systemctl", "--user", "enable", "--now", "skskyforge-daily.timer"],
        check=False,
    )

    console.print(
        f"[green]Systemd timer installed![/green] "
        f"Daily report at {hour}:{minute} for profile '{profile}'."
    )
    console.print(
        "  Check status: [cyan]systemctl --user status skskyforge-daily.timer[/cyan]"
    )


def _install_crontab(
    exe: str,
    profile: str,
    fmt: str,
    output_target: str,
    hour: str,
    minute: str,
) -> None:
    """Install a crontab entry as fallback."""
    cron_line = (
        f"{minute} {hour} * * * "
        f"{exe} daily --profile {profile} --format {fmt} --output {output_target}"
    )

    result = subprocess.run(
        ["crontab", "-l"], capture_output=True, text=True, check=False
    )
    existing = result.stdout if result.returncode == 0 else ""

    if "skskyforge daily" in existing:
        console.print("[yellow]Crontab entry already exists. Replacing...[/yellow]")
        lines = [
            l for l in existing.splitlines() if "skskyforge daily" not in l
        ]
        existing = "\n".join(lines) + "\n"

    new_crontab = existing.rstrip("\n") + "\n" + cron_line + "\n"
    proc = subprocess.run(
        ["crontab", "-"], input=new_crontab, text=True, check=False
    )

    if proc.returncode == 0:
        console.print(
            f"[green]Crontab entry installed![/green] "
            f"Daily report at {hour}:{minute} for profile '{profile}'."
        )
    else:
        console.print("[red]Failed to install crontab entry.[/red]")


WINDOWS_TASK_NAME = "SKSkyforgeDaily"


def _install_windows_task(
    exe: str,
    profile: str,
    fmt: str,
    output_target: str,
    hour: str,
    minute: str,
) -> None:
    """Install a Windows Task Scheduler entry via schtasks."""
    cmd_line = f'"{exe}" daily --profile {profile} --format {fmt} --output {output_target}'
    schtasks_cmd = [
        "schtasks",
        "/Create",
        "/SC", "DAILY",
        "/TN", WINDOWS_TASK_NAME,
        "/TR", cmd_line,
        "/ST", f"{hour}:{minute}",
        "/F",
    ]

    proc = subprocess.run(schtasks_cmd, capture_output=True, text=True, check=False)

    if proc.returncode == 0:
        console.print(
            f"[green]Windows Task Scheduler entry installed![/green] "
            f"Daily report at {hour}:{minute} for profile '{profile}'."
        )
        console.print(
            f"  Check status: [cyan]schtasks /Query /TN {WINDOWS_TASK_NAME}[/cyan]"
        )
    else:
        console.print(f"[red]Failed to create scheduled task:[/red] {proc.stderr.strip()}")


def _uninstall_windows_task() -> bool:
    """Remove the Windows Task Scheduler entry."""
    proc = subprocess.run(
        ["schtasks", "/Delete", "/TN", WINDOWS_TASK_NAME, "/F"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode == 0:
        console.print("[green]Windows scheduled task removed.[/green]")
        return True
    return False


@cli.command("uninstall-daily")
def uninstall_daily():
    """Remove the daily report timer/cron/scheduled task.

    Removes the systemd timer, crontab entry, or Windows scheduled task.
    """
    removed = False

    if platform.system() == "Windows":
        removed = _uninstall_windows_task()
    else:
        systemd_dir = Path.home() / ".config" / "systemd" / "user"
        service_path = systemd_dir / "skskyforge-daily.service"
        timer_path = systemd_dir / "skskyforge-daily.timer"

        if timer_path.exists():
            subprocess.run(
                ["systemctl", "--user", "disable", "--now", "skskyforge-daily.timer"],
                check=False,
            )
            timer_path.unlink(missing_ok=True)
            service_path.unlink(missing_ok=True)
            subprocess.run(["systemctl", "--user", "daemon-reload"], check=False)
            console.print("[green]Systemd timer removed.[/green]")
            removed = True

        result = subprocess.run(
            ["crontab", "-l"], capture_output=True, text=True, check=False
        )
        if result.returncode == 0 and "skskyforge daily" in result.stdout:
            lines = [
                l for l in result.stdout.splitlines() if "skskyforge daily" not in l
            ]
            subprocess.run(
                ["crontab", "-"],
                input="\n".join(lines) + "\n",
                text=True,
                check=False,
            )
            console.print("[green]Crontab entry removed.[/green]")
            removed = True

    if not removed:
        console.print("[yellow]No daily timer/cron/task found to remove.[/yellow]")


# =============================================================================
# Profile Commands
# =============================================================================

@cli.group()
def profile():
    """Manage user profiles."""
    pass


@profile.command("create")
@click.option("--name", "-n", required=True, help="Profile name")
@click.option("--birth-date", "-d", required=True, help="Birth date (YYYY-MM-DD)")
@click.option("--birth-time", "-t", help="Birth time (HH:MM)")
@click.option("--birth-time-range", "-r", 
              type=click.Choice(["exact", "morning", "afternoon", "evening", "night", "unknown"]),
              default="unknown", help="Birth time range if exact time unknown")
@click.option("--birth-location", "-l", help="Birth location (city, state/country)")
def profile_create(name: str, birth_date: str, birth_time: Optional[str], 
                   birth_time_range: str, birth_location: Optional[str]):
    """
    Create a new user profile.
    
    Examples:
    
        skskyforge profile create --name john --birth-date 1985-03-15
        
        skskyforge profile create --name jane --birth-date 1990-07-22 \\
            --birth-time 14:30 --birth-location "New York, NY, USA"
    """
    # Parse birth date
    try:
        bd = datetime.strptime(birth_date, "%Y-%m-%d").date()
    except ValueError:
        console.print("[red]Error:[/red] Invalid birth date format. Use YYYY-MM-DD")
        raise SystemExit(1)
    
    # Parse birth time if provided
    bt = None
    if birth_time:
        try:
            bt = datetime.strptime(birth_time, "%H:%M").time()
            birth_time_range = "exact"
        except ValueError:
            console.print("[red]Error:[/red] Invalid birth time format. Use HH:MM")
            raise SystemExit(1)
    
    # Create location if provided (with geocoding)
    location = None
    if birth_location:
        from .services.geocoding import geocode_city

        geo = geocode_city(birth_location)
        if geo:
            location = Location(
                city=geo.display_name,
                latitude=geo.latitude,
                longitude=geo.longitude,
                timezone=geo.timezone,
            )
            console.print(f"  [dim]Geocoded → {geo.display_name}[/dim]")
            console.print(f"  [dim]Coordinates: {geo.latitude}, {geo.longitude}[/dim]")
            console.print(f"  [dim]Timezone: {geo.timezone}[/dim]")
        else:
            location = Location(city=birth_location)
            console.print(f"  [yellow]Could not geocode '{birth_location}', using city name only[/yellow]")

    # Create birth data
    birth_data = BirthData(
        date=bd,
        time=bt,
        time_range=BirthTimeRange(birth_time_range),
        location=location,
    )
    
    # Calculate life path
    life_path = calculate_life_path(bd)
    
    # Create profile
    user_profile = UserProfile(
        name=name,
        birth_data=birth_data,
        life_path_number=life_path,
    )
    
    # Save profile
    profiles_dir = get_profiles_dir()
    user_profile.save(profiles_dir)
    
    console.print(f"\n[green]✓ Profile '{name}' created successfully![/green]")
    console.print(f"  Birth Date: {bd}")
    console.print(f"  Life Path: {life_path}")
    if location:
        console.print(f"  Location: {location}")
        if location.has_coordinates():
            console.print(f"  Timezone: {location.timezone}")


@profile.command("list")
def profile_list():
    """List all available profiles."""
    profiles_dir = get_profiles_dir()
    
    profiles = list(profiles_dir.glob("*.yaml"))
    
    if not profiles:
        console.print("[yellow]No profiles found.[/yellow]")
        console.print("Create one with: [cyan]skskyforge profile create --name myname --birth-date YYYY-MM-DD[/cyan]")
        return
    
    table = Table(title="Available Profiles")
    table.add_column("Name", style="cyan")
    table.add_column("Birth Date", style="green")
    table.add_column("Life Path", style="yellow")
    
    for profile_path in profiles:
        try:
            p = UserProfile.load(profile_path)
            table.add_row(
                p.name,
                str(p.birth_data.date),
                str(p.life_path_number or "?"),
            )
        except Exception:
            table.add_row(profile_path.stem, "Error loading", "")
    
    console.print(table)


@profile.command("show")
@click.argument("name")
def profile_show(name: str):
    """Show profile details."""
    profiles_dir = get_profiles_dir()
    profile_path = profiles_dir / f"{name}.yaml"
    
    if not profile_path.exists():
        console.print(f"[red]Error:[/red] Profile '{name}' not found.")
        raise SystemExit(1)
    
    p = UserProfile.load(profile_path)
    
    console.print(Panel(
        f"[bold cyan]{p.name}[/bold cyan]\n\n"
        f"Birth Date: [green]{p.birth_data.date}[/green]\n"
        f"Birth Time: [yellow]{p.birth_data.time or p.birth_data.time_range.value}[/yellow]\n"
        f"Location: {p.birth_data.location or 'Not specified'}\n"
        f"Life Path: [magenta]{p.life_path_number}[/magenta]\n"
        f"HD Type: {p.human_design_type or 'Not calculated'}",
        title="Profile Details",
    ))


@profile.command("delete")
@click.argument("name")
@click.confirmation_option(prompt="Are you sure you want to delete this profile?")
def profile_delete(name: str):
    """Delete a profile."""
    profiles_dir = get_profiles_dir()
    profile_path = profiles_dir / f"{name}.yaml"
    
    if not profile_path.exists():
        console.print(f"[red]Error:[/red] Profile '{name}' not found.")
        raise SystemExit(1)
    
    profile_path.unlink()
    console.print(f"[green]✓ Profile '{name}' deleted.[/green]")


# =============================================================================
# Main Entry Point
# =============================================================================

def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
