"""
Scrapy spider for scraping job details from URLs collected by Selenium
"""

import scrapy
import csv
import logging
from datetime import datetime
from .items import JobItem, JobLoader
from scrapy.loader import ItemLoader

logger = logging.getLogger(__name__)


class JobScrapeSpider(scrapy.Spider):
    """Main spider for scraping job details"""
    
    name = 'job_scraper'
    allowed_domains = [
                      'stripe.com' 'jobs.punjab.gov.pk']
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 2,
        'ROBOTSTXT_OBEY': False,  # Many job boards block; we'll respect manually
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'COOKIES_ENABLED': False,
        'RETRY_TIMES': 3,
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_urls = []
        self.processed_count = 0
        self.error_count = 0
        self.skipped_count = 0
    
    def start_requests(self):
        """Read URLs from CSV and create requests"""
        csv_file = '../data/raw/job_links.csv'
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    url = row.get('Job URL', '').strip()
                    if url:
                        self.job_urls.append(url)
                        logger.info(f"Queued URL: {url}")
        except FileNotFoundError:
            logger.error(f"Job links file not found: {csv_file}")
            return
        except Exception as e:
            logger.error(f"Error reading job links: {e}")
            return
        
        logger.info(f"Starting to scrape {len(self.job_urls)} job URLs")
        
        for url in self.job_urls:
            # Skip login pages and non-job pages
            if any(skip in url.lower() for skip in ['login', '/ae/', '/at/', '/au/', '/br/', '/ca/', '/de/', '/jobs?']):
                logger.warning(f"Skipping non-job page: {url}")
                self.skipped_count += 1
                continue
            
            yield scrapy.Request(
                url,
                callback=self.parse,
                errback=self.errback,
                meta={'url': url}
            )
    
    def parse(self, response):
        """Parse job detail page"""
        url = response.url
        logger.info(f"Parsing: {url} (Status: {response.status})")
        
        # Skip login pages and redirects
        if response.status == 403 or 'login' in response.url.lower():
            logger.warning(f"Login page or forbidden: {url}")
            self.skipped_count += 1
            return
        
        loader = JobLoader(item=JobItem(), response=response)
        
        try:
            # Determine source and parse accordingly
            if 'punjab.gov.pk' in url:
                yield from self._parse_punjab_gov(response, loader)
            elif 'greenhouse' in url:
                yield from self._parse_greenhouse(response, loader)
            elif 'lever' in url:
                yield from self._parse_lever(response, loader)
            else:
                yield from self._parse_generic(response, loader)
        
        except Exception as e:
            logger.error(f"Error parsing {url}: {e}", exc_info=True)
            self.error_count += 1
    
    def _parse_punjab_gov(self, response, loader):
        """Parse Punjab Government job listings"""
        
        # Extract job title
        title_xpath = '//h2[@class="card-title"]/text() | //h1/text() | //div[@class="job-title"]/text()'
        loader.add_xpath('job_title', title_xpath)
        
        # Extract company name
        loader.add_value('company_name', 'Punjab Government')
        
        # Extract location
        location_xpath = '//span[@class="location"]/text() | //div[contains(text(), "Location")]/following::div/text()'
        loader.add_xpath('location', location_xpath)
        
        # Extract job description from all text content
        description_xpath = '//div[@class="job-content"]//text() | //div[@class="description"]//text() | //article//text()'
        loader.add_xpath('job_description', description_xpath)
        
        # Extract employment type
        employment_xpath = '//span[contains(text(), "Full-time") or contains(text(), "Part-time") or contains(text(), "Permanent") or contains(text(), "Contract")]/text()'
        loader.add_xpath('employment_type', employment_xpath)
        
        # Extract salary
        salary_xpath = '//span[@class="salary"]/text() | //div[contains(text(), "Salary")]/following::div/text()'
        loader.add_xpath('salary', salary_xpath)
        
        # Extract posted date
        date_xpath = '//span[@class="date"]/text() | //div[contains(text(), "Posted")]/following::div/text()'
        loader.add_xpath('posted_date', date_xpath)
        
        # Extract experience level
        experience_xpath = '//span[@class="experience"]/text() | //div[contains(text(), "Experience")]/following::div/text()'
        loader.add_xpath('experience_level', experience_xpath)
        
        loader.add_value('job_url', response.url)
        loader.add_value('source_board', 'punjab_gov')
        loader.add_value('scrape_date', datetime.now().isoformat())
        
        item = loader.load_item()
        
        # Check if we have meaningful data
        if item.get('job_title') and len(str(item.get('job_title', ''))) > 3:
            self.processed_count += 1
            logger.info(f"✓ Extracted: {item.get('job_title')}")
            yield item
        else:
            logger.warning(f"Insufficient data from {response.url}")
            self.error_count += 1
    
    def _parse_greenhouse(self, response, loader):
        """Parse Greenhouse job board"""
        
        loader.add_xpath('job_title', '//h1/text() | //h2[@class="opening-title"]/text()')
        loader.add_value('company_name', self._extract_company_from_url(response.url) or 'Unknown')
        loader.add_xpath('location', '//div[@class="location"]//text() | //span[@class="location"]/text()')
        loader.add_xpath('job_description', '//div[@class="content"]//text()')
        loader.add_xpath('employment_type', '//span[contains(text(), "Full-time") or contains(text(), "Part-time")]/text()')
        loader.add_xpath('posted_date', '//span[contains(text(), "Posted")]/following::text()[1]')
        loader.add_xpath('required_skills', '//h3[contains(text(), "Required")]/following::li/text()')
        
        loader.add_value('job_url', response.url)
        loader.add_value('source_board', 'greenhouse')
        loader.add_value('scrape_date', datetime.now().isoformat())
        
        item = loader.load_item()
        if item.get('job_title'):
            self.processed_count += 1
            yield item
    
    def _parse_lever(self, response, loader):
        """Parse Lever job board"""
        
        loader.add_xpath('job_title', '//h2[@class="page-title"]/text() | //h1/text()')
        loader.add_xpath('company_name', '//a[@class="company-name"]/text()')
        loader.add_xpath('location', '//div[@class="location"]/text() | //span[@class="location"]/text()')
        loader.add_xpath('employment_type', '//span[contains(text(), "Full-time") or contains(text(), "Part-time")]/text()')
        loader.add_xpath('job_description', '//div[@class="description"]//text()')
        loader.add_xpath('posted_date', '//span[@class="posted-date"]/text()')
        loader.add_xpath('required_skills', '//h3[contains(text(), "Skills")]/following::li/text()')
        
        loader.add_value('job_url', response.url)
        loader.add_value('source_board', 'lever')
        loader.add_value('scrape_date', datetime.now().isoformat())
        
        item = loader.load_item()
        if item.get('job_title'):
            self.processed_count += 1
            yield item
    
    def _parse_generic(self, response, loader):
        """Parse generic job page"""
        
        loader.add_xpath('job_title', 
            '//h1/text() | //h2/text() | //span[@class="job-title"]/text() | //div[@class="title"]/text()')
        
        loader.add_value('company_name', self._extract_company_from_url(response.url) or 'Unknown')
        
        loader.add_xpath('location',
            '//span[@class="location"]/text() | //div[@class="location"]/text() | //span[contains(text(), "Location")]/following::text()')
        
        loader.add_xpath('job_description',
            '//div[@class="description"]//text() | //article//text() | //div[@class="content"]//text()')
        
        loader.add_xpath('employment_type',
            '//span[contains(text(), "Full-time") or contains(text(), "Part-time") or contains(text(), "Contract")]/text()')
        
        loader.add_xpath('salary',
            '//span[@class="salary"]/text() | //div[contains(text(), "Salary")]/following::text()')
        
        loader.add_xpath('posted_date',
            '//span[contains(text(), "Posted")]/following::text()[1] | //time/@datetime')
        
        loader.add_xpath('required_skills',
            '//h3[contains(text(), "Requirements")]/following::li/text() | //div[@class="requirements"]//li/text()')
        
        loader.add_value('job_url', response.url)
        loader.add_value('source_board', 'generic')
        loader.add_value('scrape_date', datetime.now().isoformat())
        
        item = loader.load_item()
        if item.get('job_title') and len(str(item.get('job_title', ''))) > 3:
            self.processed_count += 1
            yield item
    
    def _extract_company_from_url(self, url):
        """Extract company name from URL"""
        url_lower = url.lower()
        
        if 'boards.greenhouse.io' in url_lower:
            parts = url.split('/')
            if len(parts) > 3:
                return parts[3].replace('-', ' ').title()
        elif 'jobs.lever.co' in url_lower:
            parts = url.split('/')
            if len(parts) > 3:
                return parts[3].replace('-', ' ').title()
        elif 'github' in url_lower:
            return 'GitHub'
        elif 'stripe' in url_lower:
            return 'Stripe'
        elif 'rippling' in url_lower:
            return 'Rippling'
        elif 'punjab.gov.pk' in url_lower:
            return 'Punjab Government'
        
        return None
    
    def errback(self, failure):
        """Handle request errors"""
        self.error_count += 1
        url = failure.request.meta.get('url', 'Unknown')
        logger.warning(f"Error downloading {url}: {failure.type.__name__}")
    
    def closed(self, reason):
        """Called when spider is closed"""
        logger.info("=" * 70)
        logger.info("SPIDER CLOSED - STATISTICS")
        logger.info("=" * 70)
        logger.info(f"Total URLs queued: {len(self.job_urls)}")
        logger.info(f"URLs skipped: {self.skipped_count}")
        logger.info(f"Successfully processed: {self.processed_count}")
        logger.info(f"Errors encountered: {self.error_count}")
        if len(self.job_urls) - self.skipped_count > 0:
            success_rate = (self.processed_count / (len(self.job_urls) - self.skipped_count) * 100)
            logger.info(f"Success rate: {success_rate:.1f}%")
        logger.info("=" * 70)
    
    def parse(self, response):
        """Parse job detail page"""
        url = response.url
        logger.info(f"Parsing: {url}")
        
        loader = JobLoader(item=JobItem(), response=response)
        
        try:
            # Determine job board source
            source_board = self._detect_source(url)
            
            # Parse based on source
            if 'greenhouse' in url:
                yield from self._parse_greenhouse(response, loader, source_board)
            elif 'lever' in url:
                yield from self._parse_lever(response, loader, source_board)
            else:
                yield from self._parse_generic(response, loader, source_board)
        
        except Exception as e:
            logger.error(f"Error parsing {url}: {e}")
            self.error_count += 1
    
    def _detect_source(self, url):
        """Detect job board source from URL"""
        if 'greenhouse' in url:
            return 'greenhouse'
        elif 'lever' in url:
            return 'lever'
        elif 'ashby' in url or 'github.com' in url or 'stripe.com' in url or 'rippling' in url:
            return 'ashby'
        else:
            return 'unknown'
    
    def _parse_greenhouse(self, response, loader, source_board):
        """Parse Greenhouse job board"""
        
        # Extract job title
        loader.add_xpath('job_title', '//h1/text()[1]')
        
        # Extract company name from URL or page
        loader.add_value('company_name', self._extract_company_from_url(response.url) or 'Unknown')
        
        # Extract location
        loader.add_xpath('location', '//div[@class="location-info"]//span/text()')
        
        # Extract job description
        loader.add_xpath('job_description', '//div[@class="content"]//text()')
        
        # Extract employment type
        loader.add_xpath('employment_type', '//span[contains(text(), "Full-time") or contains(text(), "Part-time") or contains(text(), "Contract")]/text()')
        
        # Extract posted date
        loader.add_xpath('posted_date', '//span[contains(text(), "Posted")]/following-sibling::text()')
        
        # Extract skills (look for common patterns)
        loader.add_xpath('required_skills', '//strong[contains(text(), "Required")]/following::li/text()')
        
        loader.add_value('job_url', response.url)
        loader.add_value('source_board', source_board)
        loader.add_value('scrape_date', datetime.now().isoformat())
        loader.add_value('job_id', self._generate_job_id(response.url))
        
        item = loader.load_item()
        if item.get('job_title') and item.get('company_name'):
            self.processed_count += 1
            logger.debug(f"Extracted: {item.get('job_title')} at {item.get('company_name')}")
            yield item
    
    def _parse_lever(self, response, loader, source_board):
        """Parse Lever job board"""
        
        # Extract job title
        loader.add_xpath('job_title', '//h2[@class="page-title"]/text() | //h1/text()')
        
        # Extract company name
        loader.add_xpath('company_name', '//a[@class="company-name"]/text() | //span[@class="company"]/text()')
        
        # Extract location
        loader.add_xpath('location', '//div[@class="location"]/text() | //span[@class="location"]/text()')
        
        # Extract employment type
        loader.add_xpath('employment_type', '//span[contains(text(), "Full-time") or contains(text(), "Part-time")]/text()')
        
        # Extract job description
        loader.add_xpath('job_description', '//div[@class="description"]//text() | //div[@class="content"]//text()')
        
        # Extract posted date
        loader.add_xpath('posted_date', '//span[@class="posted-date"]/text()')
        
        # Extract skills
        loader.add_xpath('required_skills', '//h3[contains(text(), "Skills")]/following::li/text()')
        
        loader.add_value('job_url', response.url)
        loader.add_value('source_board', source_board)
        loader.add_value('scrape_date', datetime.now().isoformat())
        loader.add_value('job_id', self._generate_job_id(response.url))
        
        item = loader.load_item()
        if item.get('job_title') and item.get('company_name'):
            self.processed_count += 1
            logger.debug(f"Extracted: {item.get('job_title')} at {item.get('company_name')}")
            yield item
    
    def _parse_generic(self, response, loader, source_board):
        """Parse generic job page (Ashby, GitHub, Stripe, etc.)"""
        
        # Extract job title (common patterns)
        loader.add_xpath('job_title', 
            '//h1/text() | //h2[contains(@class, "title")]/text() | //span[@class="job-title"]/text() | //h1[@class="job-title"]/text()')
        
        # Extract company name
        loader.add_value('company_name', self._extract_company_from_url(response.url) or 'Unknown')
        
        # Extract location (more flexible)
        loader.add_xpath('location',
            '//span[@class="location"]/text() | //span[contains(text(), "Location")]/following::text()[1] | //div[@class="job-location"]/text() | //div[contains(@class, "location")]/text()')
        
        # Extract job description (more flexible)
        loader.add_xpath('job_description',
            '//div[@class="job-description"]//text() | //section[@class="description"]//text() | //article//text() | //main//text() | //div[contains(@class, "description")]//text()')
        
        # Extract employment type
        loader.add_xpath('employment_type',
            '//span[contains(text(), "Full-time") or contains(text(), "Part-time") or contains(text(), "Contract")]/text() | //div[contains(text(), "Full-time") or contains(text(), "Part-time")]/text()')
        
        # Extract posted date
        loader.add_xpath('posted_date',
            '//span[contains(text(), "Posted") or contains(text(), "Created")]/following::text()[1] | //*[contains(text(), "Posted")]/following::text()[1]')
        
        # Extract skills/requirements
        loader.add_xpath('required_skills',
            '//h3[contains(text(), "Requirements") or contains(text(), "Required Skills")]/following::li/text() | //div[contains(@class, "requirement")]//li/text() | //ul[@class="requirements"]//li/text() | //div[contains(text(), "Required")]/following::li/text()')
        
        loader.add_value('job_url', response.url)
        loader.add_value('source_board', source_board)
        loader.add_value('scrape_date', datetime.now().isoformat())
        loader.add_value('job_id', self._generate_job_id(response.url))
        
        item = loader.load_item()
        # Less strict - only require job_title (company_name is extracted from URL)
        if item.get('job_title'):
            self.processed_count += 1
            logger.debug(f"Extracted: {item.get('job_title')}")
            yield item
    
    def _extract_company_from_url(self, url):
        """Extract company name from URL"""
        if 'boards.greenhouse.io' in url:
            parts = url.split('/')
            if len(parts) > 3:
                return parts[3].replace('-', ' ').title()
        elif 'jobs.lever.co' in url:
            parts = url.split('/')
            if len(parts) > 3:
                return parts[3].replace('-', ' ').title()
        elif 'github.com' in url:
            return 'GitHub'
        elif 'stripe.com' in url:
            return 'Stripe'
        elif 'rippling.com' in url:
            return 'Rippling'
        return None
    
    def _generate_job_id(self, url):
        """Generate unique job ID from URL"""
        import hashlib
        return hashlib.md5(url.encode()).hexdigest()[:12]
    
    def errback(self, failure):
        """Handle request errors"""
        self.error_count += 1
        url = failure.request.meta.get('url', 'Unknown')
        logger.warning(f"Error downloading {url}: {failure.value}")
    
    def closed(self, reason):
        """Called when spider is closed"""
        logger.info("=" * 60)
        logger.info("SPIDER CLOSED - STATISTICS")
        logger.info("=" * 60)
        logger.info(f"Total URLs queued: {len(self.job_urls)}")
        logger.info(f"Successfully processed: {self.processed_count}")
        logger.info(f"Errors encountered: {self.error_count}")
        logger.info(f"Success rate: {(self.processed_count / len(self.job_urls) * 100 if self.job_urls else 0):.1f}%")
        logger.info("=" * 60)
