# ⚡ Quick Start Guide

Get the job scraper running in 5 minutes!

## Minimal Setup (Windows)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Selenium Scraper

```bash
cd selenium
python job_scraper.py
```

Output: `data/raw/job_links.csv` (list of job URLs)

### 3. Run Scrapy Spider

```bash
cd ../scrapy_project
python run_spider.py
```

Output: `data/final/jobs.csv` (detailed job data)

### 4. Analyze Data

```bash
cd ../analysis
python analyze_jobs.py
```

Output: Statistics, top skills, top companies, locations

### 5. Create Visualizations (Optional)

```bash
python visualize_jobs.py
```

Output: PNG charts in `data/final/`

---

## File Locations

| File | Created By | Location |
|------|-----------|----------|
| job_links.csv | Selenium | `data/raw/` |
| jobs.csv | Scrapy | `data/final/` |
| jobs.json | Scrapy | `data/final/` |
| analysis_stats.json | Analysis | `data/final/` |
| *.png charts | Visualization | `data/final/` |

---

## Troubleshooting

**Chrome not found:**
- Install Chrome or Chromium
- WebDriver auto-downloads driver

**Module not found:**
- Ensure you installed requirements.txt
- Check virtual environment is activated

**No jobs collected:**
- Check internet connection
- Job boards might have changed structure
- Check selenium logs for errors

---

## Full Documentation

See [README.md](../README.md) for complete documentation.

See [GIT_WORKFLOW.md](GIT_WORKFLOW.md) for branching guide.
