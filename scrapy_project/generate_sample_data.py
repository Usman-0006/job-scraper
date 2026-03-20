#!/usr/bin/env python3
"""
Sample Data Generator for Testing the Job Analysis Pipeline
Use this to generate sample jobs.csv if Selenium/Scrapy don't return real data
This helps test the analysis and visualization components
"""

import csv
import json
from pathlib import Path
from datetime import datetime, timedelta
import random

# Sample job data to populate
SAMPLE_JOBS = [
    {
        "job_title": "Senior Python Developer",
        "company_name": "TechCorp",
        "location": "San Francisco, CA",
        "department": "Engineering",
        "employment_type": "Full-time",
        "posted_date": (datetime.now() - timedelta(days=5)).isoformat(),
        "job_url": "https://jobs.example.com/python-senior-1",
        "job_description": "We are looking for a senior Python developer with 5+ years of experience. Must be proficient in Django, FastAPI, and PostgreSQL.",
        "required_skills": "Python, Django, FastAPI, PostgreSQL, Docker, Git",
        "experience_level": "Senior",
        "salary": "150000-200000",
        "source_board": "Multiple Sources",
        "scrape_date": datetime.now().isoformat(),
    },
    {
        "job_title": "Junior JavaScript Developer",
        "company_name": "WebDev Inc",
        "location": "Remote",
        "department": "Frontend",
        "employment_type": "Full-time",
        "posted_date": (datetime.now() - timedelta(days=3)).isoformat(),
        "job_url": "https://jobs.example.com/js-junior-1",
        "job_description": "Great opportunity for junior developers to learn React and modern JavaScript. We mentor our junior developers!",
        "required_skills": "JavaScript, React, HTML, CSS, Git",
        "experience_level": "Entry-level",
        "salary": "70000-90000",
        "source_board": "Multiple Sources",
        "scrape_date": datetime.now().isoformat(),
    },
    {
        "job_title": "Data Analyst Intern",
        "company_name": "DataTech Solutions",
        "location": "New York, NY",
        "department": "Analytics",
        "employment_type": "Internship",
        "posted_date": (datetime.now() - timedelta(days=1)).isoformat(),
        "job_url": "https://jobs.example.com/data-intern-1",
        "job_description": "Internship program for data analysts. Work with SQL, Python, and Tableau to analyze business data.",
        "required_skills": "SQL, Python, Tableau, Excel",
        "experience_level": "Intern",
        "salary": "18-22",
        "source_board": "Multiple Sources",
        "scrape_date": datetime.now().isoformat(),
    },
    {
        "job_title": "DevOps Engineer",
        "company_name": "CloudOps",
        "location": "Seattle, WA",
        "department": "Infrastructure",
        "employment_type": "Full-time",
        "posted_date": (datetime.now() - timedelta(days=7)).isoformat(),
        "job_url": "https://jobs.example.com/devops-1",
        "job_description": "Looking for experienced DevOps engineer to manage our Kubernetes infrastructure on AWS.",
        "required_skills": "Kubernetes, Docker, AWS, Terraform, Bash",
        "experience_level": "Mid-level",
        "salary": "120000-160000",
        "source_board": "Multiple Sources",
        "scrape_date": datetime.now().isoformat(),
    },
    {
        "job_title": "Product Manager",
        "company_name": "Startup XYZ",
        "location": "Remote",
        "department": "Product",
        "employment_type": "Full-time",
        "posted_date": (datetime.now() - timedelta(days=2)).isoformat(),
        "job_url": "https://jobs.example.com/pm-1",
        "job_description": "We seek a PM to lead product strategy for our SaaS platform. 3+ years PM experience required.",
        "required_skills": "Product Strategy, Analytics, SQL, Communication",
        "experience_level": "Mid-level",
        "salary": "140000-180000",
        "source_board": "Multiple Sources",
        "scrape_date": datetime.now().isoformat(),
    },
    {
        "job_title": "Data Scientist",
        "company_name": "AI Labs",
        "location": "San Francisco, CA",
        "department": "ML/AI",
        "employment_type": "Full-time",
        "posted_date": (datetime.now() - timedelta(days=4)).isoformat(),
        "job_url": "https://jobs.example.com/ds-1",
        "job_description": "Build ML models to improve our recommendation engine. PhD or 5+ years industry experience preferred.",
        "required_skills": "Python, Machine Learning, TensorFlow, Statistics, SQL",
        "experience_level": "Senior",
        "salary": "160000-220000",
        "source_board": "Multiple Sources",
        "scrape_date": datetime.now().isoformat(),
    },
    {
        "job_title": "QA Engineer",
        "company_name": "Quality First",
        "location": "Austin, TX",
        "department": "QA",
        "employment_type": "Full-time",
        "posted_date": (datetime.now() - timedelta(days=6)).isoformat(),
        "job_url": "https://jobs.example.com/qa-1",
        "job_description": "Test automation engineer needed for our agile team. Selenium and Python experience required.",
        "required_skills": "Selenium, Python, JavaScript, Test Automation, Jira",
        "experience_level": "Mid-level",
        "salary": "90000-120000",
        "source_board": "Multiple Sources",
        "scrape_date": datetime.now().isoformat(),
    },
    {
        "job_title": "TypeScript Developer",
        "company_name": "Modern Stack Inc",
        "location": "Remote",
        "department": "Backend",
        "employment_type": "Full-time",
        "posted_date": (datetime.now() - timedelta(days=8)).isoformat(),
        "job_url": "https://jobs.example.com/ts-backend-1",
        "job_description": "Build scalable backend services using Node.js and TypeScript. 3+ years experience.",
        "required_skills": "TypeScript, Node.js, React, PostgreSQL, Docker",
        "experience_level": "Mid-level",
        "salary": "110000-150000",
        "source_board": "Multiple Sources",
        "scrape_date": datetime.now().isoformat(),
    },
]


def generate_csv(output_path):
    """Generate sample jobs.csv"""
    try:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'job_title', 'company_name', 'location', 'department',
                'employment_type', 'posted_date', 'job_url', 'job_description',
                'required_skills', 'experience_level', 'salary', 'source_board',
                'scrape_date'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(SAMPLE_JOBS)
        
        print(f"✓ Generated {len(SAMPLE_JOBS)} sample jobs in {output_path}")
        return True
    except Exception as e:
        print(f"✗ Error generating CSV: {e}")
        return False


def generate_json(output_path):
    """Generate sample jobs.json"""
    try:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(SAMPLE_JOBS, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Generated {len(SAMPLE_JOBS)} sample jobs in {output_path}")
        return True
    except Exception as e:
        print(f"✗ Error generating JSON: {e}")
        return False


if __name__ == '__main__':
    csv_path = '../data/final/jobs.csv'
    json_path = '../data/final/jobs.json'
    
    print("=" * 70)
    print("Generating Sample Job Data for Testing")
    print("=" * 70)
    
    csv_success = generate_csv(csv_path)
    json_success = generate_json(json_path)
    
    if csv_success and json_success:
        print("\n✓ Sample data generated successfully!")
        print(f"  - CSV: {csv_path}")
        print(f"  - JSON: {json_path}")
        print("\nNow you can run the analysis scripts:")
        print("  cd ../analysis")
        print("  python analyze_jobs.py")
        print("  python visualize_jobs.py")
    else:
        print("\n✗ Failed to generate sample data")
