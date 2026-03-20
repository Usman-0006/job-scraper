"""
Runner script for Scrapy spider
Execute this script to scrape job details after running Selenium
"""

import sys
import os
from pathlib import Path

# Add project root to path (parent of scrapy_project)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scrapy.crawler import CrawlerProcess
from scrapy_project.settings import *
from scrapy_project.spider import JobScrapeSpider

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scrapy_spider.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def run_spider():
    """Run the Scrapy spider"""
    
    logger.info("=" * 70)
    logger.info("Starting Scrapy Job Details Spider")
    logger.info("=" * 70)
    
    # Check if job_links.csv exists
    csv_path = Path('../data/raw/job_links.csv')
    if not csv_path.exists():
        logger.error(f"Job links CSV not found: {csv_path}")
        logger.error("Please run the Selenium scraper first to collect job URLs")
        return False
    
    try:
        # Configure Scrapy settings
        settings = {
            'BOT_NAME': 'job_scraper',
            'SPIDER_MODULES': ['scrapy_project.spiders'],
            'NEWSPIDER_MODULE': 'scrapy_project.spiders',
            'ROBOTSTXT_OBEY': True,
            'CONCURRENT_REQUESTS': 1,
            'DOWNLOAD_DELAY': 2,
            'COOKIES_ENABLED': False,
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'ITEM_PIPELINES': {
                'scrapy_project.pipelines.JobDuplicatesPipeline': 300,
                'scrapy_project.pipelines.JobCleaningPipeline': 400,
                'scrapy_project.pipelines.JobExportPipeline': 500,
            },
            'LOG_LEVEL': 'INFO',
        }
        
        # Create crawler process
        process = CrawlerProcess(settings)
        
        # Add spider
        process.crawl(JobScrapeSpider)
        
        # Start crawling
        process.start()
        
        logger.info("=" * 70)
        logger.info("Spider completed successfully")
        logger.info("=" * 70)
        
        return True
    
    except Exception as e:
        logger.error(f"Error running spider: {e}")
        return False


if __name__ == '__main__':
    success = run_spider()
    sys.exit(0 if success else 1)
