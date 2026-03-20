"""
Define the data structure for job listings
"""

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join
from scrapy.loader import ItemLoader
import re


def clean_text(text):
    """Clean and normalize text fields"""
    if not text:
        return ''
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    return text


def extract_location(text):
    """Extract location information"""
    if not text:
        return ''
    # Remove extra whitespace and normalize
    return clean_text(text)


def extract_skills(text):
    """Extract and normalize skills"""
    if not text:
        return []
    if isinstance(text, list):
        text = ' '.join(text)
    
    # Split by common delimiters
    skills = re.split(r'[,\n•\-]', text)
    skills = [s.strip() for s in skills if s.strip()]
    
    return skills


class JobItem(scrapy.Item):
    """Define job data structure"""
    
    # Required fields
    job_title = scrapy.Field()
    company_name = scrapy.Field()
    location = scrapy.Field()
    job_url = scrapy.Field()
    job_description = scrapy.Field()
    
    # Optional fields
    department = scrapy.Field()
    employment_type = scrapy.Field()  # Full-time, Part-time, Contract, Intern, etc.
    posted_date = scrapy.Field()
    required_skills = scrapy.Field()
    experience_level = scrapy.Field()  # Entry-level, Mid-level, Senior, etc.
    salary = scrapy.Field()
    
    # Metadata
    source_board = scrapy.Field()  # greenhouse, lever, ashby, etc.
    scrape_date = scrapy.Field()
    job_id = scrapy.Field()  # Unique identifier


class JobLoader(ItemLoader):
    """Custom item loader with default processors"""
    
    default_output_processor = TakeFirst()
    
    job_title_out = MapCompose(clean_text)
    company_name_out = MapCompose(clean_text)
    location_out = MapCompose(extract_location)
    job_description_out = MapCompose(clean_text)
    department_out = MapCompose(clean_text)
    employment_type_out = MapCompose(clean_text)
    posted_date_out = MapCompose(clean_text)
    required_skills_out = MapCompose(extract_skills)
    experience_level_out = MapCompose(clean_text)
    salary_out = MapCompose(clean_text)
    source_board_out = MapCompose(clean_text)
