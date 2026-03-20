"""
Configuration and utility functions for Selenium scraper
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Selenium Configuration
HEADLESS_MODE = os.getenv('HEADLESS_MODE', 'True') == 'True'
WAIT_TIMEOUT = int(os.getenv('WAIT_TIMEOUT', '10'))
SCROLL_PAUSE_TIME = float(os.getenv('SCROLL_PAUSE_TIME', '1.5'))
MAX_SCROLL_ATTEMPTS = int(os.getenv('MAX_SCROLL_ATTEMPTS', '5'))

# Job Board URLs
GREENHOUSE_BOARDS = [
    'https://boards.greenhouse.io/uber/jobs',
    'https://boards.greenhouse.io/google/jobs',
    'https://boards.greenhouse.io/microsoft/jobs',
    'https://boards.greenhouse.io/apple/jobs',
    'https://boards.greenhouse.io/amazon/jobs',
]

LEVER_URLS = [
    'https://jobs.lever.co/search',
]

ASHBY_URLS = [
    'https://ashbyhq.com/careers',
    'https://github.com/careers',
    'https://stripe.com/jobs',
    'https://rippling.com/careers',
]

# Output Configuration
OUTPUT_DIR = '../data/raw'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'job_links.csv')

# Search Keywords
SEARCH_KEYWORDS = [
    'Software Engineer',
    'Data Analyst',
    'Intern',
    'Product Manager',
    'DevOps Engineer',
]

# Delays between requests (in seconds)
POLITE_DELAY = 2
SCROLL_DELAY = 1.5
