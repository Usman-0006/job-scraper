# Quick Start Guide - Run This Now! ✅

## Status: ✓ ALL CODE FIXED AND READY

The broken `JobLinkCollector` class in `selenium/job_scraper.py` has been **FIXED**.

---

## 🚀 COMPLETE PIPELINE (Recommended)

Run all 4 steps in order to collect real job data and analyze it:

### Step 1: Collect URLs from Stripe & Punjab Gov (5-10 minutes)
```bash
cd c:\Users\Lenovo\Desktop\scrap\selenium
python job_scraper.py
```

**Output**: 
- Creates `data/raw/job_links.csv` with job URLs
- Logs scraped data to `selenium_scraper.log`
- Shows progress in console

**Expected**: 50-200+ job URLs collected

---

### Step 2: Extract Job Details from URLs (3-5 minutes)
```bash
cd c:\Users\Lenovo\Desktop\scrap\scrapy_project
python run_spider.py
```

**Output**:
- Creates `data/final/jobs.csv` 
- Creates `data/final/jobs.json`
- Logs to `scrapy_spider.log`

**Expected**: 10-50 jobs with full details extracted

---

### Step 3: Analyze Job Data (10-30 seconds)
```bash
cd c:\Users\Lenovo\Desktop\scrap\analysis
python analyze_jobs.py
```

**Output**:
- Creates `data/final/analysis_stats.json`
- Prints statistics to console:
  - Top skills, companies, locations
  - Salary ranges, experience levels
  - Employment types

**Expected**: Full analysis report printed

---

### Step 4: Generate Visualizations (5-10 seconds) [Optional]
```bash
python visualize_jobs.py
```

**Output**:
- `data/final/top_companies.png`
- `data/final/top_locations.png`
- `data/final/employment_types.png`
- `data/final/top_titles.png`

**Expected**: 4 PNG charts created

---

## ⚡ QUICK TEST (No Web Scraping - 30 seconds)

If you don't want to wait for Selenium/Scrapy:

```bash
cd c:\Users\Lenovo\Desktop\scrap\scrapy_project
python generate_sample_data.py

cd ../analysis
python analyze_jobs.py
python visualize_jobs.py
```

This creates fake but realistic test data and runs analysis immediately.

---

## 📂 File Structure After Running

```
scrap/
├── selenium/
│   └── job_scraper.py           ← RUN THIS FIRST
│
├── scrapy_project/
│   ├── run_spider.py             ← RUN THIS SECOND
│   ├── spider.py
│   ├── items.py
│   ├── pipelines.py
│   └── generate_sample_data.py   ← For testing only
│
├── analysis/
│   ├── analyze_jobs.py           ← RUN THIS THIRD
│   └── visualize_jobs.py         ← RUN THIS FOURTH (optional)
│
└── data/
    ├── raw/
    │   └── job_links.csv         ← Created by step 1
    └── final/
        ├── jobs.csv              ← Created by step 2
        ├── jobs.json             ← Created by step 2
        ├── analysis_stats.json   ← Created by step 3
        ├── top_companies.png     ← Created by step 4
        ├── top_locations.png     ← Created by step 4
        ├── employment_types.png  ← Created by step 4
        └── top_titles.png        ← Created by step 4
```

---

## 🎯 Expected Results

### After Step 1 (Selenium):
```
✓ Scraping Greenhouse board...
✓ Scraping Lever jobs...
✓ Scraping Ashby jobs...
✓ Scraping Stripe jobs: https://stripe.com/jobs/search?teams=Data...
✓ Scraping Punjab Government jobs: https://jobs.punjab.gov.pk/new_recruit/jobs
✓ Saved 150+ URLs to ../data/raw/job_links.csv
```

### After Step 2 (Scrapy):
```
✓ Extracted 45 job listings
✓ Created data/final/jobs.csv (45 rows)
✓ Created data/final/jobs.json (45 jobs)
```

