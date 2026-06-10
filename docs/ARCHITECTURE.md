# skskyforge — Architecture

> How a birth date + a calendar date become a ten-domain daily alignment report,
> and where that report flows in the SKWorld stack.

skskyforge is a **pure generator pipeline**. It has no daemon, no database, and no
network dependency at compute time (geocoding aside, which happens once, at profile
creation). Everything is: *load a profile → run a set of calculators and analyzers
against a date → synthesize → render*. The astronomy is real — planetary positions
come from the **Swiss Ephemeris** (`pyswisseph` / `ephem`), not a lookup table.

---

## The big picture

```mermaid
flowchart TD
    CLI["skskyforge CLI (Click)<br/>generate · preview · daily · profile · install-daily"]
    PROF["UserProfile (YAML)<br/>birth date/time/place + life path"]
    CLI -->|"loads"| PROF

    subgraph PIPE["generate_daily_entry(date, profile)"]
      direction TB
      CALC["calculators<br/>moon · numerology · biorhythm · solar · planets"]
      ANA["analyzers<br/>risk · wellness (exercise/nourishment/rituals)"]
      SYNTH["synthesis<br/>theme · power hours · caution periods · affirmation"]
      CALC --> ANA --> SYNTH
    end

    EPH["Swiss Ephemeris<br/>(real planetary positions)"]
    DATAJSON["data/*.json<br/>(zodiac · numerology meanings · wisdom texts)"]

    PROF --> PIPE
    CALC --> EPH
    SYNTH --> DATAJSON
    PIPE --> DP["DailyPreparation<br/>(one model, all 10 domains)"]

    DP --> RENDER{"output format?"}
    RENDER -->|"text"| RICH["rich terminal panel"]
    RENDER -->|"markdown / json"| TXT["stdout or file"]
    RENDER -->|"pdf / excel / csv"| EXP["exporters/"]
```

The single output object is `DailyPreparation` (`models/daily_entry.py`). Every CLI
command — `preview`, `daily`, and each day of `generate` — produces one of these and
then chooses how to render it.

---

## The daily-entry flow (what `generate_daily_entry` actually does)

The orchestration lives in `generators/daily_entry.py`. The order matters: I Ching
is derived from the Human Design Sun gate, and the synthesis step reads several
upstream domains.

```mermaid
sequenceDiagram
    participant CLI
    participant Gen as generate_daily_entry()
    participant Eph as Swiss Ephemeris
    participant Ana as analyzers
    participant Model as DailyPreparation

    CLI->>Gen: (target_date, profile)
    Gen->>Eph: calculate_moon_data(date)
    Gen->>Gen: calculate_numerology_for_day(birth, date, life_path)
    Gen->>Gen: calculate_biorhythm_for_day(birth, date)
    Gen->>Eph: generate_solar_transit (sun sign, house focus, aspects)
    Gen->>Eph: generate_human_design (type + daily gate activations)
    Gen->>Gen: generate_i_ching (hexagram from the Sun gate)
    Gen->>Ana: calculate_risk_analysis(moon, biorhythm, numerology)
    Gen->>Ana: exercise + nourishment + rituals (element-tuned)
    Gen->>Gen: synthesize theme, power hours, caution periods, affirmation
    Gen-->>Model: DailyPreparation (10 domains + synthesis)
    Model-->>CLI: render (terminal / md / json / pdf / excel / csv)
```

Notable couplings, grounded in the code:

- **I Ching ← Human Design.** The 64 HD gates map to the 64 I Ching hexagrams;
  `generate_i_ching` picks the hexagram from the active **Sun** gate.
- **Spiritual reading, exercise, nourishment, affirmation ← Moon element.** The
  moon sign's element (Fire/Earth/Air/Water) routes the wisdom tradition
  (Stoic/Taoist/Buddhist/Sufi), the element-tuned exercise, and the affirmation.
- **Risk analysis ← moon + biorhythm + numerology**, e.g. moon void-of-course and
  low intellectual biorhythm both feed caution periods.

---

## The scheduled-report path

`skskyforge daily` is deliberately non-interactive so a scheduler can run it every
morning. `install-daily` writes the schedule using whatever the OS supports best.

