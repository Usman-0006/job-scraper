# 🚀 Job Scraping Project

A complete end-to-end job scraping system using **Selenium** and **Scrapy** with proper Git workflow and data analysis.

## 📋 Project Overview

This project provides an automated solution for:

1. **Collecting Job URLs** - Uses Selenium to scrape job listing URLs from major job boards
2. **Scraping Job Details** - Uses Scrapy to extract detailed job information from collected URLs
3. **Data Analysis** - Analyzes the dataset to extract insights and patterns
4. **Visualization** - Creates charts and visualizations of job market data

### Target Job Boards

- **boards.greenhouse.io** - Greenhouse ATS-powered job boards
- **jobs.lever.co** - Lever recruitment platform
- **ashbyhq.com** - Ashby careers pages and powered sites (GitHub, Stripe, Rippling)

---

## 🗂️ Project Structure

```
job-scraper/
├── selenium/                    # Selenium web scraper for URL collection
│   ├── job_scraper.py          # Main Selenium scraper classes
│   ├── config.py               # Configuration and constants
│   └── selenium_scraper.log    # Selenium execution logs
│
├── scrapy_project/              # Scrapy spider for detailed scraping
│   ├── spider.py               # Main job details spider
│   ├── items.py                # Data structure definitions
│   ├── pipelines.py            # Data processing pipelines
│   ├── settings.py             # Scrapy configuration
│   ├── run_spider.py           # Spider launcher script
│   └── spiders/                # Spider modules
│
├── analysis/                    # Data analysis and visualization
│   ├── analyze_jobs.py         # Statistical analysis script
│   ├── visualize_jobs.py       # Visualization script
│   └── analysis.log            # Analysis execution logs
│
├── data/                        # Output data directory
│   ├── raw/                    # Raw data from Selenium
│   │   └── job_links.csv       # Collected job URLs
│   └── final/                  # Processed data
│       ├── jobs.csv            # Final job dataset (CSV)
│       ├── jobs.json           # Final job dataset (JSON)
│       ├── analysis_stats.json # Analysis statistics
│       ├── top_companies.png   # Company visualization
│       ├── top_locations.png   # Location visualization
│       ├── employment_types.png # Employment type pie chart
│       └── top_titles.png      # Job titles visualization
│
├── docs/                        # Documentation
│   └── GIT_WORKFLOW.md         # Git workflow guide
│
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
└── requirements.txt             # Python dependencies
```

---

## 🔧 Setup Instructions

### Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **Google Chrome/Chromium** (for Selenium)
- **Git** (for version control)

### 1. Clone the Repository

```bash
git clone https://github.com/Usman-0006/job-scraper.git
cd job-scraper
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Setup

```bash
python --version
python -c "import selenium; import scrapy; print('All dependencies installed!')"
```

---

## 🚀 Running the Project

### Step 1: Run Selenium Scraper (Collect Job URLs)

The Selenium scraper visits job boards and collects job listing URLs.

```bash
cd selenium
python job_scraper.py
```

**What it does:**
- Opens Greenhouse, Lever, and Ashby job boards
- Scrolls to load all available jobs
- Extracts job detail page URLs
- Saves URLs to `../data/raw/job_links.csv`

**Expected Output:**
```
INFO:root:Starting Job Link Collection
INFO:root:--- Running GreenhouseScraper ---
INFO:root:Collected 234 URLs from GreenhouseScraper
INFO:root:--- Running LeverScraper ---
INFO:root:Collected 156 URLs from LeverScraper
INFO:root:--- Running AshbyScraper ---
INFO:root:Collected 89 URLs from AshbyScraper
INFO:root:Total URLs collected: 479
✓ Saved 479 unique URLs to ../data/raw/job_links.csv
```

### Step 2: Run Scrapy Spider (Scrape Job Details)

The Scrapy spider reads collected URLs and extracts detailed job information.

```bash
cd scrapy_project
python run_spider.py
```

**What it does:**
- Reads URLs from `job_links.csv`
- Visits each job URL
- Extracts job details (title, company, location, description, skills, etc.)
- Removes duplicates and cleans data
- Exports to CSV and JSON

**Expected Output:**
```
INFO:root:Starting Scrapy Job Details Spider
INFO:root:Spider crawling 479 URLs...
[job_scraper] Crawled 479 pages
INFO:root:Removed 45 duplicate items
INFO:root:Cleaned 434 job records
✓ Exported 434 jobs to ../data/final/jobs.csv
✓ Exported 434 jobs to ../data/final/jobs.json
```

### Step 3: Analyze the Data

Run statistical analysis on the collected job data.

```bash
cd analysis
python analyze_jobs.py
```

**What it does:**
- Loads job data from `jobs.csv`
- Calculates statistics on skills, companies, locations, employment types
- Identifies role patterns (Intern, Junior, Senior, Staff)
- Extracts salary information
- Exports results to JSON

**Output Includes:**
```
BASIC STATISTICS
- Total job listings: 434
- Unique companies: 78
- Unique locations: 45

