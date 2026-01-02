# SkyForge 🌟

> **"Forge your sovereign path through the cosmos"**

SkyForge is a comprehensive daily preparation system that generates personalized sovereign alignment calendars. It integrates 10 domains of guidance into a unified system for optimal daily performance.

## ✨ Features

### 10 Integrated Domains

| Domain | Description |
|--------|-------------|
| 🌓 **Moon Phase & Sign** | Lunar phase, zodiac position, void-of-course periods |
| 🔢 **Numerology** | Life path, personal year/month/day calculations |
| 🌞 **Solar Return** | Annual chart, house focus, planetary transits |
| 🧬 **Human Design** | Type, strategy, authority, daily gate activations |
| ☯️ **I Ching** | Daily hexagram overlay with wisdom guidance |
| 📈 **Biorhythm** | Physical, emotional, intellectual cycle tracking |
| ⚠️ **Risk Analysis** | Multi-domain risk scoring and warnings |
| 🧘 **Exercise & Embodiment** | Physical activity recommendations |
| 🥣 **Nourishment** | Element-based dietary guidance |
| 📖 **Spiritual Reading** | Daily wisdom texts from curated library |

### Key Capabilities

- **Year-Agnostic**: Generate calendars for any year (2025, 2026, 2027, etc.)
- **Multi-User Profiles**: Support multiple users with saved birth data
- **Multiple Output Formats**: PDF, Excel/CSV, JSON, Web Dashboard
- **Actionable Guidance**: Daily practices for optimal performance

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/skyforge.git
cd skyforge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Create Your Profile

```bash
# Interactive profile creation
skyforge profile create

# Or with all options
skyforge profile create \
  --name "my_profile" \
  --birth-date "1985-03-15" \
  --birth-time "14:30" \
  --birth-location "New York, NY, USA"
```

### Generate Your Calendar

```bash
# Generate full year calendar
skyforge generate --year 2026

# Generate single month
skyforge generate --year 2026 --month 1

# Generate with specific format
skyforge generate --year 2026 --format pdf

# Preview a single day
skyforge preview --date 2026-01-15
```

## 📋 Requirements

- Python 3.10 or later
- Swiss Ephemeris data files (downloaded automatically)

## 🏗️ Project Structure

```
skyforge/
├── agent.md              # AI agent instructions
├── prd.txt               # Product requirements
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Project configuration
├── config/
│   ├── settings.yaml     # Global settings
│   └── profiles/         # User profiles
├── src/skyforge/
│   ├── cli.py            # Command-line interface
│   ├── models/           # Data models
│   ├── calculators/      # Domain calculators
│   ├── analyzers/        # Risk & wellness analyzers
│   ├── generators/       # Output generators
│   └── data/             # Reference data
└── tests/                # Test suite
```

## 📖 Documentation

- **[agent.md](agent.md)** - Technical specifications for developers
- **[prd.txt](prd.txt)** - Product requirements document

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key settings:
- `SKYFORGE_OUTPUT_DIR` - Output directory for generated files
- `SKYFORGE_DEFAULT_PROFILE` - Default profile name
- `SWISSEPH_PATH` - Swiss Ephemeris data path

### Settings File

Edit `config/settings.yaml` to customize:
- Output format preferences
- Calculation parameters
- Wellness recommendation rules
- Spiritual library rotation

## 🧪 Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=skyforge

# Run specific test file
pytest tests/test_calculators/test_numerology.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff src/ tests/

# Type checking
mypy src/
```

## 📄 Sample Output

```
╔══════════════════════════════════════════════════════════════════╗
║  SKYFORGE DAILY SOVEREIGN ALIGNMENT                              ║
║  Wednesday, January 15, 2026 (Day 15 of 365)                     ║
╠══════════════════════════════════════════════════════════════════╣
║  DAILY THEME: "Grounded Action with Emotional Wisdom"            ║
║  OVERALL ENERGY: Moderate-High | RISK LEVEL: Low                 ║
╚══════════════════════════════════════════════════════════════════╝

🌙 MOON: Waxing Gibbous (78%) in Taurus
🔢 NUMEROLOGY: Personal Day 5 (Universal Day 7)
☀️ SOLAR TRANSIT: Sun in Capricorn, 10th House Focus
🧬 HUMAN DESIGN: Gate 41 (Decrease) Active
☯️ I CHING: Hexagram 41 - Decrease
📊 BIORHYTHM: Physical +67% | Emotional +23% | Mental -12%
⚠️ RISK ANALYSIS: Low (Score: 22/100)

💫 TODAY'S AFFIRMATION:
   "I build my dreams with patient, steady hands."
```

## 🤝 Contributing

Contributions are welcome! Please read the contributing guidelines before submitting pull requests.

## 📜 License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

Copyright (C) 2025 **S&K Holding QT (Quantum Technologies)**

> **SK** = *staycuriousANDkeepsmilin* 🐧

See [LICENSE](LICENSE) for the full license text.

## 🙏 Acknowledgments

- Swiss Ephemeris for astronomical calculations
- The I Ching and Human Design communities
- All wisdom traditions represented in the spiritual library

---

**SkyForge** - *Scientifically mapped. Spiritually grounded.*
