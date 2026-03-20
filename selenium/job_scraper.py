"""
Selenium Job Scraper
Scrapes job listing URLs from multiple job boards:
- boards.greenhouse.io
- jobs.lever.co
- ashbyhq.com/careers
"""

import time
import csv
import logging
from datetime import datetime
from typing import List, Set
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('selenium_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class JobBoardScraper:
    """Base class for scraping job boards"""
    
    def __init__(self, headless=True):
        """Initialize Chrome WebDriver"""
        self.headless = headless
        self.driver = None
        self.job_urls = set()
        self.wait = None
        
    def setup_driver(self):
        """Configure and start Chrome WebDriver"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        chrome_options.add_argument('--start-maximized')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            logger.info("Chrome WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def quit_driver(self):
        """Close WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")
    
    def scrape(self):
        """Override in subclasses"""
        raise NotImplementedError
    
    def save_urls(self, filename):
        """Save collected URLs to CSV"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Job URL', 'Source', 'Scraped Date'])
                for url in sorted(self.job_urls):
                    writer.writerow([url, self.__class__.__name__, datetime.now().isoformat()])
            logger.info(f"Saved {len(self.job_urls)} URLs to {filename}")
        except Exception as e:
            logger.error(f"Error saving URLs: {e}")

class StripeScraper(JobBoardScraper):
    """Scraper for Stripe jobs"""
    
    def scrape(self):
        """Scrape Stripe job listings"""
        self.setup_driver()
        try:
            # Stripe jobs search URL with specific teams
            stripe_url = "https://stripe.com/jobs/search?teams=Data+%26+Data+Science&teams=Security&teams=University"
            logger.info(f"Scraping Stripe jobs: {stripe_url}")
            self._scrape_stripe_jobs(stripe_url)
        finally:
            self.quit_driver()
    
    def _scrape_stripe_jobs(self, url):
        """Scrape Stripe job listings"""
        try:
            self.driver.get(url)
            time.sleep(3)  # Wait for page to load
            
            # Wait for job listings to appear
            try:
                self.wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "[data-testid='job-listing']")
                ))
            except TimeoutException:
                logger.warning("Timeout waiting for Stripe job listings")
                # Try alternative selectors
                try:
                    self.wait.until(EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, "job-listing")
                    ))
                except TimeoutException:
                    logger.warning("No job listings found with alternative selectors")
                    return
            
            # Scroll to load all jobs
            self._scroll_until_loaded(max_scrolls=10)
            
            # Extract job URLs using multiple selector strategies
            job_urls = set()
            
            # Strategy 1: data-testid selector
            job_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='job-listing'] a")
            for element in job_elements:
                try:
                    href = element.get_attribute("href")
                    if href and "stripe.com/jobs" in href:
                        job_urls.add(href)
                except Exception as e:
                    logger.debug(f"Error extracting Stripe job URL: {e}")
            
            # Strategy 2: class-based selector
            if not job_urls:
                job_elements = self.driver.find_elements(By.CLASS_NAME, "job-listing")
                for element in job_elements:
                    try:
                        links = element.find_elements(By.TAG_NAME, "a")
                        for link in links:
                            href = link.get_attribute("href")
                            if href and "stripe.com/jobs" in href:
                                job_urls.add(href)
                    except Exception as e:
                        logger.debug(f"Error extracting Stripe job URL: {e}")
            
            # Strategy 3: Generic link search
            if not job_urls:
                all_links = self.driver.find_elements(By.TAG_NAME, "a")
                for link in all_links:
                    try:
                        href = link.get_attribute("href")
                        text = link.text.lower()
                        if href and "stripe.com/jobs" in href and any(keyword in text for keyword in 
                            ['data', 'science', 'security', 'university', 'engineer', 'analyst']):
                            job_urls.add(href)
                    except Exception as e:
                        logger.debug(f"Error extracting Stripe job URL: {e}")
            
            logger.info(f"Found {len(job_urls)} Stripe job URLs")
            self.job_urls.update(job_urls)
            
        except Exception as e:
            logger.error(f"Error scraping Stripe jobs: {e}")


class PunjabGovScraper(JobBoardScraper):
    """Scraper for Punjab Government jobs"""
    
    def scrape(self):
        """Scrape Punjab Government job listings"""
        self.setup_driver()
        try:
            punjab_url = "https://jobs.punjab.gov.pk/new_recruit/jobs"
            logger.info(f"Scraping Punjab Government jobs: {punjab_url}")
            self._scrape_punjab_jobs(punjab_url)
        finally:
            self.quit_driver()
    
    def _scrape_punjab_jobs(self, url):
        """Scrape Punjab Government job listings"""
        try:
            self.driver.get(url)
            time.sleep(3)  # Wait for page to load
            
            # Wait for job listings to appear
            try:
                self.wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "table tbody tr")
                ))
            except TimeoutException:
                logger.warning("Timeout waiting for Punjab job listings")
                return
            
            # Scroll to load all jobs
            self._scroll_until_loaded(max_scrolls=5)
            
            # Extract job URLs from table rows
            job_urls = set()
            
            # Look for job links in table rows
            table_rows = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
            logger.info(f"Found {len(table_rows)} table rows")
            
            for row in table_rows:
                try:
                    # Look for links in the row
                    links = row.find_elements(By.TAG_NAME, "a")
                    for link in links:
                        href = link.get_attribute("href")
                        text = link.text.strip().lower()
                        
                        # Filter for job-related links
                        if href and ("jobs.punjab.gov.pk" in href or "/job/" in href or 
                                   any(keyword in text for keyword in 
                                       ['recruitment', 'vacancy', 'position', 'job'])):
                            if href.startswith("http"):
                                job_urls.add(href)
                            elif href.startswith("/"):
                                # Convert relative URL to absolute
                                base_url = "https://jobs.punjab.gov.pk"
                                full_url = base_url + href
                                job_urls.add(full_url)
                                
                except Exception as e:
                    logger.debug(f"Error extracting Punjab job URL: {e}")
            
            # Alternative: Look for job detail links
            if not job_urls:
                all_links = self.driver.find_elements(By.TAG_NAME, "a")
                for link in all_links:
                    try:
                        href = link.get_attribute("href")
                        text = link.text.strip().lower()
                        
                        if href and ("detail" in href or "view" in href or 
                                   any(keyword in text for keyword in 
                                       ['apply', 'details', 'vacancy', 'recruitment'])):
                            if href.startswith("http"):
                                job_urls.add(href)
                            elif href.startswith("/"):
                                base_url = "https://jobs.punjab.gov.pk"
                                full_url = base_url + href
                                job_urls.add(full_url)
                    except Exception as e:
                        logger.debug(f"Error extracting Punjab job URL: {e}")
            
            logger.info(f"Found {len(job_urls)} Punjab Government job URLs")
            self.job_urls.update(job_urls)
            
        except Exception as e:
            logger.error(f"Error scraping Punjab Government jobs: {e}")
    
    def _scroll_until_loaded(self, max_scrolls=5):
        """Scroll page to load all jobs"""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scrolls = 0
        
        while scrolls < max_scrolls:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scrolls += 1


class JobLinkCollector:
    """Main coordinator for scraping all job boards"""
    
    def __init__(self, output_file='../data/raw/job_links.csv'):
        self.output_file = output_file
        self.all_urls = set()
    
    def scrape_all(self):
        """Run all scrapers"""
        logger.info("=" * 50)
        logger.info("Starting Job Link Collection")
        logger.info("=" * 50)
        
        scrapers = [
            StripeScraper(headless=True),
            PunjabGovScraper(headless=True),
        ]
        
        for scraper in scrapers:
            try:
                logger.info(f"\n--- Running {scraper.__class__.__name__} ---")
                scraper.scrape()
                self.all_urls.update(scraper.job_urls)
                logger.info(f"Collected {len(scraper.job_urls)} URLs from {scraper.__class__.__name__}")
            except Exception as e:
                logger.error(f"Failed to run {scraper.__class__.__name__}: {e}")
        
        # Save all URLs
        self._save_all_urls()
        logger.info("=" * 50)
        logger.info(f"Job scraping completed. Total URLs collected: {len(self.all_urls)}")
        logger.info("=" * 50)
    
    def _save_all_urls(self):
        """Save all collected URLs to CSV"""
        try:
            with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Job URL', 'Source', 'Scraped Date'])
                
                for url in sorted(self.all_urls):
                    writer.writerow([url, 'Multiple Sources', datetime.now().isoformat()])
            
            logger.info(f"✓ Saved {len(self.all_urls)} unique URLs to {self.output_file}")
        except Exception as e:
            logger.error(f"Error saving URLs: {e}")


if __name__ == "__main__":
    collector = JobLinkCollector('../data/raw/job_links.csv')
    collector.scrape_all()