TOP 20 MOST REQUIRED SKILLS
1. Python           - 156 jobs (35.9%)
2. JavaScript       - 134 jobs (30.9%)
3. React           - 89 jobs (20.5%)
...

TOP 20 HIRING COMPANIES
1. Google          - 45 jobs (10.4%)
2. Microsoft       - 38 jobs (8.8%)
...

TOP 20 JOB LOCATIONS
1. San Francisco   - 67 jobs (15.4%)
2. New York        - 54 jobs (12.4%)
...

ROLE LEVEL DISTRIBUTION
- Intern          - 45 jobs (10.4%)
- Entry-Level     - 123 jobs (28.3%)
- Mid-Level       - 198 jobs (45.6%)
- Senior/Staff    - 68 jobs (15.7%)
```

### Step 4: Create Visualizations

Generate charts and visualizations of the data.

```bash
cd analysis
python visualize_jobs.py
```

**Creates PNG charts:**
- `top_companies.png` - Bar chart of top 15 hiring companies
- `top_locations.png` - Bar chart of top 15 job locations
- `employment_types.png` - Pie chart of employment type distribution
- `top_titles.png` - Bar chart of most common job titles

---

## 📊 Output Files Explanation

### Job Links CSV (`data/raw/job_links.csv`)
Collected job URLs from Selenium scraper.

| Column | Description |
|--------|-------------|
| Job URL | Direct link to job posting |
| Source | Job board source (Greenhouse, Lever, Ashby) |
| Scraped Date | When the URL was collected |

**Example:**
```csv
Job URL,Source,Scraped Date
https://greenhouse.io/app/jobs/123456,GreenhouseScraper,2024-01-15T10:30:00
https://lever.co/apply/789012,LeverScraper,2024-01-15T11:45:00
```

### Jobs CSV (`data/final/jobs.csv`)
Processed job details with all extracted information.

| Column | Description |
|--------|-------------|
| job_title | Job position title |
| company_name | Hiring company |
| location | Job location (city/remote) |
| department | Department (if available) |
| employment_type | Full-time, Part-time, Contract, Intern |
| posted_date | When job was posted |
| job_url | Link to job posting |
| job_description | Full job description text |
| required_skills | Required skills (comma-separated) |
| experience_level | Entry-level, Mid-level, Senior, etc. |
| salary | Salary range (if available) |
| source_board | Source job board |
| scrape_date | When data was scraped |

### Analysis JSON (`data/final/analysis_stats.json`)
Statistical summary of the job market.

```json
{
  "total_jobs": 434,
  "unique_companies": 78,
  "unique_locations": 45,
  "top_skills": {
    "Python": 156,
    "JavaScript": 134,
    "React": 89
  },
  "top_companies": {
    "Google": 45,
    "Microsoft": 38
  }
}
```

---

## 🔄 Git Workflow

This project follows a professional Git branching model:

```
master (main)
  ↑
  ├─ develop
      ├─ feature/selenium-scraper
      ├─ feature/scrapy-spider
      ├─ feature/data-analysis
      └─ bugfix/issue-name (if needed)
```

### Working with Branches

**Create and work on a feature:**
```bash
git checkout develop
git branch feature/my-feature
git checkout feature/my-feature

# Make changes and commit
git add .
git commit -m "feat: Add my feature"