```mermaid
flowchart LR
    INSTALL["skskyforge install-daily<br/>--time HH:MM --profile P"]
    INSTALL --> PICK{"OS?"}
    PICK -->|"Linux"| SD["systemd user timer<br/>(crontab fallback)"]
    PICK -->|"macOS"| LD["launchd / crontab fallback"]
    PICK -->|"Windows"| ST["schtasks"]
    SD --> RUN["skskyforge daily --profile P --format markdown --output file"]
    LD --> RUN
    ST --> RUN
    RUN --> FILE["~/.skskyforge/output/skskyforge_daily_YYYY-MM-DD.md"]
```

On Linux it prefers a **systemd user timer** (`skskyforge-daily.timer` +
`.service`) and falls back to a `crontab` line; on Windows it registers a
`SKSkyforgeDaily` task via `schtasks`. `uninstall-daily` reverses whichever was
installed.

---

## Source / content map

| Path | Role |
|---|---|
| `src/skskyforge/cli.py` | Click CLI — all commands, rich rendering, the systemd/cron/schtasks installer |
| `src/skskyforge/generators/daily_entry.py` | the orchestrator (`generate_daily_entry`) + HD/I-Ching/spiritual/synthesis logic |
| `src/skskyforge/calculators/moon.py` | lunar phase %, zodiac sign, element/modality, void-of-course |
| `src/skskyforge/calculators/numerology.py` | life path, personal year/month/day, universal day |
| `src/skskyforge/calculators/biorhythm.py` | physical / emotional / intellectual cycles + critical days |
| `src/skskyforge/calculators/solar.py` | sun sign + natal→transit house focus |
| `src/skskyforge/calculators/planets.py` | ephemeris planetary positions, aspects, HD gate activations |
| `src/skskyforge/analyzers/risk.py` | multi-domain risk score (0–100) + warnings |
| `src/skskyforge/analyzers/wellness.py` | exercise, nourishment, and ritual recommendations |
| `src/skskyforge/exporters/{pdf,excel,csv}_exporter.py` | PDF / Excel / CSV renderers |
| `src/skskyforge/models/daily_entry.py` | `DailyPreparation` — the unified output model |
| `src/skskyforge/models/domains.py` | per-domain pydantic models (Moon/Numerology/HD/I-Ching/…) |
| `src/skskyforge/models/profile.py`, `birth_data.py` | profile + birth-data models (load/save YAML) |
| `src/skskyforge/services/geocoding.py` | OpenStreetMap geocoding → lat/long + IANA timezone |
| `src/skskyforge/data/*.json` | reference data: `zodiac_signs.json`, `numerology_meanings.json`, `spiritual_library/wisdom_texts.json` |
| `src/skskyforge/web/` | optional FastAPI dashboard (`[web]` extra) |
| `config/settings.yaml` | global generation/export/calculation toggles |

---

## Where it lives in the ecosystem

skskyforge is a **Compute** capability: a stateless generator that depends only on
the Swiss Ephemeris and its bundled reference data. It produces a daily report; the
platform's scheduling, alerting, and agent layers consume it.

```mermaid
flowchart TD
    subgraph COMPUTE["Compute"]
      SKF["**skskyforge**<br/>10-domain daily alignment generator"]
      EPH["Swiss Ephemeris<br/>(pyswisseph / ephem)"]
      SKF --> EPH
    end
    subgraph PLATFORM["Platform primitives"]
      SCHED["skscheduler<br/>(install-daily timer)"]
      ALERT["sk-alert<br/>(deliver the morning report)"]
    end
    subgraph CORE["Core"]
      AGENT["skcapstone agents<br/>(daily alignment as context)"]
    end
    SKF -->|"timer"| SCHED
    SKF -->|"daily report"| ALERT
    SKF -->|"daily --format json"| AGENT
```

The contract with the rest of SKWorld is intentionally thin: one well-defined,
machine-readable command (`skskyforge daily --format json`) that any agent or
scheduler can call. Per `SKILL.md`, that makes the day's alignment available to
OpenClaw/skcapstone agents as context for the morning.

---

Part of the **[SKWorld](https://skworld.io)** sovereign ecosystem · 🐧 smilinTux
