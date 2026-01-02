"""
SkyForge Command Line Interface.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin 🐧

This file is part of SkyForge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

import json
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

# Default paths
DEFAULT_CONFIG_DIR = Path("./config")
DEFAULT_PROFILES_DIR = DEFAULT_CONFIG_DIR / "profiles"
DEFAULT_OUTPUT_DIR = Path("./output")


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
@click.version_option(version="1.0.0", prog_name="SkyForge")
def cli():
    """
    🌟 SkyForge - Sovereign Alignment Calendar Generator
    
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
    
        skyforge generate --year 2026
        
        skyforge generate --year 2026 --month 1 --format pdf
        
        skyforge generate --year 2026 --profile john --format json --format excel
    """
    # Load profile
    profiles_dir = get_profiles_dir()
    profile_path = profiles_dir / f"{profile}.yaml"
    
    if not profile_path.exists():
        console.print(f"[red]Error:[/red] Profile '{profile}' not found.")
        console.print(f"Create it with: [cyan]skyforge profile create --name {profile}[/cyan]")
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
        title="🌟 SkyForge",
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
            filename = f"skyforge_{profile}_{period_name.replace(' ', '_')}.json"
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
        
        elif fmt in ("pdf", "excel", "csv"):
            console.print(f"[yellow]![/yellow] {fmt.upper()} export coming soon")
    
    console.print(f"\n[bold green]✓ Calendar generation complete![/bold green]")


@cli.command()
@click.option("--date", "-d", "target_date", required=True, 
              help="Date to preview (YYYY-MM-DD)")
@click.option("--profile", "-p", default="default", help="Profile name to use")
def preview(target_date: str, profile: str):
    """
    Preview a single day's alignment.
    
    Example:
    
        skyforge preview --date 2026-01-15
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
        f"[bold cyan]SKYFORGE DAILY SOVEREIGN ALIGNMENT[/bold cyan]\n"
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
    
        skyforge profile create --name john --birth-date 1985-03-15
        
        skyforge profile create --name jane --birth-date 1990-07-22 \\
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
    
    # Create location if provided
    location = None
    if birth_location:
        location = Location(city=birth_location)
    
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
        console.print(f"  Location: {birth_location}")


@profile.command("list")
def profile_list():
    """List all available profiles."""
    profiles_dir = get_profiles_dir()
    
    profiles = list(profiles_dir.glob("*.yaml"))
    
    if not profiles:
        console.print("[yellow]No profiles found.[/yellow]")
        console.print("Create one with: [cyan]skyforge profile create --name myname --birth-date YYYY-MM-DD[/cyan]")
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