# Merge back to develop
git checkout develop
git merge feature/my-feature

# Merge develop to main when ready for release
git checkout master
git merge develop
```

### Commit Message Format

```
feat(component): Add new feature
fix(component): Fix bug
docs: Update documentation
refactor: Code restructuring
chore: Dependency updates
```

For details, see [GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md)

---

## ⚠️ Important Notes

### Ethical Scraping

This project follows responsible scraping practices:

- ✅ Respects `robots.txt` rules
- ✅ Uses polite delays between requests (2+ seconds)
- ✅ Includes proper User-Agent headers
- ✅ Only scrapes publicly available data
- ✅ Does NOT bypass login or CAPTCHA
- ✅ Does NOT use aggressive scraping techniques

### Rate Limiting

The project includes:
- 2-second delays between requests
- Respect for robots.txt
- Proper caching
- Error handling and timeouts

### Data Privacy

- No personal data is stored beyond job listings
- All data is publicly available from job boards
- No login credentials are used
- No private user information is collected

---

## 🐛 Troubleshooting

### Selenium Issues

**Problem:** `No such file or directory: chromedriver`
```bash
# Solution: Install webdriver-manager
pip install webdriver-manager
```

**Problem:** Timeouts waiting for elements
```bash
# Solution: Increase WAIT_TIMEOUT in selenium/config.py
WAIT_TIMEOUT = 20  # Increase from 10
```

### Scrapy Issues

**Problem:** `ModuleNotFoundError: No module named 'scrapy_project'`
```bash
# Solution: Ensure you're in the scrapy_project directory
cd scrapy_project
python run_spider.py
```

**Problem:** No jobs exported
```bash
# Solution: Verify job_links.csv exists and has valid URLs
cd data/raw
cat job_links.csv | head
```

### Data Analysis Issues

**Problem:** `FileNotFoundError: jobs.csv not found`
```bash
# Solution: Run Scrapy spider first to generate jobs.csv
cd scrapy_project
python run_spider.py
```

---

## 📚 Technologies Used

| Component | Technology | Purpose |
|-----------|-----------|---------|
| URL Collection | Selenium 4 | Browser automation and web scraping |
| Data Scraping | Scrapy 2 | Large-scale web scraping framework |
| Data Processing | Pandas | Data manipulation and analysis |
| Visualization | Matplotlib | Chart generation |
| Data Format | CSV/JSON | Structured data export |

---

## 📈 Sample Analysis Output

```
TOTAL JOBS ANALYZED: 434

TOP 5 SKILLS:
1. Python (35.9%)
2. JavaScript (30.9%)
3. React (20.5%)
4. TypeScript (19.1%)
5. Node.js (17.9%)

TOP 5 COMPANIES:
1. Google (10.4%)
2. Microsoft (8.8%)
3. Amazon (7.6%)
4. Apple (6.9%)
5. Meta (5.8%)

TOP 5 LOCATIONS:
1. San Francisco (15.4%)
2. New York (12.4%)
3. Seattle (9.2%)
4. Remote (31.3%)
5. Austin (7.1%)

ROLE DISTRIBUTION:
- Internships: 45 (10.4%)
- Entry-Level: 123 (28.3%)
- Mid-Level: 198 (45.6%)
- Senior/Staff: 68 (15.7%)
```

---

## 🤝 Contributing

To contribute to this project:

1. Create a feature branch from `develop`
2. Make your changes with meaningful commits
3. Merge back to `develop` after testing
4. Create a pull request to `master` when ready

---

## 📝 License

This project is for educational purposes. Ensure you comply with each job board's Terms of Service and robots.txt when scraping.

---

## 📞 Support & Issues

For issues or questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the commit history for clues
3. Check error logs in `*.log` files
4. Create a `bugfix/` branch if you find an issue

---

## 🎯 Future Enhancements

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Real-time job alerts
- [ ] Salary prediction model
- [ ] Skills recommendation system
- [ ] Web dashboard for browsing results
- [ ] Scheduled scraping (cron jobs)
- [ ] Email notifications
- [ ] Resume matching algorithm

---

**Made with ❤️ for job seekers and data enthusiasts**

Last Updated: January 2024
