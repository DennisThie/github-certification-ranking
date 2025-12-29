# 🏆 GitHub Certifications Rankings

[![Generate GitHub Certifications Rankings](https://github.com/YOUR_USERNAME/gh-cert/actions/workflows/generate-rankings.yml/badge.svg)](https://github.com/YOUR_USERNAME/gh-cert/actions/workflows/generate-rankings.yml)

> Automated daily rankings of GitHub Certifications leaders across different regions worldwide.

---

## 📊 Rankings Index

### 🌎 Regional Rankings

| Region | Ranking | Description |
|--------|---------|-------------|
| 🇧🇷 | [**TOP 10 Brazil**](TOP10_BRAZIL.md) | Top certified professionals in Brazil |
| 🌎 | [**TOP 10 Americas**](TOP10_AMERICAS.md) | Leaders across North, Central & South America |
| 🇪🇺 | [**TOP 10 Europe**](TOP10_EUROPE.md) | Top performers in European countries |
| 🌏 | [**TOP 10 Asia**](TOP10_ASIA.md) | Asian region certification leaders |
| 🌊 | [**TOP 10 Oceania**](TOP10_OCEANIA.md) | Australia, New Zealand & Pacific islands |

### 🌍 Global Ranking

| Scope | Ranking | Description |
|-------|---------|-------------|
| 🌍 | [**TOP 10 World**](TOP10_WORLD.md) | Global top 10 across all countries |

## 🔄 How It Works

The rankings are automatically updated daily via GitHub Actions:

1. **Data Collection**: Fetches certification data from Credly API for multiple countries
2. **Processing**: Consolidates data from all CSV files
3. **Ranking Generation**: Creates TOP 10 rankings for each region
4. **Auto-Commit**: Updates markdown files automatically

## 🚀 Manual Execution

You can manually trigger the rankings generation:

1. Go to the [Actions tab](../../actions)
2. Select "Generate GitHub Certifications Rankings"
3. Click "Run workflow"

## 💻 Local Execution

To generate rankings locally:

```bash
# Make sure you have CSV files in the repository
python3 generate_rankings.py
```

## 📁 Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── generate-rankings.yml    # GitHub Actions workflow
├── cert-github.sh                   # Script to fetch certification data
├── generate_rankings.py             # Main ranking generator
├── github-certs-*.csv              # Certification data files
├── TOP10_*.md                      # Generated ranking files
└── README.md                       # This file
```

## 🛠️ Data Source

Data is sourced from the [Credly API](https://www.credly.com/api/v1/directory) for GitHub certifications.

## 📝 License

This project is open source and available under the MIT License.

---

*Last updated: Automated via GitHub Actions*
