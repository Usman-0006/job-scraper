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
    allowed_domains = ['boards.greenhouse.io', 'jobs.lever.co', 'ashbyhq.com', 'github.com', 'stripe.com', 'rippling.com']
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 2,
        'ROBOTSTXT_OBEY': True,
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.job_urls = []
        self.processed_count = 0
        self.error_count = 0
    
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
                        logger.debug(f"Queued URL: {url}")
        except FileNotFoundError:
            logger.error(f"Job links file not found: {csv_file}")
            return
        except Exception as e:
            logger.error(f"Error reading job links: {e}")
            return
        
        logger.info(f"Starting to scrape {len(self.job_urls)} job URLs")
        
        for url in self.job_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                errback=self.errback,
                meta={'url': url}
            )
    
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
        loader.add_xpath('required_skills', '//strong[contains(text(), "Required")]/following::li[1:10]/text()')
        
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
        loader.add_xpath('required_skills', '//h3[contains(text(), "Skills")]/following::li[1:15]/text()')
        
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
            '//h1/text() | //h2[contains(@class, "title")]/text() | //span[@class="job-title"]/text()')
        
        # Extract company name
        loader.add_value('company_name', self._extract_company_from_url(response.url) or 'Unknown')
        
        # Extract location
        loader.add_xpath('location',
            '//span[@class="location"]/text() | //span[contains(text(), "Location")]/following::text()[1] | //div[@class="job-location"]/text()')
        
        # Extract job description
        loader.add_xpath('job_description',
            '//div[@class="job-description"]//text() | //section[@class="description"]//text() | //article//text()')
        
        # Extract employment type
        loader.add_xpath('employment_type',
            '//span[contains(text(), "Full-time") or contains(text(), "Part-time") or contains(text(), "Contract")]/text()')
        
        # Extract posted date
        loader.add_xpath('posted_date',
            '//span[contains(text(), "Posted") or contains(text(), "Created")]/following::text()[1]')
        
        # Extract skills/requirements
        loader.add_xpath('required_skills',
            '//h3[contains(text(), "Requirements") or contains(text(), "Required Skills")]/following::li[1:20]/text()')
        
        loader.add_value('job_url', response.url)
        loader.add_value('source_board', source_board)
        loader.add_value('scrape_date', datetime.now().isoformat())
        loader.add_value('job_id', self._generate_job_id(response.url))
        
        item = loader.load_item()
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
