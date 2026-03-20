"""
Pipelines for processing scraped job data
"""

import csv
import json
import logging
from datetime import datetime
from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)


class JobDuplicatesPipeline:
    """Remove duplicate job listings"""
    
    def __init__(self):
        self.seen_urls = set()
        self.duplicate_count = 0
        logger.info("JobDuplicatesPipeline initialized")
    
    def process_item(self, item, spider):
        """Check for duplicate URLs"""
        job_url = item.get('job_url')
        
        if not job_url:
            logger.warning("Item missing job_url, dropping")
            raise DropItem("Missing job_url")
        
        if job_url in self.seen_urls:
            self.duplicate_count += 1
            logger.debug(f"Duplicate URL found: {job_url}")
            raise DropItem(f"Duplicate job URL: {job_url}")
        
        self.seen_urls.add(job_url)
        return item
    
    def close_spider(self, spider):
        """Log statistics when spider closes"""
        logger.info(f"Removed {self.duplicate_count} duplicate items")


class JobCleaningPipeline:
    """Clean and validate job data"""
    
    def __init__(self):
        self.invalid_count = 0
        self.required_fields = ['job_title', 'company_name', 'location', 'job_url', 'job_description']
        logger.info("JobCleaningPipeline initialized")
    
    def process_item(self, item, spider):
        """Validate required fields and clean data"""
        
        # Check required fields
        for field in self.required_fields:
            if not item.get(field):
                self.invalid_count += 1
                logger.warning(f"Item missing required field: {field}")
                raise DropItem(f"Missing required field: {field}")
        
        # Clean text fields
        for field in item:
            if field not in ['required_skills']:
                value = item.get(field)
                if isinstance(value, str):
                    item[field] = value.strip()
        
        # Ensure skills is a list
        if isinstance(item.get('required_skills'), str):
            item['required_skills'] = [s.strip() for s in item['required_skills'].split(',')]
        elif not item.get('required_skills'):
            item['required_skills'] = []
        
        # Add scrape date if not present
        if not item.get('scrape_date'):
            item['scrape_date'] = datetime.now().isoformat()
        
        return item
    
    def close_spider(self, spider):
        """Log statistics"""
        logger.info(f"Dropped {self.invalid_count} items due to missing required fields")


class JobExportPipeline:
    """Export job data to CSV and JSON"""
    
    def __init__(self):
        self.csv_file = None
        self.csv_writer = None
        self.csv_path = '../data/final/jobs.csv'
        self.json_path = '../data/final/jobs.json'
        self.json_data = []
        self.exported_count = 0
        logger.info("JobExportPipeline initialized")
    
    def open_spider(self, spider):
        """Open CSV file for writing"""
        try:
            self.csv_file = open(self.csv_path, 'w', newline='', encoding='utf-8')
            fieldnames = [
                'job_title', 'company_name', 'location', 'department',
                'employment_type', 'posted_date', 'job_url', 'job_description',
                'required_skills', 'experience_level', 'salary', 'source_board',
                'scrape_date'
            ]
            self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=fieldnames)
            self.csv_writer.writeheader()
            logger.info(f"CSV file opened: {self.csv_path}")
        except Exception as e:
            logger.error(f"Error opening CSV file: {e}")
            raise
    
    def close_spider(self, spider):
        """Close CSV file and export JSON"""
        if self.csv_file:
            self.csv_file.close()
            logger.info(f"CSV file closed. Exported {self.exported_count} items")
        
        # Export to JSON
        try:
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(self.json_data, f, indent=2, ensure_ascii=False)
            logger.info(f"JSON file saved: {self.json_path}")
        except Exception as e:
            logger.error(f"Error saving JSON file: {e}")
    
    def process_item(self, item, spider):
        """Write item to CSV and collect for JSON"""
        try:
            # Convert item to dict for CSV
            item_dict = dict(item)
            
            # Convert list fields to strings for CSV
            if isinstance(item_dict.get('required_skills'), list):
                item_dict['required_skills'] = ', '.join(item_dict['required_skills'])
            
            # Write to CSV
            self.csv_writer.writerow(item_dict)
            self.exported_count += 1
            
            # Collect for JSON export
            self.json_data.append(item_dict)
            
            logger.debug(f"Exported job: {item.get('job_title')} at {item.get('company_name')}")
        
        except Exception as e:
            logger.error(f"Error writing to CSV: {e}")
            raise DropItem(f"Error exporting item: {e}")
        
        return item


class DataValidationPipeline:
    """Validate data quality and log issues"""
    
    def __init__(self):
        self.issues = {
            'missing_description': 0,
            'missing_skills': 0,
            'missing_location': 0,
        }
        logger.info("DataValidationPipeline initialized")
    
    def process_item(self, item, spider):
        """Check for data quality issues"""
        
        if len(item.get('job_description', ' ').strip()) < 50:
            self.issues['missing_description'] += 1
            logger.warning(f"Short description for {item.get('job_title')}")
        
        if not item.get('required_skills') or len(item.get('required_skills', [])) == 0:
            self.issues['missing_skills'] += 1
            logger.warning(f"No skills found for {item.get('job_title')}")
        
        if not item.get('location'):
            self.issues['missing_location'] += 1
            logger.warning(f"No location for {item.get('job_title')}")
        
        return item
    
    def close_spider(self, spider):
        """Log data quality summary"""
        logger.info("Data Quality Summary:")
        for issue, count in self.issues.items():
            logger.info(f"  {issue}: {count}")