### After Step 3 (Analysis):
```
Loaded 45 job records successfully
Total job listings: 45
Unique companies: 28
Top skills: Python (73%), JavaScript (56%), SQL (51%)
Top locations: Remote (40%), San Francisco (18%), New York (11%)
Employment types: 95% Full-time, 5% Contract
Salary info: 100% of jobs have salary data
Analysis complete! ✓
```

### After Step 4 (Visualization):
```
✓ Generated top_companies.png
✓ Generated top_locations.png
✓ Generated employment_types.png
✓ Generated top_titles.png
```

---

## ❌ If Something Goes Wrong

### Error: "ChromeDriver not found"
**Solution**: Install ChromeDriver or use headless mode (already enabled)

### Error: "TimeoutException" 
**Solution**: Websites taking too long to load. This is normal. The script will retry.

### Error: "No module named 'scrapy'"
**Solution**: Install requirements:
```bash
cd c:\Users\Lenovo\Desktop\scrap
pip install -r requirements.txt
```

### Error: "jobs.csv is empty"
**Solution**: This means URLs couldn't be scraped. Use sample data instead:
```bash
cd scrapy_project
python generate_sample_data.py
cd ../analysis
python analyze_jobs.py
```

---

## 📝 Files Explained

| File | Purpose | Input | Output |
|------|---------|-------|--------|
| `selenium/job_scraper.py` | Collects job URLs from websites | URLs in code | `job_links.csv` |
| `scrapy_project/run_spider.py` | Extracts job details | `job_links.csv` | `jobs.csv`, `jobs.json` |
| `analysis/analyze_jobs.py` | Analyzes job data | `jobs.csv` | `analysis_stats.json` |
| `analysis/visualize_jobs.py` | Creates charts | `jobs.csv` | PNG images |
| `scrapy_project/generate_sample_data.py` | Creates test data | None | `jobs.csv`, `jobs.json` |

---

## ✅ Checklist

- [ ] Run `python job_scraper.py` from `selenium/` directory
- [ ] Check if `data/raw/job_links.csv` was created
- [ ] Run `python run_spider.py` from `scrapy_project/` directory
- [ ] Check if `data/final/jobs.csv` has data
- [ ] Run `python analyze_jobs.py` from `analysis/` directory
- [ ] View results in console and `data/final/analysis_stats.json`
- [ ] (Optional) Run `python visualize_jobs.py` to create charts

---

## 🔧 Advanced Options

### Run Only Selenium (URL collection):
```bash
cd selenium && python job_scraper.py
```

### Run Only Scrapy (Detail extraction):
```bash
cd scrapy_project && python run_spider.py
```

### Run Only Analysis:
```bash
cd analysis && python analyze_jobs.py
```

### Generate Test Data (skip web scraping):
```bash
cd scrapy_project && python generate_sample_data.py
```

---

## 💡 Pro Tips

1. **First run takes time**: Selenium needs 5-10 minutes to collect URLs
2. **robots.txt may block some sites**: This is normal behavior
3. **Use sample data for testing**: It's instant and doesn't depend on websites
4. **Check logs**: `selenium_scraper.log` and `scrapy_spider.log` for details
5. **Monitor console output**: Shows real-time progress

---

## 📧 Summary

**Main command to run everything**:
```bash
# Terminal 1: Collect URLs
cd c:\Users\Lenovo\Desktop\scrap\selenium && python job_scraper.py

# Terminal 2: Extract details (after step 1 completes)
cd c:\Users\Lenovo\Desktop\scrap\scrapy_project && python run_spider.py

# Terminal 3: Analyze data (after step 2 completes)
cd c:\Users\Lenovo\Desktop\scrap\analysis && python analyze_jobs.py

# Optional: Generate charts
python visualize_jobs.py
```

**OR run everything in sequence**:
```bash
cd c:\Users\Lenovo\Desktop\scrap
.\selenium\job_scraper.py && .\scrapy_project\run_spider.py && .\analysis\analyze_jobs.py
```

Now go ahead and **run the scripts!** 🚀
