# Scrapy settings for job_scraper project

BOT_NAME = 'job_scraper'

SPIDER_MODULES = ['job_scraper.spiders']
NEWSPIDER_MODULE = 'job_scraper.spiders'

# Crawl responsibly by identifying yourself
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests per domain
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# Configure a delay for requests for the same domain
DOWNLOAD_DELAY = 2

# Disable cookies
COOKIES_ENABLED = False

# Configure item pipelines
ITEM_PIPELINES = {
    'job_scraper.pipelines.JobDuplicatesPipeline': 300,
    'job_scraper.pipelines.JobCleaningPipeline': 400,
    'job_scraper.pipelines.JobExportPipeline': 500,
}

# Enable and configure HTTP caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600

# Log level
LOG_LEVEL = 'INFO'

# Export formats
JOBSCOUT_EXPORTS = {
    'csv': 'jobs.csv',
    'json': 'jobs.json',
}
