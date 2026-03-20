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


class GreenhouseScraper(JobBoardScraper):
    """Scraper for boards.greenhouse.io"""
    
    BOARDS = [
        'https://boards.greenhouse.io/uber/jobs',
        'https://boards.greenhouse.io/google/jobs',
        'https://boards.greenhouse.io/microsoft/jobs',
        'https://boards.greenhouse.io/apple/jobs',
        'https://boards.greenhouse.io/amazon/jobs',
    ]
    
    SEARCH_KEYWORDS = ['Software Engineer', 'Data Analyst', 'Intern']
    
    def scrape(self):
        """Scrape Greenhouse job boards"""
        self.setup_driver()
        try:
            for board_url in self.BOARDS:
                logger.info(f"Scraping Greenhouse board: {board_url}")
                self._scrape_board(board_url)
        finally:
            self.quit_driver()
    
    def _scrape_board(self, board_url):
        """Scrape a single Greenhouse board"""
        try:
            self.driver.get(board_url)
            time.sleep(2)
            
            # Wait for job listings to load
            try:
                self.wait.until(EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "opening")
                ))
            except TimeoutException:
                logger.warning(f"Timeout waiting for jobs on {board_url}")
                return
            
            # Scroll to load all jobs
            self._scroll_until_loaded()
            
            # Extract job URLs
            job_elements = self.driver.find_elements(By.CLASS_NAME, "opening")
            logger.info(f"Found {len(job_elements)} job openings")
            
            for element in job_elements:
                try:
                    job_link = element.find_element(By.TAG_NAME, "a")
                    job_url = job_link.get_attribute("href")
                    if job_url:
                        self.job_urls.add(job_url)
                        logger.debug(f"Added URL: {job_url}")
                except StaleElementReferenceException:
                    continue
                except Exception as e:
                    logger.debug(f"Error extracting job URL: {e}")
                    
        except Exception as e:
            logger.error(f"Error scraping Greenhouse board: {e}")
    
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
        
        logger.debug(f"Scrolled {scrolls} times")


class LeverScraper(JobBoardScraper):
    """Scraper for jobs.lever.co"""
    
    SEARCH_URLS = [
        'https://jobs.lever.co/search?location=remote&commitment=',
        'https://jobs.lever.co/search?location=United%20States',
    ]
    
    def scrape(self):
        """Scrape Lever job listings"""
        self.setup_driver()
        try:
            logger.info("Starting Lever.co scraping")
            self._scrape_lever_search()
        finally:
            self.quit_driver()
    
    def _scrape_lever_search(self):
        """Scrape Lever job search results"""
        try:
            url = 'https://jobs.lever.co/search'
            self.driver.get(url)
            time.sleep(2)
            
            # Wait for search results
            try:
                self.wait.until(EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "item")
                ))
            except TimeoutException:
                logger.warning("Timeout waiting for Lever jobs")
                return
            
            # Scroll to load more
            self._scroll_until_loaded(max_scrolls=10)
            
            # Extract job URLs
            job_cards = self.driver.find_elements(By.CLASS_NAME, "item")
            logger.info(f"Found {len(job_cards)} job listings on Lever")
            
            for card in job_cards:
                try:
                    job_link = card.find_element(By.TAG_NAME, "a")
                    job_url = job_link.get_attribute("href")
                    if job_url and job_url.startswith("http"):
                        self.job_urls.add(job_url)
                        logger.debug(f"Added Lever URL: {job_url}")
                except StaleElementReferenceException:
                    continue
                except Exception as e:
                    logger.debug(f"Error extracting Lever URL: {e}")
                    
        except Exception as e:
            logger.error(f"Error scraping Lever: {e}")
    
    def _scroll_until_loaded(self, max_scrolls=5):
        """Scroll page to load all jobs (same as Greenhouse)"""
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


class AshbyScraper(JobBoardScraper):
    """Scraper for ashbyhq.com/careers"""
    
    COMPANY_CAREERS = [
        'https://ashbyhq.com/careers',  # Ashby's own careers page
        'https://github.com/careers',   # GitHub (uses Ashby)
        'https://stripe.com/jobs',      # Stripe (uses Ashby)
        'https://rippling.com/careers',  # Rippling (uses Ashby)
    ]
    
    def scrape(self):
        """Scrape Ashby-powered job boards"""
        self.setup_driver()
        try:
            for company_url in self.COMPANY_CAREERS:
                logger.info(f"Scraping Ashby board: {company_url}")
                self._scrape_company_careers(company_url)
                time.sleep(2)
        finally:
            self.quit_driver()
    
    def _scrape_company_careers(self, company_url):
        """Scrape jobs from Ashby-powered careers page"""
        try:
            self.driver.get(company_url)
            time.sleep(2)
            
            # Wait for job listings
            try:
                self.wait.until(EC.presence_of_all_elements_located(
                    (By.TAG_NAME, "a")
                ))
            except TimeoutException:
                logger.warning(f"Timeout waiting for Ashby jobs on {company_url}")
                return
            
            # Scroll to load more
            self._scroll_until_loaded(max_scrolls=5)
            
            # Try to find job links
            all_links = self.driver.find_elements(By.TAG_NAME, "a")
            job_urls = set()
            
            for link in all_links:
                try:
                    href = link.get_attribute("href")
                    text = link.text.lower()
                    
                    # Filter for job-related links
                    if href and ("/job" in href or "/jobs" in href or 
                                "career" in href or "position" in text):
                        if href.startswith("http"):
                            job_urls.add(href)
                except StaleElementReferenceException:
                    continue
            
            logger.info(f"Found {len(job_urls)} job links on {company_url}")
            self.job_urls.update(job_urls)
            
        except Exception as e:
            logger.error(f"Error scraping Ashby board {company_url}: {e}")
    
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
            GreenhouseScraper(headless=True),
            LeverScraper(headless=True),
            AshbyScraper(headless=True),
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
    collector = JobLinkCollector(output_file='../data/raw/job_links.csv')
    collector.scrape_all()
